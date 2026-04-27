<div align="center">

# 🎬 墨玩视频解读

### *把技术报告、产品文档、文章变成人人看得懂的科普视频*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-black)](https://github.com/limowan/mowan-skill)
[![Cursor](https://img.shields.io/badge/Cursor-Skill-blue)](https://github.com/limowan/mowan-skill)

<br>

<table>
<tr><td align="left">

🎯 &nbsp;输入一篇技术报告/产品文档/文章，输出一个完整的科普视频<br>
🎨 &nbsp;先出 2-3 个视频方案对比，确认后再制作<br>
🤖 &nbsp;AI 自由选择工具和创造动效，不限于固定模板<br>
🎙️ &nbsp;支持 TTS 自动配音和真人录音两种模式<br>
📐 &nbsp;从方案设计到脚本到动画到合成，全流程 AI 辅助

</td></tr>
</table>

<br>

[✨ 功能](#-功能) · [🎯 适用场景](#-适用场景) · [⚡ 安装](#-安装) · [🚀 使用](#-使用) · [🔧 工具链](#-工具链) · [📋 依赖](#-依赖)

</div>

---

## ✨ 功能

- **素材分析**：读取 PDF、文章、文档，提取核心内容和结构
- **智能选型**：根据内容类型自动推荐最合适的视频工具组合
- **方案对比**：出 2-3 个差异明显的视频方案，用户选择或混搭后再制作
- **脚本生成**：AI 生成完整逐字稿（旁白 + 画面描述 + 时间轴），也支持用户自己提供
- **动画制作**：自动生成 Manim/HyperFrames/Remotion/HTML/GSAP/SVG/Three.js 等动画并渲染
- **配音处理**：TTS 自动配音（edge-tts）或真人录音匹配（Whisper 转写）
- **GPU 渲染**：Windows + NVIDIA 优先使用 FFmpeg NVENC，MacBook 优先使用 Remotion 硬件加速
- **视频合成**：FFmpeg 合并视频、音频、字幕、BGM，画质优先输出终版

## 🎯 适用场景

| 场景 | 示例 |
|------|------|
| 技术科普 | 把 AI 论文/技术报告做成 5 分钟科普视频 |
| 产品介绍 | 把产品文档做成宣传片或演示视频 |
| 文章解读 | 把长文章做成图文解读视频 |
| Skill/工具演示 | 把 README 做成操作演示视频 |
| 数据可视化 | 把数据报告做成动态图表视频 |

## ⚡ 安装

在 Claude Code / Cursor / Codex 等支持 Skill 的 AI 编程工具中输入：

```
帮我安装一下 https://github.com/limowan/mowan-skill/tree/main/mowan-video-explainer 这个 Skill
```

## 🚀 使用

安装后，直接对 AI 说：

```
帮我做个视频解读这篇报告
```

或者更具体：

```
把这个 PDF 做成一个 5 分钟的科普视频，面向技术小白，发 B 站
```

Skill 会引导你完成以下流程：

1. **环境检测** — 自动检查依赖，缺什么装什么
2. **素材分析** — 读取你的素材，推荐视频类型和工具
3. **视频方案设计** — 出 2-3 个方案对比（视觉风格、动效策略、工具组合），你选一个或混搭
4. **创建项目** — 在视频工作区建好目录结构
5. **写脚本** — AI 生成或你自己提供，支持带时间戳格式
6. **做动画** — 逐段生成动画代码并渲染
7. **配音处理** — TTS/真人录音 + 字幕生成
8. **合成终版** — 视频+音频+BGM+字幕，输出终版

## 🔧 工具链

Skill 会根据视频类型自动选择工具：

| 工具 | 擅长 | 典型场景 |
|------|------|---------|
| **Manim** | 算法动画、数学可视化、技术原理 | 论文解读、技术科普 |
| **HyperFrames** | 图文视频、标题卡、转场、字幕 | 文章解读、产品演示 |
| **Remotion** | React 组件化视频、品牌化、批量生成 | 产品宣传片、系列视频 |
| **HTML / GSAP / SVG** | 特效片头、打字机、聚光灯、SVG 组装 | 金句揭示、Logo reveal、动效素材 |
| **Three.js / Canvas** | 3D、程序化背景、循环视觉 | 抽象隐喻、氛围 B-roll |

工具可以混合使用。比如技术科普视频：Manim 做核心动画 + Remotion 做主片 + HTML/GSAP 做标题 reveal 和 SVG 组装特效。

## 🎬 视频设计原则

默认方向是：给小白看，短视频感强，有记忆点，有趣但不标题党。

- 开头 5-10 秒必须有 Hook，让观众知道为什么值得看。
- 每支视频至少设计 1 个核心比喻、1 句可复述金句、1 个视觉锚点。
- Remotion 不是 PPT 翻页工具，要主动设计构图、转场、字幕节奏和视觉系统。
- 动效从内容需求出发设计，AI 自由选择和创造，不限于固定模板。
- 复杂内容拆成”问题 → 解释 → 例子 → 结论”，少术语，多大白话。

## 📋 依赖

### 必须

- **FFmpeg** — 视频编码和合成
  - Windows: 从 [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 下载
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

### 按需安装（Skill 会自动检测并提示）

| 依赖 | 用途 | 安装命令 |
|------|------|---------|
| Python 3.12 + Manim | 技术原理动画 | `py -3.12 -m pip install manim` |
| HyperFrames | 图文视频 | `npm install -g hyperframes` |
| Remotion | 产品宣传片 | `npx create-video@latest` |
| edge-tts | TTS 配音 | `pip install edge-tts` |
| Whisper | 真人录音转字幕 | `pip install openai-whisper` |
| GPU 硬件编码 | 加快最终 MP4 导出 | Windows + NVIDIA 使用 `h264_nvenc`；MacBook 使用 Remotion 硬件加速 |
| AI 生图能力 | 视频中的封面、背景、插图等图片素材 | Codex 用内置 `image_gen`；其它环境通过 `config.json` 配置生图 Skill |

> Manim 需要 Python 3.12（3.14 不兼容）。如果系统有多个 Python 版本，用 `py -3.12` 指定。

## ⚡ GPU 渲染策略

默认优先画质：源片要清晰，文件大小适中即可，上传平台通常还会二次压缩。

- Windows + NVIDIA：Remotion 生成画面，FFmpeg 使用 `h264_nvenc` 编码最终 MP4。
- MacBook：Remotion 使用 `--hardware-acceleration=if-possible`。
- 无可用 GPU：自动回退 CPU `libx264 -crf 18`。

注意：不要把已经压好的最终 MP4 再二次转 GPU；应从高质量中间产物或帧序列一次性编码终版，避免字幕和细线变糊。

## 🎙️ 配音方案

| 方案 | 说明 | 适合 |
|------|------|------|
| TTS 自动生成 | 使用 edge-tts（微软云端），零资源占用，秒级生成 | 快速出片、预览版 |
| 真人录音 | 你录音，Skill 用 Whisper 转写字幕并匹配动画时长 | 正式发布 |
| 先 TTS 后替换 | 先出 TTS 预览版，确认后录真人版替换 | 推荐流程 |

## 🎵 BGM

合成时可选混入背景音乐。以下免版权音源可放心商用（国内优先）：

- [Pixabay Music](https://pixabay.com/music/) — CC0 协议，国内可直接访问
- [FreePD.com](https://freepd.com/) — 公共领域，零限制
- [爱给网](https://www.aigei.com/) — 有免费可商用音乐区
- [淘声网](https://www.tosound.com/) — 免费音效和音乐
- [YouTube Audio Library](https://studio.youtube.com/channel/audio) — 完全免费，需科学上网

## 📁 项目结构

Skill 自身结构：

```
mowan-video-explainer/
├── SKILL.md                 ← Skill 入口（流程编排）
├── README.md
├── config.example.json      ← 生图能力配置示例
├── .gitignore
├── references/              ← 参考文档（按需读取）
│   ├── effects-thinking.md  ← 动效设计思考框架
│   ├── tool-manim.md        ← Manim 编码规范
│   ├── tool-hyperframes.md  ← HyperFrames 编码规范
│   ├── tool-remotion.md     ← Remotion 编码规范
│   ├── tool-html-effects.md ← HTML/GSAP/SVG 特效规则
│   └── rendering-and-encoding.md ← GPU + FFmpeg 编码
├── templates/               ← 项目模板
└── tools/                   ← 辅助脚本
```

每个视频项目自动创建标准目录：

```
{视频工作区}/01_视频草稿/{项目名}/
├── 源文件/
│   ├── manim/           ← Manim 场景代码
│   ├── hyperframes/     ← HyperFrames 项目
│   └── remotion/        ← Remotion 项目
├── 素材/                ← 项目专属素材
├── 产物/
│   ├── 视频片段/        ← 各段渲染片段
│   ├── 配音文件/        ← TTS 或真人录音
│   └── 最终视频/        ← 最终合成视频
└── 项目说明.md
```

业务文件夹使用中文；工具工程目录保持英文，例如 `源文件/remotion/`。

## 🔒 隐私与数据安全

- 所有处理在本地完成，不上传任何数据到外部服务器
- TTS 使用微软 Edge TTS 云端接口（仅发送文本，不发送其他数据）
- Whisper 转写完全在本地运行
- 生成的视频文件仅保存在你指定的本地目录

## 📄 License

MIT License

---

## 💬 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱

> 好内容不该只躺在文档里，做成视频让更多人看懂。

### 我的产品

| 产品 | 说明 | 使用方式 |
|------|------|----------|
| 🌐 墨成AI排版 | AI 快捷公众号文章排版工具 | [mocheng.mowan.work](https://mocheng.mowan.work) |
| 📱 问问毛选 | 毛选语录抽卡，真正的答案之书 | 微信搜「问问毛选」或扫码👇 |

<img src="../问问毛选小程序.png" width="160" alt="问问毛选小程序二维码">

### 关注我

| 平台 | 链接 |
|------|------|
| 📕 小红书 | [墨玩AI](https://xhslink.com/m/3Ks23mHtPrL) |
| 📺 B站 | [墨玩AI](https://space.bilibili.com/696270041) |
| 💬 公众号 | 微信搜「墨玩AI」 |

<img src="https://raw.githubusercontent.com/limowan/mowan-mc-type/main/wechat_qrcode.jpg" width="200" alt="墨玩AI 公众号二维码">
