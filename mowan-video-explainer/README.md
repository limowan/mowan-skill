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
🤖 &nbsp;自动选择最合适的工具链（Manim / HyperFrames / Remotion）<br>
🎙️ &nbsp;支持 TTS 自动配音和真人录音两种模式<br>
📐 &nbsp;从脚本到动画到合成，全流程 AI 辅助

</td></tr>
</table>

<br>

[✨ 功能](#-功能) · [🎯 适用场景](#-适用场景) · [⚡ 安装](#-安装) · [🚀 使用](#-使用) · [🔧 工具链](#-工具链) · [📋 依赖](#-依赖)

</div>

---

## ✨ 功能

- **素材分析**：读取 PDF、文章、文档，提取核心内容和结构
- **智能选型**：根据内容类型自动推荐最合适的视频工具组合
- **脚本生成**：AI 生成完整逐字稿（旁白 + 画面描述 + 时间轴），也支持用户自己提供
- **动画制作**：自动生成 Manim/HyperFrames/Remotion 代码并渲染
- **配音处理**：TTS 自动配音（edge-tts）或真人录音匹配（Whisper 转写）
- **视频合成**：FFmpeg 合并视频、音频、字幕、BGM，输出终版

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
3. **创建项目** — 在视频工作区建好目录结构
4. **写脚本** — AI 生成或你自己提供，支持带时间戳格式
5. **做动画** — 逐段生成动画代码并渲染
6. **配音** — TTS 自动生成或真人录音匹配
7. **合成** — 拼接视频+音频+字幕+BGM，输出终版

## 🔧 工具链

Skill 会根据视频类型自动选择工具：

| 工具 | 擅长 | 典型场景 |
|------|------|---------|
| **Manim** | 算法动画、数学可视化、技术原理 | 论文解读、技术科普 |
| **HyperFrames** | 图文视频、标题卡、转场、字幕 | 文章解读、产品演示 |
| **Remotion** | React 组件化视频、品牌化、批量生成 | 产品宣传片、系列视频 |

三种工具可以混合使用。比如技术科普视频：Manim 做核心动画 + HyperFrames 做开场和结尾。

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

> Manim 需要 Python 3.12（3.14 不兼容）。如果系统有多个 Python 版本，用 `py -3.12` 指定。

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

每个视频项目自动创建标准目录：

```
{视频工作区}/01_视频草稿/{项目名}/
├── 源文件/
│   ├── manim/           ← Manim 场景代码
│   ├── hyperframes/     ← HyperFrames 项目
│   └── remotion/        ← Remotion 项目
├── 素材/                ← 项目专属素材
├── 产物/
│   ├── clips/           ← 各段渲染片段 + 音频
│   └── final/           ← 最终合成视频
└── 项目说明.md
```

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
