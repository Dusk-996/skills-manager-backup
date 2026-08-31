---
name: project-to-open-slide
description: Use when converting technical projects, local documents, images, web pages, architecture ideas, or existing presentation materials into a Chinese Open Slide technical deck and image-based PPTX.
---

# Project to Open Slide

把“用户诉求 + 本地资料 + 网页来源 + 设计理念”转换为有证据约束、可验收的 Open Slide 演示。固定使用 `@open-slide/core 1.12.1`；先设计，后生成。

## 强制工作流

### 1. 建立材料清单

先运行：

```powershell
python scripts/inspect_materials.py --source <本地路径> --url <网页地址> --output <manifest.json>
```

- 默认排除 `.env`、密钥、Token、Webhook、证书、`.git`、`node_modules`、`dist`、日志和数据目录。
- 源材料保持只读。
- Word、PDF、PPTX 分别使用对应文档技能提取结构；网页必须核对来源和日期。
- 只查看与故事线相关的文件片段和候选图片，禁止无差别读取整个项目。

详细规则见 `references/input-contract.md`。

### 2. 分析并一次性补问

只询问材料无法确定且会改变结果的问题：目标、受众、场景、时长、页数、文字密度、视觉方向、动画、必留原图、网页/生成图权限、演讲者备注、真实运行数据。

已经明确的信息不得重复询问。

输出并等待确认：

- 材料事实摘要与风险。
- Evidence Ledger。
- 推荐故事线、逐页标题和页面目标。
- 图示、图片、颜色、字体和布局方案。
- 不能作为事实使用的内容。

**用户确认设计方案前，禁止生成页面。**

### 3. 设计确认后询问输出位置

必须明确询问：

> 请指定 Open Slide/PPT 输出目录。

同时确认或生成演示 ID、PPTX 文件名，并询问是否启动预览、是否创建本地 Git 提交。

运行：

```powershell
scripts/resolve_target.ps1 -Target <输出目录> -Id <演示ID>
```

- 空目录：允许初始化。
- 已有 Open Slide 项目：只新增 `slides/<id>/`。
- 非空且不是 Open Slide 项目：停止并列出冲突文件。
- `slides/<id>/` 已存在：停止，禁止覆盖。

目标规则见 `references/target-contract.md`。

### 4. 初始化或复用目标项目

空目录运行：

```powershell
scripts/bootstrap_target.ps1 -Target <输出目录>
```

模板固定为：

- `J:\skywalking\open-slide-studio\runtime`
- `@open-slide/core 1.12.1`
- Git Commit `9a213fe75f7b13fcd2cb3c49a0ab8241617148a5`

模板缺失或版本不符时停止，不得静默联网修复。不得在普通制作任务中执行 `git pull`。

### 5. 生成

目标项目必须包含：

```text
slides/<id>/index.tsx
slides/<id>/assets/
.open-slide-work/<id>/brief.md
.open-slide-work/<id>/outline.md
.open-slide-work/<id>/decisions.md
.open-slide-work/<id>/source-manifest.json
.open-slide-work/<id>/evidence-ledger.json
.open-slide-work/<id>/qa-report.json
exports/<id>/<id>.pptx
exports/<id>/html/
```

读取目标项目的 `.agents/skills/create-slide/SKILL.md` 和 `slide-authoring/SKILL.md` 后，一次生成全部页面。没有运行证据的数据标注“场景示意”。真实截图必须来自用户材料或可验证运行环境。

### 6. 验收与导出

依次执行：

```powershell
corepack pnpm install --frozen-lockfile
corepack pnpm build
python scripts/validate_open_slide.py --slide-dir <slides/id> --ledger <ledger.json>
node scripts/export_image_pptx.mjs --target <输出目录> --deck <id> --output <pptx>
python scripts/verify_delivery.py --target <输出目录> --id <id> --expected-pages <页数>
```

构建后检查全部页面：固定 1920×1080、无滚动、越界、遮挡、控制台错误、外链图片和敏感信息。只修复失败页面。

图片型 PPTX 规则见 `references/pptx-export.md`。

## Evidence Ledger

每条关键结论记录来源、证据类型、允许写法和风险。配置存在不等于已运行；文档声明不等于已验证；无法核验的运行结论禁止写成事实。

## 最终回复

报告 Open Slide 源码、HTML、PPTX、工作记录、验收报告和预览地址。必须提示：

> 图片型 PPTX 与 Open Slide 视觉一致，但在 PowerPoint 中不能单独编辑文字和图形。

同时报告扫描文件数、实际读取文件数、提问轮次、生成轮次和修复轮次。
