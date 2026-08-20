---
name: deployment-packager
description: 为 DevOps 工具、平台后端、前端、agent、Shell 工具生成部署交付包。用户提到"部署""打包""生成 Dockerfile/docker-compose/K8s/systemd/Nginx 配置""发布到生产""agent 分发"时使用。
---

# 部署交付打包

把已有项目整理成可部署、可验证、可回滚的交付形态。优先面向国内网络和运维团队长期维护。

## 个人工具链入口

- 打包前优先读取 `../profile/ops-engineer-cn.yml`，继承默认部署目标、国内镜像源和安全门禁。
- 交付后建议运行 `../scripts/devops-skillctl.ps1 accept` 做静态验收；需要归档时运行 `../scripts/devops-skillctl.ps1 report`。
- Docker/K8s 真实验收只在用户明确要求且本机工具可用时执行；默认只输出建议命令和回滚方式。

## 工作流程

1. 识别部署目标：systemd、本机二进制、Docker、Docker Compose、Kubernetes、Nginx 前端托管、agent 分发。
2. 读取项目入口、端口、配置、依赖、健康检查路径。
3. 按目标读取对应 reference：
   - Docker Compose：`references/docker-compose.md`
   - Kubernetes：`references/kubernetes.md`
   - systemd：`references/systemd.md`
   - Nginx 前端：`references/nginx-frontend.md`
4. 生成或修改部署文件，保持最小改动。
5. 输出部署命令、验证命令、回滚方案、生产注意事项。

## 默认原则

- 交付结果必须符合 `../project-init/references/acceptance-rules.md` 的固定输出要求和硬失败项。
- 不使用 `latest` 作为生产发布依据。
- 配置和密钥分离，Secret 不写明文真实值。
- 容器优先非 root 用户。
- 所有部署必须有健康检查或冒烟验证。
- Kubernetes 变更必须给出 `kubectl rollout status` 和 `kubectl rollout undo`。
- 本机服务必须给出 systemd 安装、启动、日志查看、卸载或回滚命令。

## 输出格式

```markdown
## 影响范围
## 生成/修改文件
## 部署步骤
## 验证命令
## 回滚方案
## 国内环境注意事项
## 生产环境注意事项
```
