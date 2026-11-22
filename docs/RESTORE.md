# Codex 技能安装与恢复说明

本目录汇总 69 个 Codex 技能，其中 65 个包含技能文件，4 个依赖应用提供，仅登记使用清单。本仓库没有包含账号、令牌、SSH 私钥、应用安装包、Python/Node.js 依赖环境或在线连接状态。

## 包含技能文件的 65 项

| 来源 | 数量 | 位置 | 安装与恢复方式 |
|---|---:|---|---|
| 中央技能库 | 45 | 仓库根目录各技能文件夹 | 使用 Skills Manager 导入并按需部署到 Codex；保留 profile、scripts 公共资源与相对目录关系 |
| 个人技能 | 2 | external-skills/local 下的 fde-creator、skill-upstream-sync | 将所需技能的完整目录恢复到 Codex 个人技能目录 |
| Apache-2.0 系统技能 | 3 | external-skills/codex-system | 优先由 Codex 更新或恢复；手动恢复时保留许可证及所有支持文件 |
| Superpowers 7.0.2 | 15 | external-skills/superpowers | 按包内安装文档恢复完整结构；保留 skills、scripts、hooks 等相对位置 |

同一技能在多个工具中的分发链接不重复计数。不要把整个 external-skills 目录无差别复制到一个技能目录；技能之间及其与公共脚本之间的相对路径应保持有效。

恢复现有目录前先备份并比较。以下是仅在目标不存在时恢复个人 FDE 的 Windows 示例，从本仓库根目录运行：

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills\fde-creator'
if (Test-Path -LiteralPath $target) { throw '目标已存在，请先备份和比较。' }
Copy-Item -LiteralPath '.\external-skills\local\fde-creator' -Destination $target -Recurse
```

本仓库不备份 .git 元数据；Superpowers 的版本来自其 package.json。通过本仓库恢复后如需官方 Git 更新流程，应按包内官方安装说明重新建立上游仓库关系，而不是把本仓库当作 Superpowers 上游。

## 三个 Codex 适配技能

| 技能 | 使用范围 |
|---|---|
| codex-project-rules | 维护项目、目录或个人 AGENTS.md，保留作用域，不创建其他工具专用规则格式 |
| codex-agent-config | 生成、检查和更新 Codex 代理 TOML；默认继承模型与权限，不修改父会话权限 |
| migrate-to-codex | 将持久规则与可复用工作流分别迁入 AGENTS.md 和 Codex 技能；默认保留原件，报告重名冲突 |

技能创建统一使用已有 skill-creator，不额外安装重复创建入口。安装上述三个技能本身不会修改当前模型、权限、MCP、代理定义或项目规则；只有后续用户请求具体任务时，才在其授权范围内修改对应文件。

需要在已安装 Skills Manager 的 Windows 环境中导入这三个技能时，可从本仓库根目录执行以下命令。目标已存在时应先比较，避免重复登记；只向 Codex 部署，不使用自动同步全部工具的选项。

```powershell
$manager = Join-Path $env:USERPROFILE '.skills-manager\bin\skills-manager-cli.exe'
$skillNames = @('codex-project-rules', 'codex-agent-config', 'migrate-to-codex')
foreach ($skillName in $skillNames) {
    & $manager skills install --local (Join-Path $PWD.Path $skillName)
    if ($LASTEXITCODE -ne 0) { throw "导入失败：$skillName" }
}
& $manager skills deploy --agent codex @skillNames
if ($LASTEXITCODE -ne 0) { throw 'Codex 部署失败' }
```

重新开启 Codex 会话核对技能是否加载，再按 SKILL.md 的说明使用。项目专用技能应放在目标项目支持的技能目录中，不应把个人配置和凭据写入公共仓库。

## 依赖应用恢复的 4 项

以下材料没有上传原始 SKILL.md、脚本、图标或资源。这些应用材料通过原应用恢复。它们需要相应应用、插件运行时和连接工具；从 Git 克隆本仓库不会自动恢复这些能力。

| 技能 | 中文用途 | 来源 | 恢复方式 |
|---|---|---|---|
| `Presentations` | 通过当前运行时和演示文稿工具创建、编辑 PowerPoint 或 Google Slides。 | Codex 应用插件：openai-primary-runtime/presentations/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `review-agent` | 供其他代理委派的只读代码缺陷审查入口。 | Codex 应用内置系统技能 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `Spreadsheets` | 读取、创建、分析和修改 Excel、CSV、TSV 或 Google Sheets，处理公式、表格和图表。 | Codex 应用插件：openai-primary-runtime/spreadsheets/26.1112.11217 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |
| `visualize` | 在对话中制作交互可视化、解释工具和可操作的小型模型。 | Codex 应用插件：openai-bundled/visualize/1.0.97 | 安装或更新 Codex，并在原应用中恢复对应系统技能或插件 |

恢复完成后开启新会话核对技能是否加载，再按实际任务验证。在线表格、演示和交互可视化等功能依赖应用提供的工具或运行时；恢复说明不承诺旧插件版本可以脱离原应用独立运行。

## 文件校验与许可

技能名称、中文用途与路径以 skill-catalog.json 为准。维护清单后，从仓库根运行以下命令；生成器只使用 Python 标准库，并检查重复名称、已替换入口、数量及相对链接：

```powershell
python -B -X utf8 tools/build_index.py --check
# 确认清单修改后重新生成两列 README，再复核差异。
python -B -X utf8 tools/build_index.py --write
```

backup-manifest.json 记录本次仓库提交中文件的 SHA-256 摘要。Git 可能按文本规则规范换行；若工作副本与摘要不同，先检查换行设置，或核对 Git 提交中保存的文件内容。

每份技能适用原来源的许可证和使用条款；本仓库不替第三方材料授予额外权限，也不将全部内容统一声明为 MIT 或其他单一许可证。保留已有 LICENSE、LICENSE.txt、NOTICE 及其他归属说明。Apache-2.0 系统技能和 MIT Superpowers 随附各自许可证。

未确认可公开再分发的应用材料以清单和官方应用恢复说明代替原文件上传。清单登记不代表授予其复制、分发或再许可权利。
