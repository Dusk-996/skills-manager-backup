# 代码改完，怎么组织审查和处理意见？

[返回场景目录](README.md) · Vibe Coding · 构建和交付运维工具

**已有材料**　提交范围、Spec、实施计划和改动

**结束产物**　有依据的审查结果和处理记录

![代码改完，怎么组织审查和处理意见？](review-code.svg)

[打开交互图](https://dusk-996.github.io/skills-manager-backup/atlas/review-code.html) · [查看原尺寸 SVG](review-code.svg)

## 技能怎么用

| 技能 | 何时使用 | 得到什么 |
|---|---|---|
| [devops-requesting-code-review](../../devops-requesting-code-review/SKILL.md) | 运维项目需要对齐实施计划和生产约束 | 形成审查上下文和针对性评审 |
| [requesting-code-review](../../external-skills/superpowers/skills/requesting-code-review/SKILL.md) | 通用开发任务需要发起审查 | 按变更范围交接给评审者 |
| [code-review](../../code-review/SKILL.md) | 有可比对的提交范围、标准和需求 | 得到规范与需求符合性发现 |
| [review-agent](../../docs/RESTORE.md) | 应用提供只读审查角色且可委派时选用 | 取得带位置和触发条件的缺陷发现 |
| [receiving-code-review](../../external-skills/superpowers/skills/receiving-code-review/SKILL.md) | 收到意见后 | 核对依据、修复成立的问题并验证 |

### 应用运行条件

在提供相应能力的 Codex 环境中使用这些入口。安装与连接要求见[应用恢复说明](../RESTORE.md)。

- **review-agent**　Codex 应用内置系统技能

## 可以接着做

- [有了可运行页面，怎么验证关键用户路径？](browser-check.md)　从「可访问的环境、测试账号或页面与业务路径」开始。
- [准备收尾或换人，怎么验证并交接？](release-branch.md)　从「已实现改动、测试命令和工作分支」开始。
