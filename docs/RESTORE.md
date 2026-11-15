# 技能恢复说明

本快照登记 81 个技能，其中 67 个包含原始技能文件，14 个应用附带技能仅保留清单。仓库没有包含账号、令牌、SSH 私钥、应用安装包、Python/Node.js 依赖环境或在线连接状态。

## 包含原文件的 67 项

| 来源 | 数量 | 位置 | 恢复方式 |
|---|---:|---|---|
| 中央技能库 | 47 | 仓库根目录各技能文件夹 | 沿用 Skills Manager 导入/恢复方式；保留 profile、scripts 公共资源与原有相对目录关系 |
| 个人 FDE | 1 | external-skills/local/fde-creator | 恢复完整目录到个人技能目录 |
| Apache-2.0 系统技能 | 4 | external-skills/codex-system | 优先由 Codex 更新/恢复；手动恢复时保留许可证及所有支持文件 |
| Superpowers 7.0.2 | 15 | external-skills/superpowers | 按包内安装文档恢复完整结构；保留 skills、scripts、hooks 等相对位置 |

恢复现有目录前先备份并比较。以下是仅在目标不存在时恢复个人 FDE 的 Windows 示例，命令从本仓库根目录运行：

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills\fde-creator'
if (Test-Path -LiteralPath $target) { throw '目标已存在，请先备份和比较。' }
Copy-Item -LiteralPath '.\external-skills\local\fde-creator' -Destination $target -Recurse
```

本仓库不备份 .git 元数据；Superpowers 的版本来自其 package.json。通过备份恢复后若需要官方 Git 更新流程，应按包内官方安装说明重新建立上游仓库关系，而不是把本仓库当作 Superpowers 上游。

## 仅登记清单的 14 项

以下材料没有上传原始 SKILL.md、脚本、图标或资源。documents 的附带许可证明确限制复制与第三方分发；其他这些应用材料未确认公开再分发授权，因此统一由原应用恢复。它们需要相应应用、插件运行时和连接工具；从 Git 克隆本仓库不会自动恢复这些能力。

| 技能 | 中文用途 | 来源 | 恢复方式 |
|---|---|---|---|
| `computer-use` | 通过当前可用的电脑操作工具读取和控制 Windows 应用、浏览器界面。 | Codex 应用插件：openai-bundled/computer-use/26.1111.21308 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `create-rule` | 创建 Cursor 项目规则和持久化编码约定。 | Cursor 应用内置技能 | 安装或更新 Cursor，由应用提供对应内置技能 |
| `create-skill` | 创建适合 Cursor 调用的技能。 | Cursor 应用内置技能 | 安装或更新 Cursor，由应用提供对应内置技能 |
| `create-subagent` | 创建 Cursor 的专用子代理。 | Cursor 应用内置技能 | 安装或更新 Cursor，由应用提供对应内置技能 |
| `documents` | 创建、编辑、批注和修订 Word/DOCX，并渲染检查排版。 | Codex 应用插件：openai-primary-runtime/documents/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `excel-live-control` | 通过已连接的 Excel 会话，直接操作打开的工作簿。 | Codex 应用插件：openai-primary-runtime/spreadsheets/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `migrate-to-skills` | 把 Cursor 的旧规则和斜杠命令迁移为技能。 | Cursor 应用内置技能 | 安装或更新 Cursor，由应用提供对应内置技能 |
| `pdf` | 读取、生成、渲染和检查 PDF，包括表单与版面。 | Codex 应用插件：openai-primary-runtime/pdf/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `Presentations` | 通过当前运行时和演示文稿工具创建、编辑 PowerPoint 或 Google Slides。 | Codex 应用插件：openai-primary-runtime/presentations/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `review-agent` | 供其他代理委派的只读代码缺陷审查入口。 | Codex 应用内置系统技能 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `Spreadsheets` | 读取、创建、分析和修改 Excel、CSV、TSV 或 Google Sheets，处理公式、表格和图表。 | Codex 应用插件：openai-primary-runtime/spreadsheets/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `template-creator` | 把用户认可的产物和流程整理为可复用的个人模板技能。 | Codex 应用插件：openai-primary-runtime/template-creator/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `update-cursor-settings` | 修改 Cursor/VS Code 的用户设置。 | Cursor 应用内置技能 | 安装或更新 Cursor，由应用提供对应内置技能 |
| `visualize` | 在对话中制作交互可视化、解释工具和可操作的小型模型。 | Codex 应用插件：openai-bundled/visualize/1.0.97 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |

恢复完成后开启新会话核对技能是否加载，再按各技能实际任务验证。Excel 连接、电脑控制、文档渲染等功能依赖应用提供的工具或运行时；恢复说明不承诺旧插件版本可以脱离原应用独立运行。

## 文件校验与许可

backup-manifest.json 记录本次仓库提交中文件的 SHA-256 摘要。Git 可能按文本规则规范换行；若工作副本与摘要不同，请先检查换行设置，或核对 Git 提交中保存的文件内容。

每份技能适用原来源的许可证；本仓库不替第三方材料授予额外权限。原有中央库内容保留既有许可证，新增 Apache-2.0 系统技能和 MIT Superpowers 均随附原许可证。
