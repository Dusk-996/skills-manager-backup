# Docker Compose 交付模板

## docker-compose.yml

```yaml
services:
  app:
    image: app:20260531-1
    build:
      context: .
    env_file:
      - .env
    ports:
      - "8080:8080"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

## 命令

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f --tail=100 app
curl -f http://127.0.0.1:8080/health
```

## 回滚

```bash
docker compose down
# 修改 image 为上一版本 tag
docker compose up -d
```

生产注意：生产镜像 tag 使用版本号或日期，不使用 `latest`。
