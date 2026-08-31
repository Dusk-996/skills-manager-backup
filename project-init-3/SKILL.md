---
name: project-init
description: "Initialize production-cautious DevOps projects for Shell, Python, or Golang, including backend/platform APIs, collector agents, executor agents, CLIs, and shell tools. Use when the user wants to create/init/scaffold a DevOps tool, platform service, backend API, agent, CLI, or automation project. Prefer Shell for simple single-host automation, Python for platform APIs and data/API tooling, and Go for distributed agents, single-binary delivery, or deep Kubernetes work."
---

# 项目初始化

该技能用于初始化面向运维工程实践的 Shell / Python / Golang 项目，涵盖目录结构、日志、配置、Web 框架、错误处理、CORS、健康检查、容器化、部署说明、git 初始化、.gitignore 和 README 生成。

默认目标不是“能跑 demo”，而是生成一个适合继续生产化交付的谨慎骨架：配置可覆盖、密钥不入库、日志适合容器、启动方式区分开发/生产、提供验证和回滚入口。

## 个人工具链入口

- 生成项目前，优先读取 `../profile/ops-engineer-cn.yml`，按其中的默认技术栈、国内镜像源和安全策略设置项目骨架。
- 生成或验收后，建议运行 `../scripts/devops-skillctl.ps1 accept`；需要留档时运行 `../scripts/devops-skillctl.ps1 report` 生成 `acceptance-report.md`。
- 如果 Docker 或 kubectl 不存在，只做静态验收并标记跳过，不要自动执行真实部署命令。

## 工作流程

1. 向用户确认必要问题（如果上下文中已经明确则跳过）：
   - **项目类型**：`shell-tool`、`backend`、`platform-api`、`collector-agent`、`executor-agent`、`cli`。
   - **语言**：Shell、Python 还是 Golang。
   - **部署形态**：本机/systemd、Docker Compose、Kubernetes，或暂不生成部署文件。

2. 默认选型规则：
   - 简单单机巡检、备份、清理、批处理：优先 Shell。
   - 运维平台 API、内部工具后端、数据处理、对接大量 SDK：优先 Python。
   - 常驻 agent、大量主机分发、低资源占用、K8s 深度操作：优先 Go。
   - 如果用户已指定语言或团队主栈，优先尊重用户选择。

3. 根据用户选择，读取对应的模板文件，生成完整的项目脚手架。

4. 生成完毕后，输出创建内容摘要、生产化检查清单、验证命令和下一步部署建议。

## 初始化前检查

- 检查当前目录是否已有 git 仓库（`git rev-parse --git-dir`），如果没有则执行 `git init -b main`（旧版本 git 没有 `-b` 参数时，先 `git init` 再 `git symbolic-ref HEAD refs/heads/main`）。
- 根据类型在 `backend/` 或 `agent/` 目录下创建项目。
- 所有需要文件的目录至少包含一个占位文件或 `__init__.py`。
- 创建 `logs/` 目录，放入 `.gitkeep` 保持目录存在。

## 分支策略（脚手架生成后执行）

在所有项目文件、`.gitignore`、`README.md`、`CLAUDE.md` 等都写入完毕后，按下面顺序建立分支：

1. **确保在 `main` 分支上完成首次提交**：
   - `git add -A`
   - `git commit -m "chore: scaffold project via project-init"`（如果当前不在 `main`，先 `git checkout -b main` 或 `git branch -M main`）。
   - `main` 是正式发布分支，初始化之后默认不再直接在上面提交。
2. **创建并切换到 `test` 开发分支**：
   - `git checkout -b test`
   - 后续所有开发都在 `test` 上进行；`main` 仅用于发布正式环境。
3. 如果仓库在初始化前已经存在并且已有 `test` 分支，直接 `git checkout test` 而不是重新创建，避免覆盖既有工作。
4. 最终输出摘要时，明确告知用户：
   - 当前所在分支是 `test`；
   - `main` 已保留为正式发布分支，请勿直接在 `main` 上开发；
   - 发布到正式环境时，从 `test`（或后续派生的 feature 分支）合并回 `main`。

## 模板参考

根据用户选择，从本技能的 `references/` 目录读取对应的模板文件：

| 语言   | 类型    | 模板文件                            |
|--------|---------|-------------------------------------|
| Python | backend / platform-api | `references/python_backend.md` |
| Python | collector-agent / executor-agent / cli | `references/python_agent.md` |
| Go     | backend / platform-api / cli | `references/go_backend.md` |
| Go     | collector-agent / executor-agent | `references/go_agent.md` |
| Shell  | shell-tool | 按本文件“Shell 工具标准”生成 |

