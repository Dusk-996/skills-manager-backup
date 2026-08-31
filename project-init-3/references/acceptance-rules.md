# DevOps Skill 统一验收规则

这些规则适用于 `project-init`、`stack-selector`、`deployment-packager`、`devops-production-hardening`、`html-to-mui-react` 的输出审查。

## 固定输出要求

涉及工具、平台、agent、部署或生产化时，输出必须包含：

- 部署方式或运行方式。
- 验证命令。
- 回滚方案。
- 国内环境注意事项。
- 生产环境注意事项。

涉及危险操作时，还必须包含：

- 影响范围。
- 执行前备份。
- 执行步骤。
- 验证命令。
- 回滚方案。

## 硬失败项

出现以下任一项，视为不通过：

- Python 生产模板默认 `reload=True`。
- Python/Go 生产模板默认全开放 CORS，例如 `allow_origins=["*"]` 或 `AllowAllOrigins`。
- 前端生产环境 `VITE_USE_MOCK=true`。
- 生产镜像以 `latest` 作为发布依据。
- K8s 部署没有 `kubectl rollout status` 和 `kubectl rollout undo`。
- Secret 示例包含真实密码、token、key。
- 危险操作没有影响范围、备份、验证、回滚。
- 无明确证据默认引入 Redis、Kafka/RabbitMQ、WebSocket、微服务拆分。

## 推荐验收分层

1. 完整性验收：frontmatter、reference、Markdown 代码块、编码。
2. 场景验收：固定提示词是否命中正确 skill 和关键生产化要求。
3. 生成物运行验收：Python/Go/Shell/React/K8s 样例能否通过本地验证。

## 样例项目隔离

验收样例必须放在 `J:\skills-1\skill-acceptance-sandbox\`，不得放入 `J:\skills-1\skills\`。
