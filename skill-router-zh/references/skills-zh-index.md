# 中文 Skill 使用索引

> 用途：按中文任务场景查找应该使用的 Codex skill。  
> 维护原则：优先覆盖高频工作流；插件缓存里的 skill 不直接修改，用本索引做中文说明。

## 快速选择表

| 你想做什么 | 推荐 skill | 中文理解 |
|---|---|---|
| 去掉 AI 味、中文润色 | `humanizer-zh` | 中文人味化润色 |
| 写 GitHub 热门项目飞书周报 | `github-weekly-feishu` | GitHub 周报生成 |
| 不知道该用哪个 skill | `skill-router-zh` | 中文 skill 导航 |
| 找有没有现成 skill | `find-skills` | skill 搜索和安装 |
| 生成或编辑图片 | `imagegen` | AI 配图生成 |
| 做 HTML/PPT 风格演示稿 | `html-ppt` | HTML 演示稿 |
| 做 PowerPoint / PPTX | `presentations` / `pptx` | PPT 文件处理 |
| 处理 Excel 表格 | `spreadsheets` | 表格分析和生成 |
| 处理 Word 文档 | `documents` | Word 文档编辑 |
| 查 GitHub PR / Issue | `github` | GitHub 仓库处理 |
| 修 GitHub Actions CI | `gh-fix-ci` | CI 故障排查 |
| 处理 PR review 意见 | `gh-address-comments` | Review 修改 |
| 提交、推送、开 PR | `yeet` | 发布本地修改 |
| 调试 OpenAI API 报错 | `openai-api-troubleshooting` | OpenAI 接口排障 |
| 创建 OpenAI API Key | `openai-platform-api-key` | API Key 配置 |
| 构建 Agents SDK 应用 | `agents-sdk` | OpenAI Agent 开发 |
| 构建 ChatGPT App | `build-chatgpt-app` | ChatGPT Apps SDK |
| 做前端页面或视觉设计 | `frontend-design` / `frontend-app-builder` | 前端界面生成 |
| 调试本地网页 | `browser` / `agent-browser` | 浏览器自动化验证 |
| React / Next.js 优化 | `react-best-practices` / `nextjs` | 前端框架实践 |
| Vercel 部署排障 | `vercel-cli` / `deployments-cicd` | Vercel 部署 |
| 线上错误分析 | `sentry` | Sentry 问题分析 |
| 制作视频 / 动画 | `hyperframes` / `remotion-best-practices` | 视频生成 |

## 运维排障

| 中文名称 | 原 skill | 什么时候用 | 典型口令 | 不适合 |
|---|---|---|---|---|
| CI 故障排查 | `gh-fix-ci` | GitHub Actions 失败、PR 检查没过 | “GitHub Actions 挂了，帮我看原因” | 非 GitHub CI |
| GitHub 仓库处理 | `github` | 查 PR、issue、repo、CI 状态 | “帮我看这个 PR 改了什么” | 本地纯文件处理 |
| Sentry 错误分析 | `sentry` | 查看线上报错、事件、异常趋势 | “帮我看最近生产错误” | 没接 Sentry 的项目 |
| 浏览器验证 | `browser` / `agent-browser` | 打开本地页面、截图、点击验证 | “打开 localhost:3000 看页面” | 需要用户登录态时优先 Chrome |
| Vercel 部署排障 | `vercel-cli` / `deployments-cicd` | Vercel 构建失败、部署、回滚、日志 | “Vercel 部署失败，帮我查日志” | 非 Vercel 平台 |

## 文档处理

| 中文名称 | 原 skill | 什么时候用 | 典型口令 | 不适合 |
|---|---|---|---|---|
| Word 文档 | `documents` | 创建、编辑、批注、导出 `.docx` | “帮我改这个 Word 文档” | Markdown 纯文本可直接处理 |
| 表格处理 | `spreadsheets` | Excel 分析、清洗、图表、导出 | “帮我分析这个 Excel” | 数据库在线查询 |
| PPT 制作 | `presentations` / `pptx` | `.pptx` 创建、修改、渲染验证 | “做一份 PPT” | 只要静态 HTML 演示稿时用 `html-ppt` |
| HTML 演示稿 | `html-ppt` | 用 HTML 做可视化技术分享、汇报页 | “做一个技术分享 HTML PPT” | 必须交付 `.pptx` 时优先 `presentations` |
| 飞书周报 | `github-weekly-feishu` | GitHub 项目推荐、飞书 Markdown、配图 | “写本周 GitHub 热门项目飞书文档” | 非 GitHub 周报 |

