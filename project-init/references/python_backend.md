# Python Backend Template

## Directory Structure

```
CLAUDE.md
AGENTS.md -> CLAUDE.md
backend/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── health.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
└── logs/
    └── .gitkeep
```

## File Contents

### main.py

```python
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import health
from app.utils.logger import logger, setup_logger

# 初始化 logger
setup_logger({
    "log": {
        "level": settings.LOG_LEVEL,
        "file": settings.LOG_FILE,
        "max_size_mb": settings.LOG_MAX_SIZE_MB,
        "backup_count": settings.LOG_BACKUP_COUNT,
    }
})

app = FastAPI(title=settings.APP_NAME)

# CORS middleware
# 生产环境不要使用 "*"，通过 ALLOWED_ORIGINS 显式配置允许来源，多个来源用英文逗号分隔。
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Register routers
app.include_router(health.router)


if __name__ == "__main__":
    # reload 只允许开发环境使用，生产环境必须保持 DEBUG=false。
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
```

### app/config.py

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "backend"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_SIZE_MB: int = 10
    LOG_BACKUP_COUNT: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
```

### app/__init__.py

```python
```

### app/routers/__init__.py

```python
```

### app/routers/health.py

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}
```

### app/models/__init__.py

```python
```

### app/schemas/__init__.py

```python
```

### app/services/__init__.py

```python
```

### app/utils/logger.py

```python
"""
最简洁的全局 logger - Go 语言风格
"""

import os
import sys
from loguru import logger as _logger


def init_logger(config: dict = None):
    """初始化全局 logger"""
    # 移除默认处理器
    _logger.remove()

    if config is None:
        config = {}

    log_config = config.get('log', {})
    level = log_config.get('level', 'INFO').upper()

    # 控制台配置
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    _logger.add(
        sys.stderr,
        format=console_format,
        level=level,
        colorize=True
    )

    # 文件配置
    log_file = log_config.get('file')
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} - "
            "{message}"
        )

        _logger.add(
            log_file,
            format=file_format,
            level=level,
            rotation=log_config.get('max_size_mb', 10) * 1024 * 1024,
            retention=log_config.get('backup_count', 5),
            encoding="utf-8"
        )

    _logger.info("Logger initialized")
    return _logger


# 默认初始化
logger = init_logger()


def setup_logger(config: dict = None):
    """重新配置 logger"""
    global logger
    logger = init_logger(config)
    return logger


__all__ = ['logger', 'setup_logger']
```

### app/utils/__init__.py

```python
```

### CLAUDE.md

**注意**：生成 `CLAUDE.md` 时，必须先写入 `references/claude_md_preamble.md` 的完整内容，再写一行 `---` 分隔符，最后追加下面这段项目特定内容（详见 SKILL.md 的「CLAUDE.md 内容组合规则」）。

Generate with the actual project name replacing `{project_name}`:

```markdown
# {project_name}

## 项目说明

Python 后端服务，基于 FastAPI 构建。

## 技术栈

| 类型 | 选型 |
|------|------|
| Web 框架 | FastAPI |
| 日志 | loguru（`app/utils/logger.py`），支持控制台彩色输出 + 文件轮转 |
| 配置 | pydantic_settings BaseSettings，key 大写，支持同名环境变量覆盖 |
| 依赖管理 | requirements.txt |

## 目录结构

```
app/
├── config.py      # 配置类 Settings，所有配置项在此定义
├── routers/       # 路由，每个模块一个文件
├── models/        # ORM 数据库模型
├── schemas/       # Pydantic 请求/响应模型
├── services/      # 业务逻辑层
└── utils/
    └── logger.py  # 全局 logger，import 直接使用
```

## 开发约定

- **新增配置项**：在 `app/config.py` 的 `Settings` 类中添加，命名全大写
- **使用日志**：`from app.utils.logger import logger`，禁止直接使用 `print` 或标准库 logging
- **新增接口**：在 `app/routers/` 下新建文件，在 `main.py` 中 `include_router`
- **错误处理**：业务异常统一抛出，由 `main.py` 的 `global_exception_handler` 捕获
- **健康检查**：`GET /health` 已内置，不要修改

## 启动方式

```bash
pip install -r requirements.txt
python main.py
```

默认端口 8000，可通过环境变量 `PORT` 覆盖。
```

### AGENTS.md

Create as a symlink: `ln -s CLAUDE.md AGENTS.md`

### requirements.txt

```
fastapi
uvicorn[standard]
pydantic-settings
loguru
gunicorn
pytest
httpx
```

### .env.example

```
APP_NAME=backend
HOST=0.0.0.0
PORT=8000
DEBUG=false
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_MAX_SIZE_MB=10
LOG_BACKUP_COUNT=5
```

### Makefile

```makefile
.PHONY: install run run-prod test docker-build

install:
	pip install -r requirements.txt

run:
	python main.py

run-prod:
	gunicorn main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000

test:
	pytest -q

docker-build:
	docker build -t backend:dev .
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN useradd -r -u 10001 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
services:
  backend:
    image: backend:dev
    build: .
    env_file:
      - .env
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
```

### tests/test_health.py

```python
from fastapi.testclient import TestClient

from main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## 生产部署与国内环境

- 开发启动：`python main.py`，只有 `DEBUG=true` 时启用 reload。
- 生产启动：`gunicorn main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000`。
- 构建验证：`pip install -r requirements.txt && pytest -q`。
- Docker 验证：`docker build -t backend:dev . && docker compose up -d`，再执行 `curl http://127.0.0.1:8000/health`。
- pip 国内源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`，生产建议使用公司内网 PyPI。
- 回滚：镜像使用明确 tag，例如 `backend:20260531-1`，保留上一版本镜像并用 `docker compose up -d` 回切。
- 生产注意：不要把真实密码写入 `.env.example`，不要把 `ALLOWED_ORIGINS` 设置为 `*`。

### .gitignore

```
__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv/
venv/
env/
*.egg-info/
dist/
build/
logs/
*.log
.idea/
.vscode/
*.swp
*.swo
.DS_Store
```

### README.md

Use the following template, replacing `{project_name}` with the actual project name:

```markdown
# {project_name}

## Description

TODO: Add project description.

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
python main.py
```

The server will start at `http://localhost:8000`.

## Configuration

All configuration is managed via environment variables or `.env` file:

| Key       | Default   | Description       |
|-----------|-----------|-------------------|
| APP_NAME         | backend      | Application name           |
| HOST             | 0.0.0.0      | Server host                |
| PORT             | 8000         | Server port                |
| DEBUG            | False        | Debug mode                 |
| LOG_LEVEL        | INFO         | Logging level              |
| LOG_FILE         | logs/app.log | Log file path              |
| LOG_MAX_SIZE_MB  | 10           | Max log file size (MB)     |
| LOG_BACKUP_COUNT | 5            | Number of log files to keep|

## Directory Structure

```
backend/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── app/
│   ├── config.py        # Configuration (BaseSettings)
│   ├── routers/         # API route handlers
│   ├── models/          # Database / ORM models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
└── logs/                # Log files (auto-generated)
```
```
