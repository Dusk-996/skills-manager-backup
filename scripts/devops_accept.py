"""静态验收；不连接服务器、不执行部署、不读取环境变量的真实值。"""
from pathlib import Path
import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['accept', 'report'])
parser.add_argument('--project', required=True)
parser.add_argument('--output')
args = parser.parse_args()
root = Path(args.project).resolve(strict=True)
if not root.is_dir():
    parser.error('--project 必须是目录')
skip = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build', '.next', 'backup', 'backups'}
errors, warnings, files = [], [], []
for p in root.rglob('*'):
    if not p.is_file() or any(part in skip for part in p.relative_to(root).parts) or p.stat().st_size > 1_000_000:
        continue
    if p.suffix.lower() not in {'.yml', '.yaml', '.py', '.go', '.json', '.env'} and p.name not in {'Dockerfile', '.env.production'}:
        continue
    rel = p.relative_to(root).as_posix()
    text = p.read_text(encoding='utf-8-sig', errors='replace')
    files.append(rel)
    # 静态模式只覆盖能可靠定位的硬失败项；输出不回显配置内容。
    patterns = [(r'(?m)^\s*image:\s*[^\s#]+:latest(?:\s|$)', '容器镜像使用 latest'),
                (r'(?m)^\s*FROM\s+[^\s#]+:latest(?:\s|$)', 'Dockerfile 使用 latest'),
                (r'(?m)^\s*[^#\n]*\breload\s*=\s*True\b', '发现 reload=True，需确认未作为生产启动'),
                (r'allow_origins\s*=\s*\[\s*[\'"]\*[\'"]\s*\]|AllowAllOrigins\s*:\s*true', 'CORS 允许任意来源')]
    for pattern, label in patterns:
        if re.search(pattern, text):
            errors.append({'file': rel, 'issue': label})
    if p.name == '.env.production' and re.search(r'(?m)^\s*VITE_USE_MOCK\s*=\s*(?:true|1)\s*$', text, re.I):
        errors.append({'file': rel, 'issue': '生产环境启用了 Mock'})
    if re.search(r'(?m)^kind:\s*Deployment\s*$', text):
        for probe in ('readinessProbe:', 'livenessProbe:'):
            if probe not in text:
                warnings.append({'file': rel, 'issue': 'Deployment 缺少 ' + probe[:-1]})
if not files:
    warnings.append({'file': '.', 'issue': '没有发现可静态检查的配置或代码；不能据此判断项目已就绪'})
result = {'ok': not errors, 'mode': 'static', 'project': str(root), 'checked_files': len(files), 'errors': errors, 'warnings': warnings,
          'not_verified': ['实际启动、镜像构建、服务健康', '远程主机或 Kubernetes 状态', '备份可恢复性和实际回滚', '业务正确性及真实 Secret 管理']}
if args.action == 'report':
    output = Path(args.output).resolve() if args.output else root / 'acceptance-report.md'
    if output.exists():
        parser.error('报告已存在，请指定新的 --output；不自动覆盖历史记录')
    lines = ['# 静态验收报告', '', f"结果：{'通过当前静态规则' if result['ok'] else '未通过'}。此结果不等于生产就绪。", '', f'检查文件：{len(files)} 个。', '']
    for category in ('errors', 'warnings'):
        lines += [f'## {category}', ''] + [f"- {x['file']}：{x['issue']}" for x in result[category]] + ['']
    lines += ['## 尚未验证', ''] + ['- ' + x for x in result['not_verified']]
    output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    result['report'] = str(output)
print(json.dumps(result, ensure_ascii=False))
raise SystemExit(0 if result['ok'] else 1)
