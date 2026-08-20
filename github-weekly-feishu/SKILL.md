---
name: github-weekly-feishu
description: Use when the user wants a Feishu-ready Chinese technical weekly article about current GitHub trending or popular projects, especially with AI programming, DevOps, learning, generated illustrations, Markdown delivery, project ranking, or humanized Chinese writing.
---

# GitHub Weekly Feishu

## Overview

Create a Feishu-ready Chinese technical weekly from GitHub hot/trending projects. The output should be practical for operations engineers: clear project purpose, usage scenarios, production cautions, generated visuals, and Markdown that can be pasted or imported into Feishu.

## Workflow

1. Confirm the data source and time window.
   - If the user asks for "this week", "latest", "today", or similar current information, browse or otherwise verify live data before ranking.
   - State the exact date and ranking basis, such as "GitHub Trending this week" or "this week's new stars".
   - If the user explicitly says to reuse earlier data, do not re-verify; state that the article uses the previous snapshot.

2. Select projects.
   - Filter to the requested domains, usually AI programming, DevOps, automation, and learning.
   - Rank by the agreed metric, normally weekly star growth rather than all-time stars.
   - Keep the list small unless requested otherwise. For a weekly Feishu article, 5 projects is the default.
   - Keep project links, star numbers, and repository names unchanged after selection.

3. Write in a humanized Chinese technical-weekly style.
   - Prefer short paragraphs and concrete explanations.
   - Avoid inflated wording such as "划时代", "重塑格局", "关键转折点", and generic "价值巨大".
   - Avoid formulaic AI phrasing: "不仅...而且...", "此外", "核心价值", "趋势很明显" when they add no information.
   - Explain from an operations-engineering angle: where it fits, what problem it solves, what to verify before use.

4. Structure for Feishu.
   - Title: `# 本周 GitHub 热门项目推荐`
   - Add a brief metadata line: date/data source/snapshot note.
   - Insert a cover image near the top.
   - Add the fixed opening paragraph when the user asks for the standard weekly format.
   - Include one project overview table.
   - For each project, use these sections:
     - `### 它做什么`
     - `### 适合什么场景`
     - `### 运维视角注意点`
   - Add a short weekly observation section.
   - Add the fixed closing paragraph when the user asks for the standard weekly format.
   - Add a "配图导入说明" table if local images are generated.

## Standard Opening and Closing

Use this opening exactly unless the user asks for a different style:

> 本周 GitHub 热门项目继续被 AI 工具链占据。相比单纯聊天，这些项目更关心怎么把 AI 接进真实工作流：写代码、记上下文、操作浏览器、切换模型、辅助自动化。下面选 5 个和 AI 编程、运维、学习提效关系更近的项目，适合本周快速了解。

Use this closing exactly unless the user asks for a different style:

> 本周这几个项目可以放在一个判断里看：AI 工具正在从‘回答问题’转向‘参与工作流’。真正落地时，建议优先关注权限隔离、网络可用性、API 成本、数据安全和回滚方案。尤其是接入浏览器自动化、模型网关、长期记忆这类能力时，不要直接上生产环境，先在测试环境里跑清楚边界。

## Visuals

Generate 3 technology editorial illustrations when the user asks for images or a Feishu document with visuals:

| Image | Placement | Prompt intent |
|---|---|---|
| Cover | Below the title | AI coding, terminal, automation workflow, GitHub hot-project discovery without real logos |
| AI Agent toolchain | After the overview table | Code assistant, terminal, memory store, model router, connected workflow nodes |
| DevOps automation | Near the model-router/automation section | Browser automation, monitoring dashboard, API gateway, security boundary, rollback path |

Rules:
- Do not use real GitHub logos or project trademarks in generated images.
- Prefer clean technology illustration, 16:9, blue/teal/gray palette, no readable small text.
- Save or copy images into a local `assets/` directory when creating a workspace document.
- Use Markdown image links for local delivery, for example `![封面图](assets/github-weekly-cover.png)`.

## Output Files

For a workspace artifact, create:

- `github-weekly-feishu.md`
- `assets/github-weekly-cover.png`
- `assets/github-weekly-ai-agent-toolchain.png`
- `assets/github-weekly-devops-automation.png`

If those names already exist, avoid overwriting user work unless the user explicitly asked to update them. Use a dated suffix instead, such as `github-weekly-feishu-2026-05-17.md`.

## Acceptance Checklist

Before final response, verify:

- The requested number of projects is present.
- Repository names, links, domains, and star numbers match the chosen snapshot.
- The fixed opening and closing are present when required.
- Markdown headings, table, image links, and Feishu-friendly paragraph lengths are clean.
- Image files exist when referenced from Markdown.
- No unsafe production advice is left without caution, especially for browser automation, model gateways, long-term memory, API keys, credentials, and automated command execution.

## Common Mistakes

- Do not present stale GitHub rankings as current. Browse when the user asks for latest/current data.
- Do not turn the article into marketing copy. Keep the explanation concrete.
- Do not leave image placeholders in the final Markdown if images were generated and local paths are available.
- Do not put secrets, API keys, internal URLs, or account details into examples.
- Do not claim a Feishu online document was created unless a Feishu connector/tool actually created it.
