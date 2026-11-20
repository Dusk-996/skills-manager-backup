# 按场景查找技能

从手里的材料选择入口。共 26 个场景，覆盖 80 项技能。标有「附图」的场景提供静态预览与可交互的横向流程图。

[查看全部技能及原始说明](../../README.md)

## Vibe Coding · 构建和交付运维工具

- **[想把巡检脚本做成工具，怎么确定需求和实现计划？](ops-design.md)**　**附图**<br>
  运维痛点、部署环境与边界 → 有验收条件的实施计划<br>
  `devops-brainstorming`、`devops-writing-plans`<br>
  后续可选　[确定做 Shell 工具或服务后，怎么开工？](bootstrap.md) · [还没有页面，怎么确定运维平台原型？](ui-prototype.md)
- **[确定做 Shell 工具或服务后，怎么开工？](bootstrap.md)**　**附图**<br>
  已确认需求、语言和交付形态 → 可运行和验证的初始工程<br>
  `project-init`<br>
  后续可选　[拿到开发任务，怎么拆模块并用测试实现？](build-feature.md) · [巡检工具准备上线，怎么打包、加固和审查？](package.md)
- **[还没有页面，怎么确定运维平台原型？](ui-prototype.md)**　**附图**<br>
  用户任务、核心操作和页面要求 → 可供评审的页面原型<br>
  `frontend-design`、`ui-ux-pro-max`、`design-taste-frontend`<br>
  后续可选　[已有 HTML 原型，怎么做出可操作的页面？](prototype-to-mock.md)
- **[已有 HTML 原型，怎么做出可操作的页面？](prototype-to-mock.md)**　**附图**<br>
  已确认的 HTML、关键交互和页面尺寸 → 可运行的 React + Mock，按需取得一致性报告<br>
  `html-to-mui-react`、`prototype-parity-review`<br>
  后续可选　[已有 React Mock，怎么定后端架构？](mock-to-architecture.md)
- **[已有 React Mock，怎么定后端架构？](mock-to-architecture.md)**　**附图**<br>
  可运行的 Mock、数据字段和任务行为 → 定稿的技术选型单，可交给 SDD 明确边界<br>
  `stack-selector`、`grilling`、`domain-modeling`<br>
  后续可选　[需求讨论完，怎么拆出可领取的任务？](spec-tickets.md)
- **[需求讨论完，怎么拆出可领取的任务？](spec-tickets.md)**　**附图**<br>
  已有讨论、目标、技术决策或现成规格 → 可分派且有验收条件、依赖关系的任务<br>
  `setup-matt-pocock-skills`、`to-spec`、`to-tickets`<br>
  后续可选　[拿到开发任务，怎么拆模块并用测试实现？](build-feature.md)
- **[拿到开发任务，怎么拆模块并用测试实现？](build-feature.md)**　**附图**<br>
  功能要求、代码和验收行为 → 有测试支撑的实现<br>
  `codebase-design`、`tdd`、`test-driven-development`<br>
  后续可选　[代码改完，怎么组织审查和处理意见？](review-code.md) · [有了可运行页面，怎么验证关键用户路径？](browser-check.md)
- **[代码改完，怎么组织审查和处理意见？](review-code.md)**　**附图**<br>
  提交范围、Spec、实施计划和改动 → 有依据的审查结果和处理记录<br>
  `devops-requesting-code-review`、`requesting-code-review`、`code-review`、`review-agent`、`receiving-code-review`<br>
  后续可选　[有了可运行页面，怎么验证关键用户路径？](browser-check.md) · [准备收尾或换人，怎么验证并交接？](release-branch.md)
- **[有了可运行页面，怎么验证关键用户路径？](browser-check.md)**　**附图**<br>
  可访问的环境、测试账号或页面与业务路径 → 浏览器验证证据或正式 E2E 报告<br>
  `playwright-cli`、`playwright-e2e-debug-report`、`computer-use`<br>
  后续可选　[巡检工具准备上线，怎么打包、加固和审查？](package.md) · [准备收尾或换人，怎么验证并交接？](release-branch.md)
- **[巡检工具准备上线，怎么打包、加固和审查？](package.md)**　**附图**<br>
  服务入口、部署目标、现有配置与测试结果 → 交付部署包，或得到上线就绪结论<br>
  `deployment-packager`、`devops-production-hardening`、`ops-readiness-review`<br>
  后续可选　[有了可运行页面，怎么验证关键用户路径？](browser-check.md) · [准备收尾或换人，怎么验证并交接？](release-branch.md)

## 协作开发与交接

- **[团队使用 Superpowers，如何把想法变成可执行计划？](dev-plan.md)**　**附图**<br>
  待明确的通用功能或设计任务 → 经讨论的设计与分步计划<br>
  `using-superpowers`、`brainstorming`、`writing-plans`<br>
  后续可选　[计划已经写好，一个会话做还是并行做？](execute-plan.md)
- **[计划已经写好，一个会话做还是并行做？](execute-plan.md)**　**附图**<br>
  实施计划、任务依赖与当前工作区 → 实现结果、评审与任务验证记录<br>
  `using-git-worktrees`、`executing-plans`、`subagent-driven-development`、`dispatching-parallel-agents`<br>
  后续可选　[代码改完，怎么组织审查和处理意见？](review-code.md) · [准备收尾或换人，怎么验证并交接？](release-branch.md)
