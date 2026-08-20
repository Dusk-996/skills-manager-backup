#!/usr/bin/env python3
"""Verify the expected Open Slide delivery layout and image-PPTX package."""

from __future__ import annotations

import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


WORK_FILES = (
    "brief.md",
    "outline.md",
    "decisions.md",
    "source-manifest.json",
    "evidence-ledger.json",
    "qa-report.json",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--expected-pages", required=True, type=int)
    parser.add_argument("--output")
    args = parser.parse_args()

    target = Path(args.target)
    work = target / ".open-slide-work" / args.id
    export = target / "exports" / args.id
    errors: list[str] = []
    for name in WORK_FILES:
        if not (work / name).exists():
            errors.append(f"missing work file: {name}")
    if not (target / "slides" / args.id / "index.tsx").exists():
        errors.append("missing slide source")
    if not (export / "html" / "index.html").exists():
        errors.append("missing HTML export")

    pptx = export / f"{args.id}.pptx"
    slide_count = 0
    image_count = 0
    ratio = None
    if not pptx.exists():
        errors.append("missing PPTX export")
    else:
        try:
            with zipfile.ZipFile(pptx) as archive:
                names = set(archive.namelist())
                for required in ("[Content_Types].xml", "ppt/presentation.xml"):
                    if required not in names:
                        errors.append(f"invalid OOXML: missing {required}")
                slide_count = len(
                    [
                        name
                        for name in names
                        if name.startswith("ppt/slides/slide")
                        and name.endswith(".xml")
                    ]
                )
                image_count = len(
                    [name for name in names if name.startswith("ppt/media/image")]
                )
                if "ppt/presentation.xml" in names:
                    root = ET.fromstring(archive.read("ppt/presentation.xml"))
                    size = root.find(
                        "{http://schemas.openxmlformats.org/"
                        "presentationml/2006/main}sldSz"
                    )
                    if size is not None:
                        width = int(size.attrib["cx"])
                        height = int(size.attrib["cy"])
                        ratio = width / height
        except zipfile.BadZipFile:
            errors.append("PPTX is not a valid ZIP package")
        except (ET.ParseError, KeyError, TypeError, ValueError) as exc:
            errors.append(f"invalid presentation size: {exc}")
    if slide_count != args.expected_pages:
        errors.append(
            f"PPTX slide count {slide_count} != expected {args.expected_pages}"
        )
    if image_count < args.expected_pages:
        errors.append(
            f"PPTX image count {image_count} < expected {args.expected_pages}"
        )
    if ratio is None:
        errors.append("PPTX 未声明幻灯片尺寸")
    elif abs(ratio - (16 / 9)) > 0.001:
        errors.append(f"PPTX 页面比例不是 16:9，实际为 {ratio:.6f}")

    report = {
        "ok": not errors,
        "target": str(target),
        "id": args.id,
        "expected_pages": args.expected_pages,
        "pptx_slides": slide_count,
        "pptx_images": image_count,
        "pptx_ratio": ratio,
        "errors": errors,
    }
    if args.output:
        Path(args.output).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
