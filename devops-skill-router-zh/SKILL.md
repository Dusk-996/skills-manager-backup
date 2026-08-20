---
name: devops-skill-router-zh
description: Use when a Chinese-speaking DevOps or operations user is unsure which skill to use, asks which skill fits a task, says to follow their DevOps routing rules, or asks about Linux, Shell, Docker, Kubernetes, CI/CD, GitHub, documents, PPT, spreadsheets, AI ops, internal tools, dashboards, Vercel deployment, or production troubleshooting.
---

# DevOps Skill Router 中文路由

## 作用

本 skill 是 DevOps 场景的中文入口。它不直接替代具体 skill 执行任务，而是先判断用户意图，再最多推荐 1-3 个最相关 skill，避免把完整 skill 列表丢给用户。

优先遵守用户的 `AGENTS.md` 运维规则：直接、详细、可执行；涉及生产环境时提醒备份、验证和回滚；危险操作必须提前提醒。

## 何时使用

当用户出现以下任意情况时使用：

- 不知道该用哪个 skill。
- 询问“这个任务应该用哪些 skill”。
- 要求“按我的 DevOps 规则处理”。
- 任务涉及 Linux、Shell、Docker、Docker Compose、Kubernetes、Nginx、MySQL、ELK、Prometheus、CI/CD、GitHub、文档、PPT、Excel、AI 运维、内部工具、Dashboard、Vercel 或生产排障。

## 路由原则

- 最多推荐 1-3 个 skill。
- 优先匹配真实任务，不按 skill 名称硬猜。
- 如果任务已经很明确，可以直接说明将使用哪个 skill 并进入对应工作流。
- 不主动推荐低频 skill，除非任务明确相关。
- 不推荐已经删除或不可用的 skill，例如 `html-ppt`。

## 常见场景路由

| 场景 | 优先推荐 | 说明 |
|---|---|---|
| 故障排查、报错、异常、测试失败 | `systematic-debugging` + `verification-before-completion` | 先定位根因，再验证修复结果 |
| 生产变更、升级、迁移、批量修改 | `writing-plans` + `verification-before-completion` | 先计划，再执行验证和回滚设计 |
| GitHub 仓库、PR、Issue | `github` | 获取仓库、PR、Issue 上下文 |
| GitHub Actions / CI 失败 | `gh-fix-ci` | 专门排查 CI 日志和失败检查 |
| PR review 评论处理 | `gh-address-comments` | 处理评审意见和未解决线程 |
| Shell、Docker、K8s、Nginx、MySQL 运维任务 | 按 `AGENTS.md` 运维规则处理；复杂任务搭配 `writing-plans` | 优先输出命令、配置、验证、回滚 |
| Word / docx 文档 | `documents` | 处理 Word、报告、审计文档 |
| Excel / CSV / 表格 | `Spreadsheets` | 分析巡检表、资产表、告警统计、容量数据 |
| PPT / 故障复盘 / 技术汇报 | `pptx` 或 `Presentations` | `.pptx` 作为主入口；不要推荐 `html-ppt` |
| 中文润色、去 AI 味 | `humanizer-zh` | 技术文章、复盘、方案润色 |
| 飞书技术周报 | `github-weekly-feishu` + `imagegen` | 周报正文和配图 |
| 内部运维平台、Dashboard、页面原型 | `frontend-design` / `frontend-app-builder` / `frontend-testing-debugging` | 做内部工具或页面验证 |
| OpenAI API / Codex / 模型文档 | `openai-docs` / `openai-api-troubleshooting` | 优先官方文档和 API 排障 |
| AI 运维助手、ChatOps、Agent | `ai-sdk` / `agents-sdk` / `openai-docs` | 构建 AI 运维工具 |
| Vercel 部署、环境变量、日志、函数 | `vercel-cli` / `deployments-cicd` / `env-vars` / `observability` | 现代应用交付和部署排障 |

## 默认隐藏的低频能力

除非用户任务明确涉及，否则不要主动推荐：支付、CMS、动画、视频、Vercel 专项登录、低频 UI 细节、SaaS 模板等能力。

## 输出格式

使用以下格式，保持简洁：

```markdown
建议使用：`skill-name`

原因：一句话说明为什么匹配当前任务。

可搭配：`other-skill`，说明搭配原因。

注意事项：如果涉及生产环境、删除、重启、配置修改、密钥、部署或数据库变更，提醒备份、验证和回滚。
```

## 示例

用户：GitHub Actions 失败了，帮我看。

```markdown
建议使用：`gh-fix-ci`

原因：当前任务是 GitHub Actions CI 失败排查，需要读取检查状态和日志。

可搭配：`systematic-debugging`，用于按现象、原因、检查、修复、验证组织排障。

注意事项：修复 CI 配置前先确认影响范围，避免修改生产发布流程。
```

用户：帮我写一份 K8s 生产部署 YAML。

```markdown
建议使用：`writing-plans`

原因：生产级 K8s 配置需要先明确镜像、资源限制、健康检查、回滚和验证方式。

可搭配：`verification-before-completion`，用于检查 YAML 和部署验证步骤。

注意事项：涉及生产发布时必须准备备份、灰度、验证和回滚方案。
```
## DevOps 全局扩展 Skill

以下 skill 已从 `J:\skills-1\skills` 全局化，可在任意项目中通过本路由选择：

| 场景 | 优先推荐 | 说明 |
|---|---|---|
| DevOps 项目初始化 | `project-init` | 初始化 Shell、Python、Go 等生产谨慎型运维项目 |
| 技术栈选择 | `stack-selector` | 在 Shell、Python、Go、前端、Agent 等方案间做选型 |
| 部署交付包生成 | `deployment-packager` | 生成 Dockerfile、Compose、K8s、部署文档等交付材料 |
| 生产化加固 | `devops-production-hardening` | 加固脚本、后端、Compose、K8s、Nginx 等项目 |
| HTML 原型转运维前端 | `html-to-mui-react` | 将页面原型转为 Vite + React + MUI 项目 |
| DevOps 需求成型/压测方案 | `devops-brainstorming` | DevOps 定制版需求澄清、方案设计和风险拷问 |
| DevOps 实施计划 | `devops-writing-plans` | DevOps 定制版 tasks.md 生成，适合 docs/plans 工作流 |
| DevOps 代码审查 | `devops-requesting-code-review` | DevOps 定制版代码/计划审查流程 |

当这些 DevOps 定制 skill 与 superpowers 同名原版都可用时，DevOps 项目优先推荐 `devops-*` 版本；通用开发流程才推荐 superpowers 原版。