"""只读检查自定义代理的基础静态约束；不代替 Codex 的完整版本校验。"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import tomllib
except ImportError:
    raise SystemExit("需要 Python 3.11+ 的 tomllib；没有修改任何文件。")


def inspect(path: Path) -> dict:
    errors = []
    try:
        text = path.read_text(encoding="utf-8-sig")
        data = tomllib.loads(text)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "scope": "basic_static_only"}
    for key in ("name", "description", "developer_instructions"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} 必须是非空字符串")
    for key in ("sandbox_mode", "approval_policy", "model_provider", "mcp_servers"):
        if key in data:
            errors.append(f"{key} 不能在角色文件中覆盖父会话配置")
    return {"ok": not errors, "errors": errors, "scope": "basic_static_only"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="待检查的独立代理 TOML 文件")
    args = parser.parse_args()
    result = inspect(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
