# 有了可运行页面，怎么验证关键用户路径？

[返回场景目录](README.md) · Vibe Coding · 构建和交付运维工具

**已有材料**　可访问的环境、测试账号或页面与业务路径

**结束产物**　浏览器验证证据或正式 E2E 报告

![有了可运行页面，怎么验证关键用户路径？](browser-check.svg)

[打开交互图](https://dusk-996.github.io/skills-manager-backup/atlas/browser-check.html) · [查看原尺寸 SVG](browser-check.svg)

## 技能怎么用

| 技能 | 何时使用 | 得到什么 |
|---|---|---|
| [playwright-cli](../../playwright-cli/SKILL.md) | 需要操作浏览器和检查特定页面 | 取得页面状态、交互结果与证据 |
| [playwright-e2e-debug-report](../../playwright-e2e-debug-report/SKILL.md) | 明确要求 Playwright E2E、冒烟、回归或完整的人工确认测试报告时 | 先给测试计划，确认后执行并交付问题与报告 |
| [computer-use](../../docs/RESTORE.md) | 必须通过已连接的桌面或浏览器操作时可独立使用 | 得到界面操作结果；需要应用会话 |

### 应用运行条件

在提供相应能力的 Codex 环境中使用这些入口。安装与连接要求见[应用恢复说明](../RESTORE.md)。

- **computer-use**　Codex 应用插件：openai-bundled/computer-use/26.1111.21308

## 可以接着做

- [巡检工具准备上线，怎么打包、加固和审查？](package.md)　从「服务入口、部署目标、现有配置与测试结果」开始。
- [准备收尾或换人，怎么验证并交接？](release-branch.md)　从「已实现改动、测试命令和工作分支」开始。
