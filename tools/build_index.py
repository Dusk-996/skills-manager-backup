"""从 skill-catalog.json 检查或更新 README；默认只读，不依赖安装环境。

仓库根目录运行：python tools/build_index.py --check
确认需要更新后：python tools/build_index.py --write
"""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Sequence
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

from readme_builder import ATLAS_NAVIGATION, EXPECTED_SKILL_COUNT, REPOSITORY_URL, build_readme


def validate_relative_links(readme: str, repo_root: Path) -> int:
    """检查生成的全部相对链接，解析符号链接后仍须位于仓库内。"""
    root = repo_root.resolve(strict=True)
    count = 0
    for target in re.findall(r"\[[^\]\r\n]+\]\(([^)\r\n]+)\)", readme):
        parsed = urlsplit(target)
        if parsed.scheme == "https":
            continue
        if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
            raise ValueError(f"README 包含无效相对链接：{target}")
        relative = PurePosixPath(unquote(parsed.path))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"README 链接越出仓库：{target}")
        resolved = (root / relative).resolve(strict=True)
        if not resolved.is_relative_to(root):
            raise ValueError(f"README 链接越出仓库：{target}")
        if not resolved.is_file():
            raise ValueError(f"README 链接不是文件：{target}")
        count += 1
    # 恢复说明与场景目录各占一个入口，保留对丢失链接的检查。
    expected = EXPECTED_SKILL_COUNT + 2 + sum(len(entries) for _, entries in ATLAS_NAVIGATION)
    if count != expected:
        raise ValueError(f"README 应含 {expected} 个相对链接，实际为 {count} 个")
    return count


def generate_index(repo_root: Path) -> tuple[str, int]:
    """目录是唯一数据源，不读取历史审计脚本或本机技能安装信息。"""
    catalog = json.loads((repo_root / "skill-catalog.json").read_text(encoding="utf-8-sig"))
    if not isinstance(catalog, dict) or not isinstance(catalog.get("skills"), list):
        raise ValueError("skill-catalog.json 必须包含 skills 数组")
    records = catalog["skills"]
    if catalog.get("total_skills") != EXPECTED_SKILL_COUNT:
        raise ValueError(f"total_skills 必须为 {EXPECTED_SKILL_COUNT}")
    if not isinstance(catalog.get("snapshot_date"), str) or not catalog["snapshot_date"].strip():
        raise ValueError("snapshot_date 必须是非空字符串")
    readme = build_readme(records, catalog["snapshot_date"], REPOSITORY_URL)
    counts = Counter(record["status"] for record in records)
    for status in ("files", "inventory_only"):
        if catalog.get(status) != counts[status]:
            raise ValueError(f"目录统计字段 {status} 与技能记录不一致")
    link_count = validate_relative_links(readme, repo_root)
    return readme, link_count


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="校验目录、链接和 README 一致性（默认）")
    mode.add_argument("--write", action="store_true", help="校验通过后重新生成 README.md")
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    try:
        readme, link_count = generate_index(repo_root)
        readme_path = repo_root / "README.md"
        # 写入前完成所有数据与路径校验；--check 不修改任何文件。
        if args.write:
            readme_path.write_text(readme, encoding="utf-8", newline="\n")
            print(f"已生成 README.md：{EXPECTED_SKILL_COUNT} 条技能，{link_count} 个相对链接")
        elif readme_path.read_text(encoding="utf-8-sig") != readme:
            raise ValueError("README.md 与目录不一致；请运行 python tools/build_index.py --write")
        else:
            print(f"校验通过：{EXPECTED_SKILL_COUNT} 条技能，{link_count} 个相对链接，README.md 与目录一致")
    except (OSError, ValueError, TypeError) as error:
        print(f"校验失败：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
