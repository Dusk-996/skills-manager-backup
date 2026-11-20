# 拿到开发任务，怎么拆模块并用测试实现？

[返回场景目录](README.md) · Vibe Coding · 构建和交付运维工具

**已有材料**　功能要求、代码和验收行为

**结束产物**　有测试支撑的实现

![拿到开发任务，怎么拆模块并用测试实现？](build-feature.svg)

[打开交互图](https://dusk-996.github.io/skills-manager-backup/atlas/build-feature.html) · [查看原尺寸 SVG](build-feature.svg)

## 技能怎么用

| 技能 | 何时使用 | 得到什么 |
|---|---|---|
| [codebase-design](../../codebase-design/SKILL.md) | 模块边界或测试接口需要先厘清时 | 得到接口与可测性设计 |
| [tdd](../../tdd/SKILL.md) | 采用侧重用户行为和集成测试的开发方法 | 逐个行为红绿重构并留下回归测试 |
| [test-driven-development](../../external-skills/superpowers/skills/test-driven-development/SKILL.md) | 项目使用 Superpowers 测试优先流程时选此入口 | 先取得失败测试，再补实现和验证 |

## 可以接着做

- [代码改完，怎么组织审查和处理意见？](review-code.md)　从「提交范围、Spec、实施计划和改动」开始。
- [有了可运行页面，怎么验证关键用户路径？](browser-check.md)　从「可访问的环境、测试账号或页面与业务路径」开始。
