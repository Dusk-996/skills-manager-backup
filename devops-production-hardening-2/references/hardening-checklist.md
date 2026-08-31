# 生产化加固检查清单

## 通用

| 检查项 | 要求 |
|---|---|
| 配置 | 提供 `.env.example` 或 `config.example.yaml`，真实密钥不入库 |
| 启动 | 生产不启用 debug、reload、mock |
| 日志 | 容器输出 stdout/stderr，本机部署说明日志路径和轮转 |
| 健康检查 | Web 服务提供 `/health`，依赖检查可提供 `/ready` |
| 依赖 | 锁定版本或保留 lock 文件，说明国内源 |
| 构建 | 提供 `make build` 或等价命令 |
| 测试 | 至少有 smoke test 或 health test |
| 回滚 | 镜像/二进制/配置保留上一版本 |

## Shell

- 使用 `set -Eeuo pipefail`。
- 提供 `usage()`、参数校验、退出码。
- 危险操作默认 dry-run 或二次确认。
- 输出执行前备份、验证、回滚命令。

## Python

- FastAPI/uvicorn 生产不使用 `reload=True`。
- 生产建议 `gunicorn + uvicorn worker` 或明确 workers。
- CORS 通过配置限制来源。
- `requirements.txt` 固定版本或说明锁定策略。

## Go

- `go test ./...` 和 `go build ./...` 必须通过。
- 不允许未使用 import。
- agent 二进制使用 `CGO_ENABLED=0 go build -trimpath -ldflags "-s -w"`。
- 配置文件示例不包含真实 token。

## Docker / Compose

- 镜像 tag 不使用 `latest` 作为生产发布依据。
- 容器尽量非 root 用户运行。
- 使用 healthcheck。
- volume、端口、环境变量写清影响范围。

## Kubernetes

- Deployment 配置 readiness/liveness。
- ConfigMap 和 Secret 分离。
- 设置 resources requests/limits。
- 给出 `kubectl rollout status` 和 `kubectl rollout undo`。

## Nginx

- 前端静态资源设置缓存策略。
- API 代理带 `X-Real-IP`、`X-Forwarded-For`。
- BrowserRouter 必须有 `try_files` fallback。
- 生产变更前备份配置并执行 `nginx -t`。
