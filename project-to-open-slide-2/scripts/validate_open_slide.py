#!/usr/bin/env python3
"""Static contract and sensitive-data validation for one Open Slide deck."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"(?i)(password|passwd|token|secret|webhook)\s*[:=]\s*['\"]?(?!<)[^\s,'\"]{8,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
]
REMOTE_IMAGE = re.compile(r"""(?:src\s*=\s*|url\()\s*['"]?https?://""", re.I)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slide-dir", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    slide_dir = Path(args.slide_dir)
    ledger_path = Path(args.ledger)
    errors: list[str] = []
    warnings: list[str] = []
    index = slide_dir / "index.tsx"
    if not index.exists():
        errors.append("missing index.tsx")
        text = ""
    else:
        text = index.read_text("utf-8")
    if "1920" not in text or "1080" not in text:
        warnings.append("未在源码中发现 1920×1080 显式尺寸，请由浏览器验收确认")
    if REMOTE_IMAGE.search(text):
        errors.append("检测到外部图片热链接")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append("检测到疑似敏感信息")
            break
    if not ledger_path.exists():
        errors.append("Evidence Ledger 不存在")
    else:
        try:
            json.loads(ledger_path.read_text("utf-8"))
        except json.JSONDecodeError:
            errors.append("Evidence Ledger 不是有效 JSON")
    if "export const notes" not in text:
        errors.append("缺少演讲者备注导出")
    report = {"ok": not errors, "errors": errors, "warnings": warnings}
    if args.output:
        Path(args.output).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
