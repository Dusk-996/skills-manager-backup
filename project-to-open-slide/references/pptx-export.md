# 图片型 PPTX 导出

Open Slide 1.12.1 原生支持“导出图片 PPTX”。每页以高分辨率图片写入 16:9 幻灯片。

优点：视觉结果稳定，与浏览器页面一致，避免二次排版偏差。

限制：PowerPoint 中不能单独编辑文字、图形、图表和连线；修改内容应回到 Open Slide 源码重新导出。

验收至少包括：

- PPTX 是有效 ZIP/OOXML。
- 幻灯片数量与 Open Slide 页数一致。
- 每页包含对应图片。
- PowerPoint 或 LibreOffice 可打开。
- 渲染抽查无明显视觉偏差。
