# 维护场景图

读图从[场景目录](../docs/atlas/README.md)进入。这里保存导航数据和可编辑的 Archify 图源。

- [技能目录](../skill-catalog.json)定义技能名、原始路径和运行环境。[场景清单](scenarios.json)记录真实起点、所需技能、交付物与可选后续场景。引用技能时使用目录里的调用名。
- 每张图的 JSON 在 [sources](sources/)。主路径写明交接材料；可以替代的技能使用独立入口或选择分支。证据引用对应版本的技能说明，应用提供的能力链接到[恢复说明](../docs/RESTORE.md)。
- 从仓库根目录运行 Archify 的 `finalize workflow`，传入图源和其中声明的 HTML 输出路径，并带上 `--repo-root . --quality showcase --json`。用 Viewer 的「导出 → SVG（自动主题）」保存同名 SVG，检查浅色和深色下的中文、箭头与分支。校验与截图回执保存在本地。
- 图和导航准备好后，从仓库根目录生成目录页并复查：

  ```shell
  python -B -X utf8 tools/build_atlas.py --write
  python -B -X utf8 tools/build_index.py --write
  python -B -X utf8 tools/build_atlas.py --check
  python -B -X utf8 tools/build_index.py --check
  ```

GitHub 仓库渲染 Markdown 与 SVG。GitHub Pages 从 `main` 的 `/docs` 发布已生成的 HTML；Pages 首页只链接到具备 HTML 和 SVG 的场景。
