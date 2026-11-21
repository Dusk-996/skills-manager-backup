"""Inventory installed skill directories and their recorded provenance, without fetching."""

import argparse
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import sys
from urllib.parse import urlsplit


def safe_source(value):
    """只显示来源位置，省略认证信息、查询参数与片段。"""
    if not isinstance(value, str) or not value:
        return None
    value = value.split("?", 1)[0].split("#", 1)[0]
    if "://" in value:
        try:
            url = urlsplit(value)
            if url.scheme == "file":
                return "file://" + url.path
            if url.scheme not in {"https", "http", "ssh", "git"} or not url.hostname:
                return None
            host = url.hostname
            if ":" in host:
                host = "[" + host + "]"
            if url.port is not None:
                host += ":" + str(url.port)
            return url.scheme + "://" + host + url.path
        except ValueError:
            return None
    scp = re.fullmatch(r"(?:[\w.-]+@)?([\w.-]+):([^\s:]+)", value)
    if scp and len(scp[1]) > 1:
        return "ssh://" + scp[1] + "/" + scp[2].lstrip("/")
    if re.fullmatch(r"[\w.-]+/[\w.-]+", value) or os.path.isabs(value):
        return value
    return None


def key(path):
    return os.path.normcase(os.path.abspath(path))


def link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    )


def manager_index(db, errors):
    """只读查询中央目录与实际部署记录。来源只用于定位候选上游。"""
    index = {}
    try:
        with sqlite3.connect(db.absolute().as_uri() + "?mode=ro", uri=True) as con:
            con.execute("PRAGMA query_only=ON")
            con.row_factory = sqlite3.Row
            targets = {}
            for row in con.execute("SELECT skill_id, tool, mode, status, target_path FROM skill_targets"):
                targets.setdefault(row["skill_id"], []).append(dict(row))
            for row in con.execute("""
                SELECT id, central_path, source_type, source_ref, source_ref_resolved,
                       source_subpath, source_branch, source_revision, content_hash FROM skills
            """):
                record = dict(row)
                for field in ("source_ref", "source_ref_resolved"):
                    record[field] = safe_source(record[field])
                source = record["source_ref_resolved"] or record["source_ref"] or ""
                record["backup_hint"] = bool(re.search(r"(?i)(?:^|[/_.-])(?:backup|mirror)(?:$|[/_.-])", source))
                record["targets"] = targets.get(record["id"], [])
                for path in [record["central_path"], *(t["target_path"] for t in record["targets"])]:
                    if path and os.path.isabs(path):
                        index[key(path)] = record
    except (OSError, sqlite3.Error) as exc:
        errors.append({"path": str(db), "error": str(exc)})
    return index


def lock_index(path, errors):
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))["skills"]
        if not isinstance(data, dict):
            raise ValueError("expected skills object")
        return {name: {
            "source": safe_source(row.get("sourceUrl") or row.get("source")),
            "source_type": row.get("sourceType"),
            "skill_path": row.get("skillPath"),
            "folder_hash": row.get("skillFolderHash"),
        } for name, row in data.items() if isinstance(row, dict)}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append({"path": str(path), "error": str(exc)})
        return {}


def skill_name(file):
    with file.open("rb") as stream:
        lines = stream.read(32768).decode("utf-8-sig", errors="replace").splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            match = re.fullmatch(r"""name:\s*['"]?([\w.-]+)['"]?\s*(?:#.*)?""", line)
            if match:
                return match[1]
    return None


def owner(path, codex):
    if path.is_relative_to(codex / "skills" / ".system"):
        return "system"
    if path.is_relative_to(codex / "plugins") or path.is_relative_to(codex / ".tmp" / "plugins"):
        return "plugin"
    return "unmanaged"


def git_hint(path):
    for directory in (path, *path.parents):
        if (directory / ".git").exists():
            return str(directory)
    return None


def project_roots():
    cwd = Path.cwd()
    repo = git_hint(cwd)
    for base in (cwd, *cwd.parents) if repo else (cwd,):
        for prefix in (".agents", ".codex"):
            root = base / prefix / "skills"
            if root.is_dir():
                yield root
        if str(base) == repo:
            break