## GitHub 工作流

| 中文名称 | 原 skill | 什么时候用 | 典型口令 | 不适合 |
|---|---|---|---|---|
| GitHub 总入口 | `github` | 查仓库、PR、issue、CI 概况 | “帮我看这个 issue” | 没有 GitHub 上下文 |
| 修 CI | `gh-fix-ci` | Actions failed、checks failed | “CI 红了，帮我修” | 非 CI 问题 |
| 处理 review | `gh-address-comments` | PR review 有待处理意见 | “处理 PR review 意见” | 没有 PR review |
| 提交发布 | `yeet` | commit、push、open PR | “提交并开 PR” | 用户不想提交代码 |

## AI / OpenAI

| 中文名称 | 原 skill | 什么时候用 | 典型口令 | 不适合 |
|---|---|---|---|---|
| OpenAI 接口排障 | `openai-api-troubleshooting` | 401、429、模型不可用、请求失败 | “OpenAI API 报 401” | 非 OpenAI 服务 |
| API Key 设置 | `openai-platform-api-key` | 需要创建或配置 `OPENAI_API_KEY` | “帮我配置 OpenAI API Key” | 不需要 OpenAI Key |
| Agents SDK | `agents-sdk` | 构建 OpenAI Agent 应用 | “用 Agents SDK 做个工具” | 普通聊天提示词 |
| ChatGPT App | `build-chatgpt-app` | MCP server + widget UI 的 ChatGPT App | “做一个 ChatGPT App” | 普通网页应用 |
| 官方文档查询 | `openai-docs` | 查 OpenAI 最新官方用法 | “查一下 Responses API 怎么用” | 非 OpenAI 文档 |

## 前端 / 网页

| 中文名称 | 原 skill | 什么时候用 | 典型口令 | 不适合 |
|---|---|---|---|---|
| 前端视觉设计 | `frontend-design` | 页面、组件、海报、仪表盘视觉设计 | “帮我做一个好看的页面” | 后端脚本 |
| 前端应用生成 | `frontend-app-builder` | 新建前端 app、dashboard、game | “做一个前端小工具” | 只改一段文案 |
| 前端调试 | `frontend-testing-debugging` | 截图、布局、交互、渲染问题 | “页面错位了，帮我看” | 后端接口排障 |
| React 实践 | `react-best-practices` | React/TSX 性能或结构优化 | “帮我检查 React 组件” | 非 React 项目 |
| Next.js | `nextjs` | Next.js App Router、构建、路由问题 | “Next.js 页面报错” | 非 Next.js |
| Vercel | `vercel-cli` / `deployments-cicd` | 部署、环境变量、日志、回滚 | “帮我部署到 Vercel” | 其他云平台 |

## 内容创作

| 中文名称 | 原 skill | 什么时候用 | 典型口令 | 不适合 |
|---|---|---|---|---|
| 中文去 AI 味 | `humanizer-zh` | 中文文章润色、改得自然 | “把这段话改得像人写的” | 代码逻辑问题 |
| AI 配图 | `imagegen` | 生成封面图、插图、视觉素材 | “给这篇文章配图” | 需要精确工程图纸 |
| GitHub 周报 | `github-weekly-feishu` | GitHub 热门项目推荐文章 | “生成飞书版 GitHub 周报” | 非项目推荐 |
| 视频动画 | `hyperframes` / `remotion-best-practices` | 生成视频、动画、字幕、网页转视频 | “把这个网站做成视频” | 只要静态文档 |

## 10 个测试场景

| 中文请求 | 应推荐 |
|---|---|
| “帮我润色这篇中文文章” | `humanizer-zh` |
| “帮我做一份 PPT” | `presentations` 或 `html-ppt` |
| “帮我分析 Excel” | `spreadsheets` |
| “GitHub Actions 挂了” | `gh-fix-ci` |
| “我要处理 PR review” | `gh-address-comments` |
| “我要写本周 GitHub 热门项目飞书文档” | `github-weekly-feishu` |
| “OpenAI API 报 401” | `openai-api-troubleshooting` |
| “我要生成一张配图” | `imagegen` |
| “帮我调试前端页面” | `frontend-testing-debugging` 或 `browser` |
| “帮我部署 Vercel” | `vercel-cli` 或 `deployments-cicd` |

## 维护建议

- 新增个人 skill 后，把它补到本索引。
- 插件自带 skill 不直接改显示名；用中文索引解释即可。
- 如果某个 skill 你经常用，可以为个人 skill 添加 `agents/openai.yaml` 中文显示名。
