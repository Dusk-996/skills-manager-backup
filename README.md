# 本机技能备份与中文索引

快照日期：2026-11-15。目标仓库：[skills-manager-backup](https://github.com/Dusk-996/skills-manager-backup)。

本次逐项登记 **81 个技能**：**67 个已备份原文件**，**14 个仅登记清单**。统计按实际技能去重，同一个技能的多工具分发链接不重复计数。

标记为“仅登记清单”的技能没有上传其原始指令、脚本或资源，不能视为完整原文件备份。具体以逐项表格中的备份状态为准，恢复时需从相应应用或官方来源重新安装。

原有 **47 个中央技能**继续保留在仓库根目录，路径不变；附加技能及其支持资源归档于 `external-skills/`，按来源保留目录关系。`profile/` 和 `scripts/` 是中央库公共资源，不另计为技能。

本仓库备份技能文件与用途索引；Codex、Cursor、插件连接、电脑控制工具和应用运行时需要在目标环境中另行安装或启用。仅复制文件不会自动恢复这些工具能力。

## 来源统计

| 来源 | 技能数量 |
|---|---:|
| 中央技能库 | 47 |
| Superpowers | 15 |
| 应用挂载插件 | 8 |
| Cursor 内置技能 | 5 |
| 个人本地技能 | 1 |
| Codex 系统技能 | 5 |

## 全部技能名称与作用

“已备份原文件”表示该项原文件已纳入本次备份；“仅登记清单”表示只列名称、用途和来源。表中的仓库路径用于查找对应备份或清单位置。

| 技能名称 | 中文用途 | 来源 | 备份状态 | 仓库路径 |
|---|---|---|---|---|
| `aliyun-asr` | 调用阿里云录音文件识别闲时版，把批量音视频 URL 转成文字和结构化结果。 | 中央技能库 | 已备份原文件 | [aliyun-asr](aliyun-asr) |
| `archify` | 生成可交互的独立 HTML 架构图、流程图、时序图、数据流和生命周期图。 | 中央技能库 | 已备份原文件 | [archify](archify) |
| `baoyu-infographic` | 把内容整理为信息图，选择版式和视觉风格。 | 中央技能库 | 已备份原文件 | [baoyu-infographic](baoyu-infographic) |
| `baoyu-markdown-to-html` | 把 Markdown 转成带主题样式的 HTML，适配微信公众号并支持代码、公式等。 | 中央技能库 | 已备份原文件 | [baoyu-markdown-to-html](baoyu-markdown-to-html) |
| `brainstorming` | 编码前澄清需求、比较方案并形成设计；属于 Superpowers 通用流程。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/brainstorming](external-skills/superpowers/skills/brainstorming) |
| `code-review` | 按仓库规范和原始需求两个维度审查某个基点之后的代码变更。 | 中央技能库 | 已备份原文件 | [code-review](code-review) |
| `codebase-design` | 设计模块接口、依赖边界和可测试性，建立“深模块”等共享设计词汇。 | 中央技能库 | 已备份原文件 | [codebase-design](codebase-design) |
| `computer-use` | 通过当前可用的电脑操作工具读取和控制 Windows 应用、浏览器界面。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `create-rule` | 创建 Cursor 项目规则和持久化编码约定。 | Cursor 内置技能 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `create-skill` | 创建适合 Cursor 调用的技能。 | Cursor 内置技能 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `create-subagent` | 创建 Cursor 的专用子代理。 | Cursor 内置技能 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `darwin-skill` | 按结构和效果评分，迭代优化 SKILL.md，并验证优化结果。 | 中央技能库 | 已备份原文件 | [darwin-skill](darwin-skill) |
| `deployment-packager` | 生成 Dockerfile、Compose、K8s、systemd、Nginx 配置及部署、验证、回滚文档。 | 中央技能库 | 已备份原文件 | [deployment-packager-2](deployment-packager-2) |
| `design-taste-frontend` | 为落地页、作品集和改版选择视觉方向，避免套模板式页面。 | 中央技能库 | 已备份原文件 | [design-taste-frontend](design-taste-frontend) |
| `devops-brainstorming` | 把运维需求整理为可实现设计，澄清边界、运行约束与风险。 | 中央技能库 | 已备份原文件 | [devops-brainstorming](devops-brainstorming) |
| `devops-production-hardening` | 给现有脚本、服务和部署补健康检查、日志、安全配置、备份及回滚。 | 中央技能库 | 已备份原文件 | [devops-production-hardening](devops-production-hardening) |
| `devops-requesting-code-review` | 从运维实现、计划和生产约束等角度组织代码审查。 | 中央技能库 | 已备份原文件 | [devops-requesting-code-review](devops-requesting-code-review) |
| `devops-skill-router-zh` | 面向中文运维任务选择最相关的 1～3 个技能。 | 中央技能库 | 已备份原文件 | [devops-skill-router-zh](devops-skill-router-zh) |
| `devops-writing-plans` | 把已明确的需求拆为 DevOps 实施任务、验证步骤和交付计划。 | 中央技能库 | 已备份原文件 | [devops-writing-plans](devops-writing-plans) |
| `diagnosing-bugs` | 对难复现故障、异常和性能回退循环提出假设、采集证据、定位根因。 | 中央技能库 | 已备份原文件 | [diagnosing-bugs](diagnosing-bugs) |
| `diagnosing-superpowers` | 读取会话记录，用证据解释 Superpowers 工作流失误、重复劳动、耗时或技能未触发等问题。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/diagnosing-superpowers](external-skills/superpowers/skills/diagnosing-superpowers) |
| `dispatching-parallel-agents` | 判断哪些独立任务适合并行分派代理。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/dispatching-parallel-agents](external-skills/superpowers/skills/dispatching-parallel-agents) |
| `documents` | 创建、编辑、批注和修订 Word/DOCX，并渲染检查排版。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `domain-modeling` | 维护项目领域术语、领域模型和架构决策记录。 | 中央技能库 | 已备份原文件 | [domain-modeling](domain-modeling) |
| `draw-io-diagram-generator` | 生成和修改可继续编辑的 draw.io 图，包括架构、拓扑、流程、ER 和 UML 图。 | 中央技能库 | 已备份原文件 | [draw-io-diagram-generator](draw-io-diagram-generator) |
| `excel-live-control` | 通过已连接的 Excel 会话，直接操作打开的工作簿。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `executing-plans` | 按已写好的计划执行，并在检查点核对结果。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/executing-plans](external-skills/superpowers/skills/executing-plans) |
| `fde-creator` | 解释 FDE 课程、章节重点、相关代码和学习问题，不直接代写作业。 | 个人本地技能 | 已备份原文件 | [external-skills/local/fde-creator](external-skills/local/fde-creator) |
| `find-skills` | 发现可安装的第三方技能，按任务寻找扩展能力。 | 中央技能库 | 已备份原文件 | [find-skills](find-skills) |
| `finishing-a-development-branch` | 实现完成后处理合并、PR、工作树清理和交付方式。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/finishing-a-development-branch](external-skills/superpowers/skills/finishing-a-development-branch) |
| `frontend-design` | 按新版 Anthropic 指令设计和实现页面与组件；ECC 工程检查表作为按需参考。 | 中央技能库 | 已备份原文件 | [frontend-design](frontend-design) |
| `frontend-slides` | 创建带动画的 HTML 演示稿，或把 PPT 内容转换为网页演示。 | 中央技能库 | 已备份原文件 | [frontend-slides](frontend-slides) |
| `github-weekly-feishu` | 整理当期 GitHub 热门项目，生成适合飞书阅读的中文技术周报和配图需求。 | 中央技能库 | 已备份原文件 | [github-weekly-feishu](github-weekly-feishu) |
| `grafana-dashboards` | 设计 Grafana 监控看板，覆盖基础设施、接口、数据库等指标和面板。 | 中央技能库 | 已备份原文件 | [grafana-dashboards](grafana-dashboards) |
| `grilling` | 逐项追问方案假设、取舍和风险；需要同步术语或 ADR 时搭配 domain-modeling。 | 中央技能库 | 已备份原文件 | [grilling](grilling) |
| `handoff` | 把当前会话整理为供下一位代理继续工作的交接文档。 | 中央技能库 | 已备份原文件 | [handoff](handoff) |
| `html-to-mui-react` | 把批准的 HTML 原型保真转换为 Vite、React、TypeScript、MUI 和 Mock 工程。 | 中央技能库 | 已备份原文件 | [html-to-mui-react](html-to-mui-react) |
| `humanizer-zh` | 润色中文，减少空泛表述、夸张语气、机械排比等常见 AI 文风。 | 中央技能库 | 已备份原文件 | [humanizer-zh](humanizer-zh) |
| `imagegen` | 生成或编辑照片、插画、贴图、透明素材等位图。 | Codex 系统技能 | 已备份原文件 | [external-skills/codex-system/imagegen](external-skills/codex-system/imagegen) |
| `k8s-troubleshoot` | 按 Pod、Service、Ingress、公网访问四层排查 Kubernetes 故障。 | 中央技能库 | 已备份原文件 | [k8s-troubleshoot](k8s-troubleshoot) |
| `learning-notes-builder` | 把已经收集的文本、网页和课程资料整理为结构化中文 Markdown 学习笔记。 | 中央技能库 | 已备份原文件 | [learning-notes-builder](learning-notes-builder) |
| `learning-roadmap` | 把学习笔记转成交互 HTML 路线图，支持进度和知识详情。 | 中央技能库 | 已备份原文件 | [learning-roadmap](learning-roadmap) |
| `migrate-to-skills` | 把 Cursor 的旧规则和斜杠命令迁移为技能。 | Cursor 内置技能 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `openai-docs` | 为 OpenAI API 入门及 Codex/Work 的用法、配置和行为提供官方资料入口。 | Codex 系统技能 | 已备份原文件 | [external-skills/codex-system/openai-docs](external-skills/codex-system/openai-docs) |
| `ops-readiness-review` | 上线前检查危险操作、鉴权、Secret、任务可靠性、观测性和恢复能力，给出就绪结论。 | 中央技能库 | 已备份原文件 | [ops-readiness-review](ops-readiness-review) |
| `pdf` | 读取、生成、渲染和检查 PDF，包括表单与版面。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `playwright-cli` | 使用 Playwright CLI 操作浏览器、检查网页并执行交互。 | 中央技能库 | 已备份原文件 | [playwright-cli](playwright-cli) |
| `playwright-e2e-debug-report` | 按用户明确要求制定、执行浏览器 E2E/冒烟/回归测试，分流问题并输出报告。 | 中央技能库 | 已备份原文件 | [playwright-e2e-debug-report](playwright-e2e-debug-report) |
| `pptx` | 读取、修改、合并、生成和验证 PowerPoint 文件，包含脚本和模板处理。 | 中央技能库 | 已备份原文件 | [pptx](pptx) |
| `Presentations` | 通过当前运行时和演示文稿工具创建、编辑 PowerPoint 或 Google Slides。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `project-init` | 初始化 Shell、Python、Go 运维项目，包含生产谨慎的目录、配置、日志与部署约定。 | 中央技能库 | 已备份原文件 | [project-init](project-init) |
| `project-to-open-slide` | 把本地项目、文档和网页材料转为中文 Open Slide 演示及图片型 PPTX。 | 中央技能库 | 已备份原文件 | [project-to-open-slide](project-to-open-slide) |
| `prototype-parity-review` | 比较已批准 HTML 原型与 React Mock 的视觉、布局和交互一致性。 | 中央技能库 | 已备份原文件 | [prototype-parity-review](prototype-parity-review) |
| `question-gap-analyzer` | 结合 Roadmap、岗位和已有题库，分析普通面试题、场景题的覆盖缺口。 | 中央技能库 | 已备份原文件 | [question-gap-analyzer](question-gap-analyzer) |
| `receiving-code-review` | 核查评审意见是否成立，再落实修改和验证。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/receiving-code-review](external-skills/superpowers/skills/receiving-code-review) |
| `requesting-code-review` | 在任务或较大功能完成后组织通用代码审查。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/requesting-code-review](external-skills/superpowers/skills/requesting-code-review) |
| `review-agent` | 供其他代理委派的只读代码缺陷审查入口。 | Codex 系统技能 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `scenario-question-designer` | 从知识点和生产经验设计场景面试题，先出题目简报再完善。 | 中央技能库 | 已备份原文件 | [scenario-question-designer](scenario-question-designer) |
| `setup-matt-pocock-skills` | 初始化工程技能依赖的 Issue 跟踪器、标签和领域文档约定。 | 中央技能库 | 已备份原文件 | [setup-matt-pocock-skills](setup-matt-pocock-skills) |
| `skill-creator` | 创建或更新 Codex 技能，整理触发条件、指令和配套资源。 | Codex 系统技能 | 已备份原文件 | [external-skills/codex-system/skill-creator](external-skills/codex-system/skill-creator) |
| `skill-installer` | 从指定 GitHub 仓库或 OpenAI 技能目录安装技能。 | Codex 系统技能 | 已备份原文件 | [external-skills/codex-system/skill-installer](external-skills/codex-system/skill-installer) |
| `skill-router-zh` | 按中文场景为文档、前端、运维、图像等任务选择技能。 | 中央技能库 | 已备份原文件 | [skill-router-zh](skill-router-zh) |
| `Spreadsheets` | 读取、创建、分析和修改 Excel、CSV、TSV 或 Google Sheets，处理公式、表格和图表。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `ssh-remote-ops` | 通过 SSH 巡检 Linux 主机，分析进程、日志、网络和磁盘；按授权执行受控变更。 | 中央技能库 | 已备份原文件 | [ssh-remote-ops](ssh-remote-ops) |
| `stack-selector` | 从 React Mock 和运行约束推导后端、Worker、Agent 等组件及技术栈，输出选型确认单。 | 中央技能库 | 已备份原文件 | [stack-selector](stack-selector) |
| `subagent-driven-development` | 按计划分派实现和审查子任务，适用于授权使用子代理的开发工作。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/subagent-driven-development](external-skills/superpowers/skills/subagent-driven-development) |
| `systematic-debugging` | 通用系统化排障流程：先调查根因，再验证假设和修复。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/systematic-debugging](external-skills/superpowers/skills/systematic-debugging) |
| `tdd` | 另一套测试驱动开发指引，强调集成测试及按行为推进的实现过程。 | 中央技能库 | 已备份原文件 | [tdd](tdd) |
| `teach` | 在工作区内维护学习目标、课程状态和跨会话教学记录。 | 中央技能库 | 已备份原文件 | [teach](teach) |
| `template-creator` | 把用户认可的产物和流程整理为可复用的个人模板技能。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `test-driven-development` | 按先失败测试、再实现、再重构的顺序开发功能和修复。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/test-driven-development](external-skills/superpowers/skills/test-driven-development) |
| `to-spec` | 把已有讨论整理为需求规格，并发布到已配置的项目跟踪器。 | 中央技能库 | 已备份原文件 | [to-spec](to-spec) |
| `to-tickets` | 把计划或规格拆为带阻塞关系的纵向开发任务。 | 中央技能库 | 已备份原文件 | [to-tickets](to-tickets) |
| `ui-ux-pro-max` | 按产品类型检索界面风格、配色、字体、交互和图表设计建议。 | 中央技能库 | 已备份原文件 | [ui-ux-pro-max](ui-ux-pro-max) |
| `update-cursor-settings` | 修改 Cursor/VS Code 的用户设置。 | Cursor 内置技能 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `using-git-worktrees` | 为需要隔离的开发任务创建和使用 Git worktree。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/using-git-worktrees](external-skills/superpowers/skills/using-git-worktrees) |
| `using-superpowers` | Superpowers 的总入口，规定技能发现、调用顺序和平台工具映射。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/using-superpowers](external-skills/superpowers/skills/using-superpowers) |
| `verification-before-completion` | 在声称完成、修复或通过前，要求运行验证并以实际输出为依据。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/verification-before-completion](external-skills/superpowers/skills/verification-before-completion) |
| `visualize` | 在对话中制作交互可视化、解释工具和可操作的小型模型。 | 应用挂载插件 | 仅登记清单；未上传原文件 | docs/RESTORE.md |
| `writing-plans` | 把设计写成可以逐项执行的实现计划。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/writing-plans](external-skills/superpowers/skills/writing-plans) |
| `writing-skills` | 按 Superpowers 流程编写、验证和测试技能文档。 | Superpowers | 已备份原文件 | [external-skills/superpowers/skills/writing-skills](external-skills/superpowers/skills/writing-skills) |

