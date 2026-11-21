"""从备份仓库已暂存的 Git blob 生成或验证 backup-manifest.json。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile


MANIFEST = "backup-manifest.json"
CATALOG = "skill-catalog.json"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def indexed_files(repo):
    result = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, oid, stage = meta.split()
        path = raw_path.decode("utf-8")
        if stage != b"0" or mode not in (b"100644", b"100755", b"120000"):
            raise ValueError(f"索引有未合并条目或非 blob 路径：{path}")
        result[path] = oid
    return result


def blob_hashes(repo, oids):
    # 读取索引锁定的对象；一个 blob 只读一次，大文件分块计算。
    hashes = {}
    with subprocess.Popen(["git", "-C", str(repo), "cat-file", "--batch"],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as batch:
        for oid in oids:
            batch.stdin.write(oid + b"\n")
            batch.stdin.flush()
            header = batch.stdout.readline().split()
            if len(header) != 3 or header[:2] != [oid, b"blob"]:
                raise ValueError(f"无法读取 Git blob {oid.decode()}")
            size = int(header[2])
            digest = hashlib.sha256()
            remaining = size
            while remaining:
                data = batch.stdout.read(min(1024 * 1024, remaining))
                if not data:
                    raise ValueError("Git 对象提前结束")
                digest.update(data)
                remaining -= len(data)
            if batch.stdout.read(1) != b"\n":
                raise ValueError("Git 对象输出不完整")
            hashes[oid] = (size, digest.hexdigest())
        batch.stdin.close()
        if batch.wait():
            raise ValueError("读取 Git 对象失败")
    return hashes


def build(repo, index, manifest):
    catalog = json.loads(git(repo, "cat-file", "blob", index[CATALOG].decode()))
    tracked = {path: oid for path, oid in index.items() if path != MANIFEST}
    signatures = blob_hashes(repo, dict.fromkeys(tracked.values()))
    previous = {item["path"]: item for item in manifest["files"]}
    rows = []
    for path in sorted(tracked):
        size, sha = signatures[tracked[path]]
        # 现有格式包含 path、bytes、sha256；保留今后可能添加的逐项元数据。
        row = dict(previous.get(path, {}))
        row.update(path=path, bytes=size, sha256=sha)
        rows.append(row)
    return dict(manifest, snapshot_date=catalog["snapshot_date"], skills=catalog["total_skills"],
                files_skills=catalog["files"], inventory_only=catalog["inventory_only"], files=rows)


def write_manifest(path, original, current, updated):
    if json.loads(current) == updated:
        return
    # 保留用户可能正在编辑的清单；允许 Git 检出时转换换行。
    if current.replace(b"\r\n", b"\n") != original.replace(b"\r\n", b"\n"):
        raise ValueError("清单有未暂存的编辑，请先核对")
    data = (json.dumps(updated, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if b"\r\n" in current:
        data = data.replace(b"\n", b"\r\n")
    if current.startswith(b"\xef\xbb\xbf"):
        data = b"\xef\xbb\xbf" + data
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        tmp = Path(stream.name)
    try:
        tmp.write_bytes(data)
        tmp.chmod(stat.S_IMODE(path.stat().st_mode))
        if current != path.read_bytes():
            raise ValueError("写入前清单发生变化，请从最新索引重试")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="备份仓库根目录")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="仅更新工作区清单，复核后另行暂存")
    mode.add_argument("--check", action="store_true", help="验证已暂存的清单（默认）")
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    try:
        if git(repo, "rev-parse", "--show-prefix").strip():
            raise ValueError("--repo 应指向工作树根目录")
        index = indexed_files(repo)
        original = git(repo, "cat-file", "blob", index[MANIFEST].decode())
        manifest = json.loads(original)
        path = repo / MANIFEST
        current = None
        if args.write:
            if not stat.S_ISREG(path.lstat().st_mode):
                raise ValueError("清单应是普通文件")
            current = path.read_bytes()
        updated = build(repo, index, manifest)
        if indexed_files(repo) != index:
            raise ValueError("计算期间 Git 索引发生变化，请重试")
        if args.write:
            write_manifest(path, original, current, updated)
        elif manifest != updated:
            raise ValueError("暂存的清单与 Git 索引不一致，运行 --write 并复核、暂存清单后重试")
        print(f"{'工作区清单已核对' if args.write else '暂存清单通过'}：{len(updated['files'])} 个文件")
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"backup_manifest: {exc}\n")


if __name__ == "__main__":
    main()
