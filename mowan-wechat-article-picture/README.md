<div align="center">

# 公众号文章配图总控

### 给 Markdown 公众号草稿生成封面、正文配图，并自动整理回文章

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-black)](https://github.com/limowan/mowan-skill)

</div>

> 一键配图：封面 + 正文插图 + 关注卡片，全流程 AI 辅助

## 功能简介

`mowan-wechat-article-picture` 是一个公众号文章配图总控 Skill。

它负责把一篇 Markdown 公众号草稿，从“只有正文”推进到“有封面、有正文插图、有固定关注卡片、图片路径已回填”的状态。

主要能力：

- 从文章路径识别公众号账号。
- 首次使用时引导用户逐项配置，不要求用户直接手写 JSON。
- 按账号配置生成公众号封面提示词和封面图。
- 复用 `baoyu-article-illustrator` 的正文配图分析和风格体系。
- 正文配图生成前必须给 3 个风格候选，由用户确认后再继续。
- 在 Codex 环境默认使用内置 `image_gen` 直出 PNG。
- 在 Claude Code 或其它环境优先检查配置中的生图 Skill。
- 按配置决定是否使用封面头像、是否追加关注卡片、正文配图右下角是否展示公众号名称。
- 把最终 PNG 用相对路径插回 Markdown。

## 安装方式

在 Claude Code 中说：

```
帮我安装一下 https://github.com/limowan/mowan-skill/tree/main/mowan-wechat-article-picture 这个 Skill
```

## 使用方法

在 Agent 里直接说：

```text
用 mowan-wechat-article-picture 给这篇文章做封面和配图：
<文章路径>
```

执行时会先做这些检查：

- 读取 `config.json`。
- 根据 `accounts[].pathMatchers` 判断公众号。
- 输出确认句，例如：`识别到公众号：<accountName>，文章类型：<短篇/长文/未知>`。
- 检查头像、关注卡片、输出目录和生图方式。
- 给出 3 个正文配图风格候选，等待用户确认。

如果路径无法判断公众号，Skill 必须先问用户确认，不允许猜。

## 配置说明

复制 `config.example.json` 为 `config.json`，再填入自己的真实路径。

首次使用时，Skill 会优先通过 AskUserQuestion 工具逐项询问配置项。如果当前环境没有这个工具，也会用普通对话一步步问清楚，不会直接把整份 JSON 丢给你填。

关键字段：

- `vaultRoot`：Obsidian Vault 根目录，不是图片输出目录。
- `defaultImageProvider`：默认生图方式，Codex 环境建议 `codex_image_gen`。
- `requiredSkills`：正文配图流程依赖的 Skill，例如 `baoyu-article-illustrator`。
- `imageGenerationSkills`：非 Codex 环境可用的生图 Skill 列表。
- `accounts[].accountName`：公众号名称。
- `accounts[].pathMatchers`：用于从文章路径判断公众号的关键词。
- `accounts[].needsCoverAvatar`：封面是否需要头像参考。
- `accounts[].coverAvatarPath`：封面头像路径。
- `accounts[].appendFollowCard`：文章底部是否追加关注卡片。
- `accounts[].followCardPath`：关注卡片路径。
- `accounts[].showAccountNameOnArticleImages`：正文配图右下角是否展示公众号名称，默认关闭。
- `accounts[].outputRoot`：该公众号图片产物的根目录。

## 输出结构

每篇文章会在对应账号的 `outputRoot` 下创建独立目录：

```text
outputRoot/
└── 2026年/
    └── 2026-04-27-文章标题/
        ├── 提示词-封面.md
        ├── 提示词-插图-主题.md
        ├── 封面.png
        └── 插图-主题.png
```

Markdown 图片引用必须指向这个单篇文章目录里的最终 PNG，并优先转换成相对文章文件的相对路径。

## 工作原理

```text
读取文章路径
    ↓
读取 config.json；缺失时进入首次配置向导
    ↓
识别公众号账号
    ↓
生成封面提示词与封面图
    ↓
分析正文插图位置
    ↓
给 3 个正文配图风格候选，等待用户确认
    ↓
生成正文插图提示词与 PNG
    ↓
回填 Markdown 图片引用
    ↓
按配置追加关注卡片
```

## 隐私与数据安全

- 文章、头像、关注卡片和生成图片都保存在你的本地目录。
- Skill 本身不收集、不上传、不托管你的公众号素材。
- 生图方式由你当前环境决定，实际使用的工具会在执行时告诉你。

## 依赖 Skill

正文配图分析依赖 `baoyu-article-illustrator`。

如果你的环境里没有这个 Skill，可以让 Agent 安装：

```text
https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-article-illustrator/SKILL.md
```

## License

MIT License © [墨玩AI](https://github.com/limowan)

## 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱

> 让公众号配图不再是创作的瓶颈。

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