## 恢复与使用

1. 克隆仓库，先按上表确认目标技能是否包含原文件，再读取其 `SKILL.md` 和来源说明。
2. 个人技能只恢复到目标工具支持的个人技能目录。已有同名内容时，先备份并比较，再决定是否替换。中央库根路径与公共 `profile/`、`scripts/` 应保持相对目录关系。
3. Superpowers 的技能之间存在相对引用；恢复时保留其技能目录、公共支持文件和原有层级。应用挂载插件也应保持原包的 `skills/`、`docs/`、`assets/` 等目录关系。
4. Codex 系统技能、Cursor 内置技能和应用插件优先由对应应用或官方安装器恢复。不要将整个 `external-skills/` 无差别复制到一个个人技能目录。
5. 重新安装各技能实际需要的 Shell、Python、Node.js、渲染工具或插件连接，再按技能说明做最小验证；本快照不等于运行环境或凭据备份。

## 许可证与来源

不同技能适用各自来源的许可证和使用条款。保留已有 `LICENSE`、`LICENSE.txt`、`NOTICE` 及其他归属说明；本仓库不将全部内容统一声明为 MIT 或其他单一许可证。

对尚未确认可公开再分发的随应用材料，以清单登记和官方安装来源说明代替原文件上传。清单登记不代表授予这些材料的复制、分发或再许可权利。
