#!/usr/bin/env python3
"""Three-way file sync for one verified skill. Python 3.9+; standard library only."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import socket
import stat
import sys
import tempfile
from contextlib import contextmanager


class Conflict(Exception):
    def __init__(self, paths):
        self.paths = sorted(set(paths))
        self.detail = {}
        super().__init__(", ".join(self.paths))


def checked_name(name):
    parts = name.split("/")
    if (not name or any(p in ("", ".", "..") or p.lower() == ".git" for p in parts)
            or "\\" in name or ":" in name or PureWindowsPath(name).drive
            or (os.name == "nt" and any(p.endswith((" ", ".")) or PureWindowsPath(p).is_reserved()
                                       for p in parts))):
        raise ValueError(f"Unsafe relative path: {name!r}")
    return name


def kind(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
        raise ValueError(f"Link/reparse point inside tree: {path}")
    if stat.S_ISDIR(info.st_mode):
        return "dir"
    if stat.S_ISREG(info.st_mode):
        return "file"
    raise ValueError(f"Unsupported file type: {path}")


def signature(path):
    what = kind(path)
    if what is None:
        return None
    if what != "file":
        raise ValueError(f"Expected a regular file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    execute = path.stat().st_mode & 0o111 if os.name != "nt" else 0
    return f"{digest.hexdigest()}:{execute:o}"


def scan(root):
    files, dirs = {}, set()

    def visit(folder):
        for item in folder.iterdir():
            name = checked_name(item.relative_to(root).as_posix())
            if kind(item) == "dir":
                dirs.add(name)
                visit(item)
            else:
                files[name] = signature(item)

    if kind(root) != "dir":
        raise ValueError(f"Missing directory: {root}")
    visit(root)
    return files, dirs


def skill_tree(root):
    files, dirs = scan(root)
    if not files.get("SKILL.md") or not (root / "SKILL.md").stat().st_size:
        raise ValueError(f"Missing or empty SKILL.md: {root}")
    return files, dirs


def disjoint(*roots):
    for i, root in enumerate(roots):
        for other in roots[:i]:
            if root == other or root in other.parents or other in root.parents:
                raise ValueError(f"Directories overlap: {root} / {other}")


def plan(current, dirs, base, new):
    changes, conflicts = {}, []
    all_files = set(current) | set(base) | set(new)
    if os.name == "nt" or sys.platform == "darwin":
        # 同名异大小写的路径可能指向同一对象，例如上游把 README 改名为 readme。
        spellings = {}
        names = set(dirs)
        for name in all_files:
            names.add(name)
            names.update(str(p) for p in PurePosixPath(name).parents)
        for name in names:
            other = spellings.setdefault(name.casefold(), name)
            if name != other:
                conflicts.extend((name, other))
    for path in sorted(all_files):
        old, local, incoming = base.get(path), current.get(path), new.get(path)
        if incoming == old or local == incoming:
            continue
        if local != old:
            conflicts.append(path)
        else:
            # 文件和目录相互替换可能吞掉本机目录内容，交给人工核对。
            parents = PurePosixPath(path).parents
            if incoming and (path in dirs or any(str(p) in current for p in parents)):
                conflicts.append(path)
            changes[path] = [local, incoming]
    if conflicts:
        raise Conflict(conflicts)
    return changes


@contextmanager
def exclusive(local, backup):
    # 同一目标的多个调用共用独占文件。进程被强杀时保留备份位置供恢复。
    lock = local.parent / f".{local.name}.skill-upstream-sync.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f"Check the owner of the existing lock: {lock}") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"host": socket.gethostname(), "pid": os.getpid(), "backup": str(backup)}, f)
        yield
    finally:
        lock.unlink()


def checked_target(root, rel):
    # 每次替换前重新检查父目录；目标根已解析，部署入口的顶层链接保持原样。
    if kind(root) != "dir":
        raise ValueError(f"Missing directory: {root}")
    path = root
    for part in PurePosixPath(checked_name(rel)).parts[:-1]:
        path = path / part
        if kind(path) == "file":
            raise Conflict([rel])
    return root / rel


def replace_one(target, before, source, after):
    actual = signature(target)
    if actual == after:
        return
    if actual != before:
        raise Conflict([str(target)])
    if after is None:
        target.unlink()
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tempname = tempfile.mkstemp(prefix=".skill-sync-", dir=target.parent)
    os.close(fd)
    temp = Path(tempname)
    try:
        shutil.copyfile(source, temp)
        mode = source.stat().st_mode & 0o777
        if before is not None:
            # 保留现有读写权限，仅同步上游可执行位。
            mode = (target.stat().st_mode & 0o666) | (mode & 0o111)
        temp.chmod(mode)
        if signature(temp) != after or signature(target) != before:
            raise Conflict([str(target)])
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.chmod(0o600)
            temp.unlink()


def make_backup(backup, local, changes, dirs):
    # POSIX 备份目录仅允许当前账号进入，Windows 继承所选父目录的 ACL。
    backup.mkdir(mode=0o700, parents=True, exist_ok=False)
    before = backup / "before"
    before.mkdir(mode=0o700)
    new_dirs = set()
    for rel, (old, new) in changes.items():
        if old:
            dest = before / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(checked_target(local, rel), dest)
        if new:
            new_dirs.update(str(p) for p in PurePosixPath(rel).parents if str(p) != "." and str(p) not in dirs)
    original, _ = scan(before)
    if original != {p: pair[0] for p, pair in changes.items() if pair[0]}:
        raise ValueError(f"Backup failed verification: {backup}")
    record = {"version": 1, "local": str(local), "changes": changes, "new_dirs": sorted(new_dirs)}
    (backup / "manifest.json").write_text(json.dumps(record, ensure_ascii=True, indent=2), encoding="utf-8")


def restore(backup, local, completed=None):
    disjoint(local, backup)
    if kind(backup / "manifest.json") != "file":
        raise ValueError("Incomplete backup: manifest.json missing")
    record = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    if record["version"] != 1 or Path(record["local"]) != local:
        raise ValueError("Backup belongs to a different destination or format")
    changes = record["changes"]
    before = backup / "before"
    saved, _ = scan(before)
    if saved != {p: pair[0] for p, pair in changes.items() if pair[0]}:
        raise ValueError("Backup contents failed verification")
    if completed is not None:
        changes = {p: changes[p] for p in completed}
    current, dirs = skill_tree(local)
    conflicts = []
    for rel, pair in changes.items():
        checked_target(local, rel)
        if rel in dirs or current.get(rel) not in pair:
            conflicts.append(rel)
    if conflicts:
        raise Conflict(conflicts)
    for rel, (old, new) in changes.items():
        replace_one(checked_target(local, rel), new, before / rel, old)
    # 仅清理本次更新新建、且回滚后为空的目录。
    for rel in sorted(record["new_dirs"], key=lambda p: p.count("/"), reverse=True):
        folder = checked_target(local, rel)
        if kind(folder) == "dir" and not any(folder.iterdir()):
            folder.rmdir()
    if any(signature(checked_target(local, p)) != pair[0] for p, pair in changes.items()):
        raise ValueError("Restored files failed verification")


def run(args):
    local = Path(args.local).resolve(strict=True)
    if args.restore:
        backup = Path(args.restore).resolve(strict=True)
        with exclusive(local, backup):
            restore(backup, local)
        return {"status": "restored", "local": str(local), "backup": str(backup)}

    base, upstream = [Path(p).resolve(strict=True) for p in (args.base, args.upstream)]
    backup = Path(args.backup).resolve() if args.backup else None
    disjoint(local, base, upstream, *([backup] if backup else []))
    baseline, _ = skill_tree(base)
    incoming, _ = skill_tree(upstream)

    def compare():
        current, dirs = skill_tree(local)
        preserved = sorted(p for p in set(current) | set(incoming)
                           if current.get(p) != incoming.get(p) and baseline.get(p) == incoming.get(p))
        detail = {"preserved": preserved, "local_only": preserved,
                  "local_matches_base": current == baseline, "local_matches_upstream": current == incoming}
        try:
            changes = plan(current, dirs, baseline, incoming)
        except Conflict as error:
            error.detail = detail
            raise
        detail["changes"] = list(changes)
        return current, dirs, changes, detail

    if not args.apply:
        _, _, changes, detail = compare()
        return {"status": "ready" if changes else "unchanged", **detail}

    with exclusive(local, backup):
        current, dirs, changes, detail = compare()
        if not changes:
            return {"status": "unchanged", **detail}
        make_backup(backup, local, changes, dirs)
        completed = []
        try:
            expected = current.copy()
            for rel, (old, new) in changes.items():
                replace_one(checked_target(local, rel), old, checked_target(upstream, rel), new)
                completed.append(rel)
                if new is None:
                    del expected[rel]
                else:
                    expected[rel] = new
            if skill_tree(local)[0] != expected:
                raise ValueError("Post-update verification found unexpected changes")
            detail.update(local_matches_base=expected == baseline, local_matches_upstream=expected == incoming)
        except (Exception, KeyboardInterrupt):
            try:
                restore(backup, local, completed)
            except (Exception, KeyboardInterrupt) as failure:
                raise ValueError(f"Automatic rollback incomplete. Inspect {backup}: {failure}") from failure
            raise
    return {"status": "updated", "backup": str(backup), **detail}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", required=True, help="installed skill directory")
    parser.add_argument("--base", help="verified previous official skill tree")
    parser.add_argument("--upstream", help="verified candidate official skill tree")
    parser.add_argument("--apply", action="store_true", help="apply the entire conflict-free plan")
    parser.add_argument("--backup", help="new directory outside all three trees")
    parser.add_argument("--restore", help="restore changed files from a previous backup")
    args = parser.parse_args()
    if args.restore:
        if args.base or args.upstream or args.apply or args.backup:
            parser.error("--restore takes only --local")
    elif not args.base or not args.upstream or (args.apply and not args.backup):
        parser.error("--base and --upstream are required; --apply also needs --backup")
    try:
        result = run(args)
        code = 0
    except Conflict as error:
        result, code = {"status": "conflict", "paths": error.paths, **error.detail}, 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        result, code = {"status": "error", "detail": str(error)}, 1
    print(json.dumps(result, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
