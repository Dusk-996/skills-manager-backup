# 输出目录契约

## 判定

| 状态 | 行为 |
|---|---|
| 空目录 | 从固定模板初始化 |
| Open Slide 项目 | 复用，只新增当前演示 |
| 非空非 Open Slide | 停止并列出冲突文件 |
| `slides/<id>` 已存在 | 停止，禁止覆盖 |

Open Slide 项目至少应有 `package.json`、固定版本 `@open-slide/core` 和 `slides/`。

## 初始化复制

仅复制 `package.json`、`pnpm-lock.yaml`、`open-slide.config.ts`、`tsconfig.json`、`.agents/skills/`。不复制 `node_modules`、`dist`、缓存和已有演示。

依赖安装使用：

```powershell
corepack pnpm install --frozen-lockfile
```