- **[准备收尾或换人，怎么验证并交接？](release-branch.md)**　**附图**<br>
  已实现改动、测试命令和工作分支 → 完成证据、分支处理结果或交接文档<br>
  `verification-before-completion`、`finishing-a-development-branch`、`handoff`

## 值班排障与观测

- **[服务不通，从主机、K8s 还是应用查起？](incident.md)**　**附图**<br>
  主机日志、Pod 状态或可复现的异常 → 有证据支持的定位、修复和验证路径<br>
  `ssh-remote-ops`、`k8s-troubleshoot`、`diagnosing-bugs`、`systematic-debugging`<br>
  后续可选　[定位瓶颈后，怎么做成 Grafana 看板？](observability.md)
- **[定位瓶颈后，怎么做成 Grafana 看板？](observability.md)**　**附图**<br>
  已确认的数据源、指标、标签与查询目标 → 可导入的看板及对应查询<br>
  `grafana-dashboards`

## 学习、复习与面试

- **[课程录音和资料怎么整理成可复习的路线图？](notes-roadmap.md)**　**附图**<br>
  可访问的录音 URL 或已有同主题文本 → 结构化笔记或可跟踪学习进度的网页<br>
  `aliyun-asr`、`learning-notes-builder`、`learning-roadmap`<br>
  后续可选　[怎样把笔记或故障经验变成面试题？](interview.md)
- **[正在学一门课，怎么读懂这一章并接着学？](course-study.md)**　**附图**<br>
  FDE 章节材料或个人学习目标 → 章节讲解，或可跨会话延续的教学记录<br>
  `fde-creator`、`teach`<br>
  后续可选　[课程录音和资料怎么整理成可复习的路线图？](notes-roadmap.md) · [怎样把笔记或故障经验变成面试题？](interview.md)
- **[怎样把笔记或故障经验变成面试题？](interview.md)**　**附图**<br>
  笔记、目标岗位、可选已有题库或脱敏案例 → 确认后的普通题或场景题及追问<br>
  `question-gap-analyzer`、`scenario-question-designer`

## 技术表达与办公交付

- **[项目动态怎么整理成周报或公众号文章？](publish-article.md)**　**附图**<br>
  GitHub 项目资料，或已有中文 Markdown → 可交给飞书的周报或公众号 HTML<br>
  `github-weekly-feishu`、`humanizer-zh`、`baoyu-markdown-to-html`<br>
  后续可选　[我要讲清一套系统，选交互图还是可编辑图？](explain-visually.md)
- **[我要讲清一套系统，选交互图还是可编辑图？](explain-visually.md)**　**附图**<br>
  系统说明、仓库证据、讲解问题或图稿 → 取决于读者的交互图、可编辑图或插图<br>
  `archify`、`draw-io-diagram-generator`、`visualize`、`baoyu-infographic`、`imagegen`<br>
  后续可选　[项目材料要做技术分享，交付网页还是 PPT？](slides.md)
- **[项目材料要做技术分享，交付网页还是 PPT？](slides.md)**　**附图**<br>
  文档、已有幻灯片、受众与目标格式 → 网页演示、图片型 PPTX 或可编辑幻灯片<br>
  `project-to-open-slide`、`frontend-slides`、`pptx`、`Presentations`
- **[收到工作簿或文档，怎么分析和交付？](office-files.md)**　**附图**<br>
  Excel、CSV、Word、PDF 或已打开的工作簿 → 处理后的工作簿、报告或经检查的文档<br>
  `Spreadsheets`、`excel-live-control`、`documents`、`pdf`<br>
  后续可选　[项目材料要做技术分享，交付网页还是 PPT？](slides.md)

## 维护个人技能库和 Codex 环境

- **[这件事有现成 skill 吗，缺的怎么补？](find-install.md)**　**附图**<br>
  自然语言任务，或已选定的技能来源 → 可用技能推荐或安装结果<br>
  `devops-skill-router-zh`、`skill-router-zh`、`find-skills`、`skill-installer`<br>
  后续可选　[怎么把重复工作变成技能并改进效果？](author-skill.md)
- **[怎么把重复工作变成技能并改进效果？](author-skill.md)**　**附图**<br>
  可重复的任务或已认可的成品、已有技能 → 可复用技能、个人模板或优化报告<br>
  `skill-creator`、`writing-skills`、`template-creator`、`darwin-skill`
- **[怎样迁移旧规则、配置 Codex 和专用代理？](codex-environment.md)**　**附图**<br>
  旧规则或明确的工作习惯与配置目标 → 在正确作用域生效的规则、配置或代理定义<br>
  `migrate-to-codex`、`codex-project-rules`、`codex-config-manager`、`codex-agent-config`<br>
  后续可选　[会话为什么重复劳动，怎样核实工具行为？](diagnose-workflow.md)
- **[会话为什么重复劳动，怎样核实工具行为？](diagnose-workflow.md)**　**附图**<br>
  Superpowers 会话记录或 OpenAI 产品使用问题 → 有证据的工作流诊断或官方使用依据<br>
  `diagnosing-superpowers`、`openai-docs`<br>
  后续可选　[怎样迁移旧规则、配置 Codex 和专用代理？](codex-environment.md)
