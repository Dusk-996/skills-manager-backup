---
name: skill-router-zh
description: Use when a Chinese-speaking user is unsure which Codex skill to use, asks for a Chinese skill guide, wants to find skills by Chinese task descriptions, or needs routing for tasks like DevOps troubleshooting, documents, GitHub, OpenAI, frontend, Feishu weekly reports, images, PPT, Excel, Word, browser testing, or Chinese text polishing.
---

# Skill 中文导航

## 作用

当用户用中文描述任务但不知道该用哪个 skill 时，先用本 skill。目标不是执行任务本身，而是把用户意图翻译成合适的 skill 选择，并用中文说明推荐理由。

## 使用方式

1. 先读取 `references/skills-zh-index.md`。
2. 按用户的中文场景匹配 1-3 个候选 skill。
3. 用中文回答：
   - 推荐使用哪个 skill
   - 为什么选它
   - 典型触发口令
   - 是否需要搭配其他 skill
4. 如果任务已经很明确，可以直接进入对应 skill 的工作流；不要让用户自己看英文列表。

## 路由原则

- 优先匹配用户真实任务，不按英文 skill 名称猜。
- 运维、Docker、K8s、CI、日志、生产排障场景，优先选择排障或 GitHub/浏览器/部署相关 skill。
- 文档、PPT、Excel、Word、飞书周报场景，优先选择文档类或内容类 skill。
- OpenAI API、API Key、Agents SDK、ChatGPT App 场景，优先选择 OpenAI Developers 相关 skill。
- 前端页面、React、Next.js、Vercel 部署场景，优先选择前端或 Vercel 相关 skill。
- 中文润色、去 AI 味、技术周报、配图，优先选择内容创作类 skill。

## 输出模板

```markdown
建议使用：`skill-name`

原因：一句话说明为什么它匹配当前任务。

典型口令：
- “……”
- “……”

可搭配：
- `other-skill`：说明搭配原因。

注意事项：如涉及生产环境、密钥、删除、重启、部署等，提醒备份、验证和回滚。
```

## 常见组合

| 中文场景 | 推荐组合 |
|---|---|
| 写 GitHub 热门项目飞书周报 | `github-weekly-feishu` + `imagegen` |
| 中文文章去 AI 味 | `humanizer-zh` |
| 做 PPT / 演示稿 | `html-ppt` 或 `presentations` |
| 分析 Excel | `spreadsheets` |
| 处理 Word 文档 | `documents` |
| GitHub Actions 失败 | `gh-fix-ci` |
| 处理 PR review | `gh-address-comments` |
| 查 PR / issue / repo | `github` |
| OpenAI API 报错 | `openai-api-troubleshooting` |
| 创建 OpenAI API Key | `openai-platform-api-key` |
| 做前端页面 | `frontend-design` 或 `frontend-app-builder` |
| Vercel 部署排障 | `vercel-cli` 或 `deployments-cicd` |

## 不要做

- 不要直接修改插件缓存目录里的 skill。插件更新可能覆盖这些文件。
- 不要要求用户理解英文列表后再选择。
- 不要把所有可能 skill 都推荐出来；最多给 3 个候选。
- 不要在未确认工具可用时声称已经创建飞书、GitHub PR、Vercel 部署等在线资源。
