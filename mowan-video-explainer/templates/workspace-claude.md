# {workspace_name} 视频工作区

## 项目概述

视频制作工作区，用于产品演示、宣传片、技术讲解动画的制作。使用编程方式（Remotion / HyperFrames / Manim）生成视频，配合录屏工具完成产品展示。

默认视频方向：面向小白、短视频感、有记忆点、有趣但不标题党。AI 需要先做视频设计方案，再写脚本和做动画。工具不限于 Remotion，可按效果需要混合 HTML/GSAP/SVG/Three.js/浏览器录制等方式。

## 目录结构

```
{workspace_root}/
├── CLAUDE.md
├── AGENTS.md
├── 01_视频草稿/
│   └── {项目名}/
│       ├── 源文件/        ← Remotion/HyperFrames/Manim 代码
│       │   ├── remotion/
│       │   ├── hyperframes/
│       │   ├── manim/
│       │   └── effects/   ← HTML/GSAP/SVG/Three.js 等临时特效工程
│       ├── 素材/          ← 项目专属素材
│       │   ├── 视频片段/  ← 各段渲染片段
│       │   ├── 配音文件/  ← TTS 或真人录音
│       │   └── 最终视频/  ← 最终合成视频
│       └── 项目说明.md     ← 项目信息
│
├── 02_发布中心/
│   ├── YYYY-MM/
│   └── ...
│
└── 共享素材/              ← 跨项目复用（Logo、字体、音乐）
```

**命名规范**：
- 业务文件夹名用中文：`源文件/`、`素材/`、`产物/`、`视频片段/`、`配音文件/`、`最终视频/`
- 工具工程目录保留英文：`源文件/remotion/`、`源文件/hyperframes/`、`源文件/manim/`、`源文件/effects/`
- 草稿项目命名：`{项目名}`（如「飞书转公众号-产品宣传」）
- 发布中心按月份归档：`YYYY-MM`

**组织规则**：
- 每个视频项目在 `01_视频草稿/` 下独立建文件夹
- 新建项目时自动创建 `项目说明.md`
- 出稿后终版视频移到 `02_发布中心/{月份}/`，草稿中间产物可删
- `共享素材/` 放跨项目复用的素材，项目专属素材放项目目录内

## 视频设计原则

- 先设计，再制作：先明确核心一句话、开场 Hook、记忆点、画面风格，再写脚本。
- 面向小白：少术语，多例子，多类比。
- 短视频节奏：前 5-10 秒抓人，每 30-45 秒有一次节奏变化。
- 有记忆点：至少保留 1 个核心比喻、1 句金句、1 个视觉锚点。
- Remotion 不是 PPT 翻页工具，要主动设计构图、转场和视觉系统。
- 动效从内容需求出发设计，参考 `references/effects-thinking.md` 的思考框架，不限于任何固定列表。
- 工具按效果选：Remotion 做主片，HTML/GSAP/SVG 做特效素材，Three.js/Canvas 做程序化或 3D 场景，最后统一合成。

## 工具链

| 工具 | 用途 | 创建项目 | 预览 | 渲染 |
|------|------|---------|------|------|
| Remotion | 产品宣传片、数据可视化、批量生成 | `npx create-video@latest` | `npx remotion preview` | `npx remotion render` |
| HyperFrames | 图文视频、字幕、转场、标题卡 | `npx hyperframes init` | `npx hyperframes preview` | `npx hyperframes render` |
| Manim | 技术原理讲解、算法可视化 | 手动创建 .py | — | `manim -qh scene.py` |

**共同依赖**：FFmpeg（Remotion、HyperFrames、Manim 都需要）

**Manim 运行注意**：如果系统安装了多个 Python 版本，Manim 需要 Python 3.12（3.14 不兼容），运行时用 `py -3.12 -m manim` 或对应的 Python 3.12 路径。

## Skill 路由

| 场景 | 路由到 |
|------|--------|
| 编程做视频（React 组件方式） | 直接用 Remotion |
| 快速图文视频/字幕/转场/标题卡 | `hyperframes` + `hyperframes-cli` |
| 安装视频组件/模块 | `hyperframes-registry` |
| 技术原理/算法动画 | 直接用 Manim |
| 下载 YouTube 素材 | `video-downloader` |

## 约束

- 视频项目不进 git（文件太大），用目录结构管理版本
- 渲染输出统一用 MP4（H.264），除非平台有特殊要求
- 素材版权自查：使用外部素材前确认授权
