# {workspace_name} 视频工作区

## 项目概述

视频制作工作区，用于产品演示、宣传片、技术讲解动画的制作。使用编程方式（Remotion / HyperFrames / Manim）生成视频，配合录屏工具完成产品展示。

## 目录结构

```
{workspace_root}/
├── CLAUDE.md
├── AGENTS.md
├── 01_视频草稿/
│   └── {项目名}/
│       ├── 源文件/        ← Remotion/HyperFrames/Manim 代码
│       ├── 素材/          ← 项目专属素材
│       ├── 产物/          ← 渲染产物（中间版本 + 终版）
│       └── 项目说明.md     ← 项目信息
│
├── 02_发布中心/
│   ├── YYYY-MM/
│   └── ...
│
└── 共享素材/              ← 跨项目复用（Logo、字体、音乐）
```

## 工具链

| 工具 | 用途 | 渲染命令 |
|------|------|---------|
| Remotion | 产品宣传片、批量生成 | `npx remotion render` |
| HyperFrames | 图文视频、字幕、转场 | `npx hyperframes render` |
| Manim | 技术原理讲解、算法可视化 | `manim -qh scene.py` |

**共同依赖**：FFmpeg

**Manim 注意**：需要 Python 3.12（3.14 不兼容）

## 约束

- 视频项目不进 git（文件太大），用目录结构管理版本
- 渲染输出统一用 MP4（H.264）
- 素材版权自查：使用外部素材前确认授权
