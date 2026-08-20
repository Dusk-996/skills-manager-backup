#!/usr/bin/env python3
"""Create a safe, deterministic material manifest without reading file contents."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".cache",
    "logs",
    "log",
    "data",
}
EXCLUDED_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}
EXCLUDED_SUFFIXES = {".key", ".pem", ".p12", ".pfx", ".crt", ".cer"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
DOC_SUFFIXES = {".md", ".txt", ".docx", ".pdf", ".pptx"}
CONFIG_SUFFIXES = {".yaml", ".yml", ".json", ".toml", ".ini", ".conf"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in DOC_SUFFIXES:
        return "document"
    if suffix in CONFIG_SUFFIXES:
        return "configuration"
    return "source"


def excluded(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part.lower() in EXCLUDED_DIRS for part in relative.parts[:-1]):
        return True
    name = path.name.lower()
    return (
        name in EXCLUDED_FILES
        or name.startswith(".env.")
        or path.suffix.lower() in EXCLUDED_SUFFIXES
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    files: list[dict[str, object]] = []
    excluded_count = 0
    for source_text in args.source:
        source = Path(source_text).expanduser().resolve()
        if not source.exists():
            parser.error(f"source does not exist: {source}")
        candidates = [source] if source.is_file() else source.rglob("*")
        for path in candidates:
            if not path.is_file():
                continue
            root = source.parent if source.is_file() else source
            if excluded(path, root):
                excluded_count += 1
                continue
            files.append(
                {
                    "source": str(source),
                    "path": path.relative_to(root).as_posix(),
                    "type": classify(path),
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )

    files.sort(key=lambda item: (str(item["source"]), str(item["path"])))
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "urls": [{"url": url, "status": "pending_fetch"} for url in args.url],
        "metrics": {
            "scanned_sources": len(args.source),
            "included_files": len(files),
            "excluded_files": excluded_count,
            "urls": len(args.url),
            "actual_read_files": 0,
            "question_rounds": 0,
            "generation_rounds": 0,
            "repair_rounds": 0,
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
