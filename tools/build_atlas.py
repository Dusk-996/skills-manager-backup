"""按场景清单生成 GitHub 导航页。默认只读，使用 --write 写入。"""
from __future__ import annotations

import argparse
from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote

from readme_builder import EXPECTED_SKILL_COUNT, REPOSITORY_URL, validate_records


ROOT = Path(__file__).resolve().parents[1]
PAGES_BASE = "https://dusk-996.github.io/skills-manager-backup/atlas"


def load_scenarios(root):
    catalog = json.loads((root / "skill-catalog.json").read_text(encoding="utf-8-sig"))
    rows = validate_records(catalog["skills"])
    if catalog.get("total_skills") != len(rows):
        raise ValueError("目录统计与实际技能名称数量不一致")
    skills = {row["name"]: row for row in rows}
    for record in catalog["skills"]:
        if record["status"] == "inventory_only":
            skills[record["name"]]["runtime"] = record["restore_source"]
    entries = json.loads((root / "atlas/scenarios.json").read_text(encoding="utf-8-sig"))
    scenarios = {}
    covered = set()
    for entry in entries:
        slug = entry["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in scenarios:
            raise ValueError(f"场景 ID 重复或无效：{slug}")
        if not all(entry[key].strip() for key in ("title", "input", "output", "group")):
            raise ValueError(f"场景说明不完整：{slug}")
        local = set()
        for step in entry["skills"]:
            name = step["name"]
            if name not in skills or name in local:
                raise ValueError(f"{slug} 引用了未知或重复技能：{name}")
            if not step["when"].strip() or not step["result"].strip():
                raise ValueError(f"{slug}/{name} 缺少适用条件或产物")
            local.add(name)
        if not local:
            raise ValueError(f"场景没有技能入口：{slug}")
        covered.update(local)
        scenarios[slug] = entry
    missing = skills.keys() - covered
    if missing:
        raise ValueError("未覆盖的技能：" + "、".join(sorted(missing)))
    for slug, entry in scenarios.items():
        destinations = entry["next"]
        if not isinstance(destinations, list) or len(set(destinations)) != len(destinations):
            raise ValueError(f"{slug} 的下一场景清单无效")
        if any(target == slug or target not in scenarios for target in destinations):
            raise ValueError(f"{slug} 引用了自身或不存在的下一场景")
    return skills, scenarios


def scene_link(scene):
    return f"[{scene['title']}]({scene['id']}.md)"


def diagram_exists(output_dir, slug):
    # 图源、交互图与预览图应一起更新，避免漏发整组产物。
    html, svg = (output_dir / f"{slug}.{ext}" for ext in ("html", "svg"))
    source = output_dir.parents[1] / "atlas/sources" / f"{slug}.json"
    present = [path.is_file() for path in (source, html, svg)]
    if any(present) and not all(present):
        raise ValueError(f"{slug} 的 Archify 图源、HTML 或 SVG 不完整")
    if html.is_file() and (not html.stat().st_size or not svg.stat().st_size):
        raise ValueError(f"{slug} 的图形文件为空")
    return html.is_file()


def render_scene(root, scene, scenarios, skills, has_diagram):
    slug = scene["id"]
    lines = [f"# {scene['title']}", "", f"[返回场景目录](README.md) · {scene['group']}", "",
             f"**已有材料**　{scene['input']}", "", f"**结束产物**　{scene['output']}", ""]
    if has_diagram:
        lines += [f"![{scene['title']}]({slug}.svg)", "",
                  f"[打开交互图]({PAGES_BASE}/{slug}.html) · [查看原尺寸 SVG]({slug}.svg)", ""]
    lines += ["## 技能怎么用", "", "| 技能 | 何时使用 | 得到什么 |", "|---|---|---|"]
    runtimes = []
    for step in scene["skills"]:
        name = step["name"]
        skill = skills[name]
        if skill["status"] == "files":
            path = Path(skill["path"])
            if path.name != "SKILL.md":
                path = path / "SKILL.md"
        else:
            path = Path(skill["path"] or "docs/RESTORE.md")
            runtimes.append(f"- **{name}**　{skill['runtime']}")
        source = (root / path).resolve(strict=True)
        if not source.is_relative_to(root) or not source.is_file():
            raise ValueError(f"{name} 的文档未指向仓库内文件：{path}")
        link = "../../" + quote(path.as_posix(), safe="/._-@")
        condition, result = (step[key].replace("|", "\\|") for key in ("when", "result"))
        lines.append(f"| [{name}]({link}) | {condition} | {result} |")
    if runtimes:
        lines += ["", "### 应用运行条件", "",
                  "在提供相应能力的 Codex 环境中使用这些入口。安装与连接要求见[应用恢复说明](../RESTORE.md)。",
                  "", *runtimes]
    if scene["next"]:
        lines += ["", "## 可以接着做", ""]
        for target in scene["next"]:
            next_scene = scenarios[target]
            lines.append(f"- {scene_link(next_scene)}　从「{next_scene['input']}」开始。")
    return "\n".join(lines) + "\n"


def render_catalog(scenarios, diagrams):
    groups = defaultdict(list)
    for scene in scenarios.values():
        groups[scene["group"]].append(scene)
    lines = ["# 按场景查找技能", "",
             f"从手里的材料选择入口。共 {len(scenarios)} 个场景，覆盖 {EXPECTED_SKILL_COUNT} 项技能。"
             "标有「附图」的场景提供静态预览与可交互的横向流程图。", "",
             "[查看全部技能及原始说明](../../README.md)", ""]
    for group, entries in groups.items():
        lines += [f"## {group}", ""]
        for scene in entries:
            mark = "　**附图**" if scene["id"] in diagrams else ""
            names = "、".join(f"`{step['name']}`" for step in scene["skills"])
            lines += [f"- **{scene_link(scene)}**{mark}<br>",
                      f"  {scene['input']} → {scene['output']}<br>",
                      f"  {names}"]
            if scene["next"]:
                links = " · ".join(scene_link(scenarios[key]) for key in scene["next"])
                lines[-1] += "<br>"
                lines.append(f"  后续可选　{links}")
        lines.append("")
    return "\n".join(lines)


def render_pages_index(scenarios, diagrams):
    groups = defaultdict(list)
    for slug, scene in scenarios.items():
        if slug in diagrams:
            groups[scene["group"]].append(scene)
    lines = ['''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>技能场景图</title>
  <style>
    :root { color-scheme:light dark; --paper:#f7f9fc; --card:#fff; --ink:#17232d; --muted:#475c69; --line:#c7d5dc; --link:#006172 }
    @media (prefers-color-scheme:dark) {
      :root { --paper:#10181d; --card:#182329; --ink:#e8f0f4; --muted:#bed0da; --line:#42535c; --link:#74d4dd }
    }
    * { box-sizing:border-box }
    body { margin:0; background:var(--paper); color:var(--ink); font:1rem/1.65 Inter,"Microsoft YaHei",sans-serif }
    main { max-width:75rem; margin:auto; padding:clamp(1.25rem,5vw,4rem) }
    header { display:flex; flex-wrap:wrap; gap:.6rem 1.5rem; align-items:baseline; justify-content:space-between; padding-bottom:1rem; border-bottom:2px solid var(--link) }
    h1,h2,h3,p { margin:0 }
    h1 { font-size:clamp(2rem,5vw,3.75rem); line-height:1.2 }
    h2 { font-size:1.35rem; margin:2rem 0 1rem }
    a { color:var(--link); text-underline-offset:.2em }
    a:focus-visible { outline:3px solid var(--link); outline-offset:3px }
    ul { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(24rem,100%),1fr)); gap:1rem; list-style:none; padding:0; margin:0 }
    nav { display:flex; flex-wrap:wrap; gap:.5rem 1rem; margin:1rem 0 }
    li { background:var(--card); border:1px solid var(--line); border-radius:.55rem; padding:1rem }
    li:focus-within,li:hover { border-color:var(--link) }
    li a:first-child { display:block; text-decoration:none }
    li .usage { display:inline-block; font-size:.9rem; margin-top:.65rem }
    img { display:block; width:100%; height:auto; aspect-ratio:2.5; object-fit:contain; margin-bottom:.7rem }
    h3 { font-size:1.05rem }
    li p { margin-top:.3rem; color:var(--muted); font-size:.9rem }
  </style>
</head>
<body>
<main>
  <header><h1>技能场景图</h1>''',
             f'  <a href="{REPOSITORY_URL}/blob/main/docs/atlas/README.md">在 GitHub 查看全部 {len(scenarios)} 个场景</a></header>']
    lines.append('  <nav aria-label="工作流">' + " ".join(
        f'<a href="#group-{number}">{escape(group)}</a>'
        for number, group in enumerate(groups, 1)
    ) + '</nav>')
    for number, (group, scenes) in enumerate(groups.items(), 1):
        lines += [f'  <section id="group-{number}"><h2>{escape(group)}</h2>', "    <ul>"]
        for scene in scenes:
            slug = scene["id"]
            lines += [f'      <li><a href="atlas/{slug}.html">',
                      f'        <img src="atlas/{slug}.svg" alt="" loading="lazy" decoding="async">',
                      f'        <h3>{escape(scene["title"])}</h3>',
                      f'        <p>{escape(scene["input"])} → {escape(scene["output"])}</p>',
                      '      </a>',
                      f'      <a class="usage" href="{REPOSITORY_URL}/blob/main/docs/atlas/{slug}.md">技能用法与后续场景</a></li>']
        lines += ["    </ul>", "  </section>"]
    lines += ["</main>", "</body>", "</html>", ""]
    return "\n".join(lines)


def generate(root):
    skills, scenarios = load_scenarios(root)
    output_dir = root / "docs/atlas"
    diagrams = {slug for slug in scenarios if diagram_exists(output_dir, slug)}
    documents = {
        output_dir / f"{slug}.md": render_scene(root, scene, scenarios, skills, slug in diagrams)
        for slug, scene in scenarios.items()
    }
    documents[output_dir / "README.md"] = render_catalog(scenarios, diagrams)
    documents[root / "docs/index.html"] = render_pages_index(scenarios, diagrams)
    # 发布原始文件，防止 Jekyll 将同名 .md 转成 .html 覆盖交互图。
    documents[root / "docs/.nojekyll"] = ""
    return documents, len(scenarios)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="更新场景页和导航")
    mode.add_argument("--check", action="store_true", help="检查清单覆盖和生成内容（默认）")
    args = parser.parse_args()
    try:
        # 先核对完整清单，再更新有变化的导航页和发布标记。
        documents, scene_count = generate(ROOT)
        stale = [path for path, text in documents.items()
                 if not path.is_file() or path.read_text(encoding="utf-8") != text]
        if args.write:
            (ROOT / "docs/atlas").mkdir(parents=True, exist_ok=True)
            for path in stale:
                path.write_text(documents[path], encoding="utf-8", newline="\n")
        elif stale:
            raise ValueError("请先运行 --write 更新：" + "、".join(path.name for path in stale))
        print(f"场景导航已核对：{scene_count} 个场景，{EXPECTED_SKILL_COUNT} 项技能")
    except (KeyError, TypeError, ValueError, OSError) as error:
        print(f"场景导航校验失败：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
