# 材料输入契约

## 支持材料

项目目录、Markdown/TXT、YAML/JSON、代码配置、Word、PDF、PPTX、图片、截图、微信文章、官方文档、GitHub 和普通网页。

## 读取原则

1. 先清单后阅读；先目录结构后正文。
2. Word/PDF 先提取目录，再按相关章节读取。
3. 图片先记录尺寸、哈希和用途，只查看候选图。
4. URL 先记录标题、来源、发布日期和必要段落；联网前通知用户。
5. 不读取 `.env`、密钥、Token、Webhook、证书和密码。
6. 排除 `.git`、`node_modules`、`dist`、日志、缓存和数据目录。
7. 源材料只读，派生内容写入目标项目的 `.open-slide-work/<id>/`。

## Evidence Ledger

建议字段：`claim`、`source`、`evidence_type`、`allowed_in_slide`、`wording`、`risk`。运行状态必须有命令输出、截图或用户明确确认。
