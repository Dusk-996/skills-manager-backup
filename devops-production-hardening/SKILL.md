---
name: devops-production-hardening
description: 对已有 DevOps 工具、Shell 脚本、Python/Go 后端、agent、Docker Compose、Kubernetes、Nginx 项目做生产化加固检查和补齐。用户提到"生产化""加固""上线前检查""部署到生产""补健康检查/日志/回滚/备份/国内源/安全配置"时使用。
---

# DevOps 生产化加固

用于把“能跑”的工具或平台加固成“能部署、能验证、能排障、能回滚”的生产谨慎形态。

## 个人工具链入口

- 加固前优先读取 `../profile/ops-engineer-cn.yml`，按个人默认安全策略检查备份、回滚、验证和 dry-run 要求。
- 加固完成后建议运行 `../scripts/devops-skillctl.ps1 accept`；需要输出交付记录时运行 `../scripts/devops-skillctl.ps1 report`。
- 没有 Docker 或 kubectl 时，真实运行验收降级为静态验收，不把缺少工具当成生产变更失败。

## 工作流程

1. 先识别项目类型：Shell 工具、Python 服务、Go 服务、agent、前端、Docker Compose、K8s、Nginx。
2. 读取项目入口、配置、依赖、部署文件和 README。缺文件时按缺口处理，不要脑补已经存在。
3. 按 `references/hardening-checklist.md` 做检查，输出缺口和建议。
4. 如果涉及危险操作，必须先读取 `references/dangerous-operations.md`，并输出影响范围、备份、验证、回滚。
5. 实施加固时保持最小改动，不重构无关代码。

## 必须覆盖的加固维度

- 统一规则：先按 `../project-init/references/acceptance-rules.md` 检查固定输出和硬失败项。
- 启动方式：生产环境不使用热加载、debug、mock。
- 配置：支持环境变量或配置文件覆盖，示例文件不包含真实密钥。
- 日志：容器优先 stdout，本机部署说明日志位置和轮转。
- 健康检查：至少有 health；需要依赖检查时增加 ready。
- 构建验证：给出可执行的 build/test/lint/smoke 命令。
- 部署：Docker、Compose、K8s、systemd 按项目形态补齐。
- 回滚：明确上一版本镜像、二进制、配置和数据库回滚方式。
- 国内环境：pip/npm/Go/Docker/K8s 镜像源或离线方案。

## 输出格式

默认用 Markdown，结构固定：

1. 影响范围
2. 当前问题
3. 加固方案
4. 执行步骤
5. 验证命令
6. 回滚方案
7. 生产环境注意事项

如果只是做检查，不改文件，则输出问题清单和建议优先级。
