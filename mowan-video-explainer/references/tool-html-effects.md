# HTML / GSAP / SVG / Three.js 特效制作规则

## 适用场景

当某段更像"动效素材"而不是完整视频场景时，用 HTML/GSAP/SVG 单独制作，再合成进主视频。

## 目录结构

```bash
源文件/effects/
├── spotlight-title/
├── svg-assembly/
└── typer/
```

## 制作规则

- 优先做成自包含 HTML，方便浏览器预览
- 需要透明背景时，导出 PNG 序列帧或 ProRes 4444 MOV，再合成
- 用 GSAP 做时间线时，关键动画要可复现：明确 duration、ease、stagger
- SVG 组装类动效要先拆主体和零件，再设计飞入、回弹、旋转、速度感
- 聚光灯/扫光/揭示类动效适合标题和金句，不要整片滥用

## 浏览器录制 / Canvas / Three.js

当需要网页交互、程序化背景、3D 场景或复杂 Canvas 动画时，可以直接做一个本地页面再录制：

- 适合：3D 隐喻、动态背景、流程演示、网页产品真实操作
- 要求：先预览确认不卡顿、不黑屏、不遮挡字幕，再录制或导出
- 输出仍进入 `产物/视频片段/`，最后统一合成

## 已有动效 Skill

如果已安装以下 Skill，可以优先调用：

- `svg-assembly-animator`：SVG 零件组装动画
- `light-spotlight-render`：聚光灯扫字/揭示动画
- `ruler-progress-render`：尺子进度条动画
- `claude-typer`：CLI 风格打字动画

没有对应 Skill 时，按当前项目临时实现即可。