def inventory(args):
    home = (args.home or Path.home()).absolute()
    codex = home / ".codex" if args.home else Path(os.environ.get("CODEX_HOME") or home / ".codex").absolute()
    agents = home / ".agents" / "skills"
    issues, skipped, found = [], [], {}
    db = args.manager_db or home / ".skills-manager" / "skills-manager.db"
    managers = manager_index(db, issues) if args.manager_db or db.is_file() else {}
    locks = lock_index(agents.parent / ".skill-lock.json", issues)
    roots = list(dict.fromkeys(p.absolute() for p in (args.root or [codex / "skills", agents, *project_roots()])))

    def record(path, root):
        marker = path / "SKILL.md"
        if not marker.is_file():
            return False
        real = path.resolve(strict=True)
        identity = key(real)
        if marker.resolve(strict=True).parent != real:
            skipped.append({"path": str(marker), "reason": "external SKILL.md link"})
            return True
        entry = found.get(identity)
        if entry is None:
            entry = {"name": skill_name(marker) or path.name, "real_path": str(real),
                     "locations": [], "owner": "unmanaged"}
            found[identity] = entry
        here = {"path": str(path), "root": str(root), "via_link": any(
            link(d) for d in (path, *path.parents) if d == root or d.is_relative_to(root)
        )}
        if here not in entry["locations"]:
            entry["locations"].append(here)
        kind = owner(path, codex)
        if kind == "unmanaged":
            kind = owner(real, codex)
        if kind in ("system", "plugin"):
            entry["owner"] = kind
        manager = managers.get(identity) or managers.get(key(path))
        if manager:
            entry["manager"] = manager
            if entry["owner"] == "unmanaged":
                entry["owner"] = "skills-manager"
            if here["via_link"] and key(manager["central_path"]) != identity:
                issues.append({"path": str(path), "error": "deployed link differs from recorded central_path"})
        elif entry["owner"] == "unmanaged":
            checkout = git_hint(real)
            if checkout:
                entry["git_root_hint"] = checkout
        if path.name in locks and (path.parent == agents or real.parent == agents):
            entry["lock_hint"] = locks[path.name]
        return True

    def scan(directory, root, depth):
        try:
            if record(directory, root):
                return
            if depth == 2:
                return
            # 只向下一层集合探测，每个目录设置上限，以免误遍历大型链接目标。
            with os.scandir(directory) as children:
                for index, child in enumerate(children):
                    if index >= 512:
                        skipped.append({"path": str(directory), "reason": "512-entry scan limit"})
                        break
                    if child.name.startswith(".") and not (
                        child.name == ".system" and key(directory) == key(codex / "skills")
                    ):
                        continue
                    child_path = directory / child.name
                    try:
                        if child.is_dir():
                            scan(child_path, root, depth + 1)
                        elif child.is_symlink() and not child_path.exists():
                            skipped.append({"path": str(child_path), "reason": "broken link"})
                    except (OSError, RuntimeError) as exc:
                        issues.append({"path": str(child_path), "error": str(exc)})
        except (OSError, RuntimeError) as exc:
            issues.append({"path": str(directory), "error": str(exc)})

    for root in roots:
        if not root.is_dir():
            if args.root:
                issues.append({"path": str(root), "error": "requested root is missing or not a directory"})
            else:
                skipped.append({"path": str(root), "reason": "optional root unavailable"})
            continue
        scan(root, root, 0)
    return {"roots": [str(r) for r in roots], "skills": sorted(found.values(), key=lambda e: (e["name"], e["real_path"])),
            "errors": issues, "skipped": skipped}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, help="use this profile (including its .codex directory)")
    parser.add_argument("--root", type=Path, action="append", help="scan only these skill/collection directories (repeatable)")
    parser.add_argument("--manager-db", type=Path, help="read provenance from this skills-manager SQLite database")
    report = inventory(parser.parse_args())
    sys.stdout.buffer.write((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
