"""从本地 Git 对象导出指定提交的技能目录，无需 checkout。"""

import argparse
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
import sys
import tempfile
import unicodedata


def path_parts(name):
    parts = name.split("/")
    for part in parts:
        if (not part or part in (".", "..") or part.lower() in (".git", "git~1")
                or part.endswith((" ", ".")) or PureWindowsPath(part).is_reserved()
                or any(ord(ch) < 32 or ch in '<>:"\\|?*' for ch in part)):
            raise ValueError(f"不安全的 Git 路径 {name!r}")
    return parts


def export(repo, commit, subpath, out):
    if not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", commit):
        raise ValueError("--commit 需要完整的提交对象 ID")
    if os.path.lexists(out):
        raise FileExistsError(f"输出已存在 {out}")
    if subpath not in ("", "."):
        path_parts(subpath)

    cmd = ["git", "-C", str(repo)]
    # 保证从所指定的仓库读取真实对象，缺失对象时不触发部分克隆的网络获取。
    env = {k: v for k, v in os.environ.items() if k not in
           ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES")}
    env.update(GIT_NO_REPLACE_OBJECTS="1", GIT_NO_LAZY_FETCH="1")

    def git(*args):
        return subprocess.check_output([*cmd, *args], env=env)

    if git("cat-file", "-t", commit).strip() != b"commit":
        raise ValueError("--commit 必须指向 commit 对象")
    selector = commit + (":" + subpath if subpath not in ("", ".") else "^{tree}")
    tree = git("rev-parse", "--verify", selector).decode("ascii").strip()
    if git("cat-file", "-t", tree).strip() != b"tree":
        raise ValueError("--subpath 必须指向目录")
    entries = []
    seen = {}
    for row in git("ls-tree", "-r", "-z", "--full-tree", tree).split(b"\0"):
        if not row:
            continue
        meta, raw_name = row.split(b"\t", 1)
        mode, kind, oid = meta.split()
        name = raw_name.decode("utf-8")
        if kind != b"blob" or mode not in (b"100644", b"100755"):
            raise ValueError(f"需要普通文件 {name!r}，实际模式 {mode!r}")
        parts = path_parts(name)
        for i in range(1, len(parts) + 1):
            prefix = "/".join(parts[:i])
            key = unicodedata.normalize("NFC", prefix).casefold()
            if seen.setdefault(key, prefix) != prefix:
                raise ValueError(f"文件系统路径冲突 {name!r}")
        entries.append((parts, mode, oid))
    if not any(parts == ["SKILL.md"] for parts, _, _ in entries):
        raise ValueError("所选目录缺少 SKILL.md，请核对 --subpath")

    # 临时目录和输出同盘。全部 blob 读取成功后才发布快照。
    with tempfile.TemporaryDirectory(prefix=".git-snapshot-", dir=out.parent) as tmp:
        stage = Path(tmp) / "tree"
        stage.mkdir()
        with subprocess.Popen([*cmd, "cat-file", "--batch"], env=env,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE) as batch:
            for parts, mode, oid in entries:
                batch.stdin.write(oid + b"\n")
                batch.stdin.flush()
                header = batch.stdout.readline().split()
                if len(header) != 3 or header[:2] != [oid, b"blob"]:
                    raise ValueError(f"无法读取 Git blob {oid.decode('ascii')}")
                remaining = int(header[2])
                dest = stage.joinpath(*parts)
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("xb") as stream:
                    while remaining:
                        chunk = batch.stdout.read(min(remaining, 1024 * 1024))
                        if not chunk:
                            raise ValueError("Git blob 提前结束")
                        stream.write(chunk)
                        remaining -= len(chunk)
                if batch.stdout.read(1) != b"\n":
                    raise ValueError("Git blob 输出不完整")
                dest.chmod(0o755 if mode == b"100755" else 0o644)
            batch.stdin.close()
            if batch.wait() != 0:
                raise ValueError("git cat-file 失败")
        if os.path.lexists(out):
            raise FileExistsError(f"输出已存在 {out}")
        stage.rename(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="已获取对象的本地 Git 仓库")
    parser.add_argument("--commit", required=True, help="完整的 40 位或 64 位提交对象 ID")
    parser.add_argument("--subpath", default=".", help="技能在仓库中的精确子目录，默认仓库根目录")
    parser.add_argument("--out", required=True, type=Path, help="尚不存在的目录，其父目录必须存在")
    args = parser.parse_args()
    try:
        export(args.repo, args.commit, args.subpath, args.out)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"git_snapshot: {exc}\n")


if __name__ == "__main__":
    main()
