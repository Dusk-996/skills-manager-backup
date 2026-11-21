"""从技能目录生成中文 README；只使用标准库，构建函数不访问磁盘或 Git。"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import PurePosixPath
import re
from urllib.parse import quote, urlsplit


EXPECTED_SKILL_COUNT = 68
REPOSITORY_URL = "https://github.com/Dusk-996/skills-manager-backup"
ATLAS_NAVIGATION = (
    ("Vibe Coding · 构建运维工具", (("原型转 React Mock", "prototype-to-mock"), ("从 Mock 确认后端选型", "mock-to-architecture"))),
    ("协作开发与交接", (("执行既有计划", "execute-plan"), ("验证与交接", "release-branch"))),
    ("值班排障与观测", (("从异常定位故障", "incident"), ("制作 Grafana 看板", "observability"))),
    ("学习与复习", (("从材料到学习路线图", "notes-roadmap"),)),
    ("技术表达与办公交付", (("挑选图稿形式", "explain-visually"), ("准备技术分享", "slides"))),
    ("维护个人技能库和 Codex 环境", (("查找和安装技能", "find-install"), ("迁移规则与配置代理", "codex-environment"))),
)
REPLACED_ENTRY_NAMES = frozenset({
    "create-rule", "create-skill", "create-subagent", "migrate-to-skills", "update-cursor-settings",
})


def _cell(value: object) -> str:
    """转义分隔符，避免用途内容改变两列表格结构。"""
    return str(value).strip().replace("\r", " ").replace("\n", " ").replace("|", "\\|")


def _relative_path(value: object, *, required: bool) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if not text:
        if required:
            raise ValueError("files 状态必须提供仓库内相对路径")
        return ""
    path = PurePosixPath(text)
    if (
        path.is_absolute()
        or ".." in path.parts
        or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", text)
        or any(character in text for character in "\x00\r\n")
    ):
        raise ValueError(f"技能路径必须是仓库内相对路径：{text}")
    return path.as_posix()


def validate_records(records: Iterable[Mapping[str, object]]) -> list[dict[str, str]]:
    """检查固定快照的数量、名称、中文用途及路径格式。"""
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("每条技能记录必须是对象")
        missing = {"name", "purpose", "source_group", "path", "status"} - record.keys()
        if missing:
            raise ValueError(f"技能记录缺少字段：{', '.join(sorted(missing))}")
        name = str(record["name"]).strip()
        purpose = str(record["purpose"]).strip()
        group = str(record["source_group"]).strip()
        status = str(record["status"])
        if not name or not purpose or not group:
            raise ValueError("技能名称、中文用途和来源不能为空")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
            raise ValueError(f"技能名称格式无效：{name}")
        if not re.search(r"[\u3400-\u9fff]", purpose):
            raise ValueError(f"技能用途必须有中文说明：{name}")
        if name.casefold() in seen:
            raise ValueError(f"技能名称重复：{name}")
        if name.casefold() in REPLACED_ENTRY_NAMES:
            raise ValueError(f"旧入口不再属于 Codex 目录：{name}")
        if status not in {"files", "inventory_only"}:
            raise ValueError(f"未知备份状态：{status}")
        seen.add(name.casefold())
        rows.append({
            "name": name,
            "purpose": purpose,
            "path": _relative_path(record["path"], required=status == "files"),
            "status": status,
        })
    if len(rows) != EXPECTED_SKILL_COUNT:
        raise ValueError(f"技能记录必须为 {EXPECTED_SKILL_COUNT} 条，实际为 {len(rows)} 条")
    return rows


def build_readme(
    records: Iterable[Mapping[str, object]],
    snapshot_date: object,
    remote_url: str,
) -> str:
    """生成名称与中文用途两列表格，供发布准备脚本及仓库 CLI 共用。"""
    rows = validate_records(records)
    parsed_url = urlsplit(remote_url)
    if (
        parsed_url.scheme != "https"
        or not parsed_url.netloc
        or parsed_url.username is not None
        or parsed_url.password is not None
        or parsed_url.query
        or parsed_url.fragment
        or re.search(r"[\s()<>]", remote_url)
    ):
        raise ValueError("remote_url 必须为不含凭据或查询参数的 HTTPS 仓库地址")
    repo_url = remote_url.rstrip("/").removesuffix(".git")
    lines = [
        "# Codex 技能目录与中文用途",
        "",
        f"更新日期：{_cell(snapshot_date)}。仓库：[skills-manager-backup]({repo_url})。",
        "",
        f"本目录汇总 **{len(rows)} 个 Codex 技能**。点击技能名称查看对应指令或使用说明。",
        "",
        "安装、恢复、运行条件与许可说明见 [使用说明](docs/RESTORE.md)。",
        "",
        "## 按工作场景查找",
        "",
        "[浏览全部场景、已有材料和下一步](docs/atlas/README.md)",
        "",
        "| 工作流 | 从这里开始 |",
        "|---|---|",
    ]
    for group, entries in ATLAS_NAVIGATION:
        links = " · ".join(f"[{label}](docs/atlas/{slug}.md)" for label, slug in entries)
        lines.append(f"| {group} | {links} |")
    lines += ["", "## 全部技能", "", "| 技能名称 | 中文用途 |", "|---|---|"]
    for row in sorted(rows, key=lambda item: item["name"].casefold()):
        if row["status"] == "files":
            path = PurePosixPath(row["path"])
            target = path if path.name == "SKILL.md" else path / "SKILL.md"
        else:
            target = PurePosixPath(row["path"] or "docs/RESTORE.md")
        escaped_path = quote(target.as_posix(), safe="/._-@")
        lines.append(f"| [{row['name']}]({escaped_path}) | {_cell(row['purpose'])} |")
    lines.append("")
    return "\n".join(lines)