读取选定的模板文件，严格按照模板内容生成所有项目文件。

## 通用标准（所有模板共享）

生成或审查任何 DevOps 项目时，先按 `references/acceptance-rules.md` 校验固定输出和硬失败项。

### .gitignore
生成语言对应的 .gitignore 文件，始终包含 `logs/`。

### README.md
生成 README.md，包含以下章节：
- 项目名称与描述
- 启动/运行方式
- 配置说明（列出所有配置项及默认值）
- 目录结构概览

### 健康检查
所有 Web 项目暴露 `GET /health` 端点，返回 `{"status": "ok"}`。

### 端口配置
端口始终定义在配置文件/类中，并提供合理的默认值（Python 默认 8000，Go 默认 8080）。

### CORS
所有 Web 项目默认加载 CORS 中间件，但生产环境必须通过配置项限制来源。开发环境可以允许所有来源，README 中必须明确生产环境不要使用 `*`。

### 生产交付文件
Web 项目默认生成或说明以下文件：
- `.env.example` 或 `config.example.yaml`：只放示例值，不放真实密码。
- `Makefile`：至少包含 `run`、`test`、`build`、`docker-build`。
- `Dockerfile`：使用非 root 用户，区分构建和运行阶段。
- `docker-compose.yml`：用于本地或小规模部署，镜像 tag 不使用 `latest`。
- README 中包含生产启动、构建、健康检查、回滚说明。

Agent 项目默认生成或说明：
- systemd unit 示例。
- 安装/卸载命令。
- 资源限制建议。
- 日志与配置文件位置。
- 执行型 agent 必须有超时、并发上限、命令白名单说明。

### 国内网络环境
README 必须包含国内环境依赖下载建议：
- pip：清华源或公司内网 PyPI。
- npm：npmmirror 或公司内网 npm registry。
- Go：`GOPROXY=https://goproxy.cn,direct`。
- Docker：说明镜像拉取失败时的替代镜像、离线导入、私有仓库推送方案。

### Shell 工具标准
生成 Shell 工具时，必须包含：
- `set -Eeuo pipefail`。
- `usage()` 帮助。
- `--dry-run` 或执行前确认机制，危险操作必须默认不直接执行。
- 日志函数：`log_info`、`log_warn`、`log_error`。
- 参数校验和退出码约定。
- 生产操作说明：影响范围、备份、验证、回滚。

## 危险操作门禁

当项目或脚本涉及删除文件、清空数据库、重启服务、修改防火墙、`rm -rf`、`kubectl delete`、`docker system prune`、修改 Docker/containerd/Nginx/MySQL/K8s 核心配置时，必须先输出：

1. 影响范围
2. 执行前备份
3. 执行步骤
4. 验证命令
5. 回滚方案
6. 生产环境注意事项

## CLAUDE.md 放置规则

- `CLAUDE.md` 和 `AGENTS.md` 必须创建在 **git 仓库根目录**，而不是 `backend/` 或 `agent/` 子目录下。只有放在仓库根目录，Claude Code 才会自动读取。
- 如果项目文件在子目录（如 `backend/`、`agent/`）下创建，`CLAUDE.md` 仍然要放在上一级的仓库根目录。

## CLAUDE.md 内容组合规则

生成 `CLAUDE.md` 时，**必须**按以下顺序拼接两段内容，中间用一行分隔符 `---` 隔开：

1. **通用行为准则（preamble）**：从 `references/claude_md_preamble.md` 读取，原样写入，**不要改动**。这是所有项目共享的 LLM 编码行为约束。
2. **项目特定内容**：从对应语言/类型的模板（如 `references/python_backend.md`）的 `### CLAUDE.md` 段落读取，替换占位符（`{project_name}`、`{module}` 等）后写入。

最终 `CLAUDE.md` 的结构应当是：

```
<preamble 全部内容>

---

<项目特定内容（# {project_name} 开头那段）>
```

## 注意事项

- 不要让用户手动创建文件，所有文件自动生成。
- 脚手架生成后，提醒用户安装依赖并执行验证（例如 `pip install -r requirements.txt && pytest`、`go mod tidy && go test ./... && go build ./...`）。
- 如果用户提供了项目名称，在 README 和模块名中使用该名称；否则使用目录名。
- 不要默认生成 `latest` 镜像 tag，不要默认使用生产宽松 CORS，不要把 mock/dev 配置当成生产配置。
