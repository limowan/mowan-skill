<div align="center">

# 🎭 墨玩 CTI 人格侧写

### *"不是你说自己是谁，而是你留下的对话痕迹暴露了你是谁。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/limowan/mowan-CTI)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-teal)](https://github.com/limowan/mowan-CTI)
[![Codex](https://img.shields.io/badge/Codex-Skill-black)](https://github.com/limowan/mowan-CTI)

<br>

<table>
<tr><td align="left">

🧪 &nbsp;CTI（Conversation Trace Indicator）是一个娱乐向的聊天人格侧写系统<br>
💬 &nbsp;它通过分析你的对话痕迹，把你归类到 12 种聊天人格中的一种<br>
🎯 &nbsp;不是问卷测试，不是 MBTI 翻版 — 吃的是你真实的聊天记录

</td></tr>
</table>

<br>

[🎭 12 类人格](#-12-类人格) · [✨ 三种模式](#-三种测评模式) · [📦 数据来源](#-支持的数据来源) · [⚡ 安装](#-安装) · [🚀 使用](#-使用) · [🔧 工作原理](#-工作原理)

</div>

---

## 🎭 12 类人格

| 代号 | 名字 | 一句话 |
|------|------|--------|
| GGGG | 改改改改 | 你不是在做选择，你是在折磨做选择的人 |
| 3:00 | 凌晨三点兽 | 白天装死晚上发疯，你的灵魂倒时差了吧 |
| BLBL | 散装弹珠 | 你的脑子是不是没装盖子，想法全洒出来了 |
| SUIB | 随便侠 | 你嘴上说随便，全世界都知道你一点都不随便 |
| YDLH | 已读乱回 | 别人说了一万句，你精准忽略了九千九百九十九句 |
| 6+1 | 第六感战士 | 你做决定靠的不是逻辑，是一种玄学叫"我觉得" |
| DSSQ | 毒舌菩萨 | 嘴上在拆你台，手上在帮你撑 |
| ZZZZ | 人形咕咕机 | 你的deadline不是用来赶的，是用来突破的 |
| MFMF | 嘴硬王 | 明明在意得要死，嘴上说的全是"无所谓" |
| KBKB | 控制欲保安 | 你不是在聊天，你是在开项目管理会议 |
| QXJZ | 情绪锦鲤 | 你的情绪起伏比股票还刺激，身边人坐的是过山车 |
| WDWS | 十万个为什么 | 全世界都欠你一个解释，你是行走的十万个为什么 |

---

## ✨ 三种测评模式

<table>
<thead>
<tr>
<th width="33%" align="center">🅰️ 复制提示词分析</th>
<th width="33%" align="center">🅱️ 聊天记录导入</th>
<th width="33%" align="center">🅲 AI 记忆导入</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><sub>最轻量，零门槛</sub></td>
<td align="center"><sub>最准确，多来源</sub></td>
<td align="center"><sub>最真实，面具最薄</sub></td>
</tr>
<tr>
<td><sub>Skill 给你一段标准提示词 → 复制到 Gemini / GPT / Claude / 豆包 → 模型分析你的聊天行为 → 把结果贴回来 → Skill 做人格分类</sub></td>
<td><sub>直接导入飞书、钉钉、微信、Slack 等聊天记录，支持自动采集和手动上传多种方式</sub></td>
<td><sub>导入你和 AI 的对话历史（GPT / Claude / Gemini 导出），人跟 AI 聊天时社交面具最薄，暴露的是最真实的认知人格</sub></td>
</tr>
</tbody>
</table>

---

## 📦 支持的数据来源

B 模式支持以下数据来源：

| 来源 | 消息 | 文档 / Wiki | 表格 | 说明 |
|------|:----:|:-----------:|:----:|------|
| 🟢 飞书（自动采集） | ✅ API | ✅ | ✅ | 输入姓名，全自动拉取 |
| 🟡 钉钉（自动采集） | ⚠️ 浏览器 | ✅ | ✅ | 钉钉 API 不支持消息历史 |
| 🟣 Slack（自动采集） | ✅ API | — | — | 需管理员安装 Bot；免费版限 90 天 |
| 💬 微信聊天记录 | ✅ SQLite | — | — | 先用 WeChatMsg / PyWxDump / 留痕 导出 |
| 📄 PDF / 图片 / 截图 | — | ✅ | — | 手动上传 |
| 📦 飞书 JSON 导出 | ✅ | ✅ | — | 手动上传 |
| ✉️ 邮件 `.eml` / `.mbox` | ✅ | — | — | 手动上传 |
| 📝 Markdown / 直接粘贴 | ✅ | ✅ | — | 手动输入 |

---

## ⚡ 安装

打开你的 Claude Code / Hermes / OpenClaw / Codex，让 Agent 帮你装：

> 帮我安装这个 Skill：`https://github.com/limowan/mowan-CTI`

Agent 会自动检测当前宿主的 skills 目录，克隆仓库并注册入口。

<details>
<summary><b>🛠️ 手动安装</b></summary>

<br>

```bash
git clone https://github.com/limowan/mowan-CTI <TARGET>
```

| 宿主 | `<TARGET>` 路径 |
|------|-----------------|
| Claude Code | `~/.claude/skills/mowan-cti` |
| OpenClaw | `~/.openclaw/workspace/skills/mowan-cti` |
| Codex | `~/.codex/skills/mowan-cti` |
| Hermes | 克隆后按宿主文档注册 |

</details>

---

## 🚀 使用

安装完成后，在宿主中输入：

```
/cti
```

或者直接说：

```
帮我做人格测评
```

Skill 会引导你选择 A / B / C 模式，收集材料，自动分析，输出你的聊天人格结果。

---

## 🔧 工作原理

```
材料输入（A/B/C 三种模式）
    ↓
材料标准化（统一成"人格证据包"）
    ↓
人格分类引擎（匹配 12 类人格）
    ↓
结果包装（毒舌文案 + 配图 + 分享文案）
    ↓
输出（对话展示 / HTML 结果页）
```

三种来源在采集层不同，但后面统一走同一套分类引擎和结果包装。中间层是一个结构化的"人格证据包"，包含表达风格、决策方式、情绪表达、关系姿态等 10 个维度。

---

## 📂 项目结构

```
mowan-CTI/
├── SKILL.md                              # Skill 主入口（6步流程）
├── README.md                             # 项目说明（本文件）
├── prompts/
│   ├── external_analysis_prompt.md       # A 模式：给用户复制的提示词
│   ├── personality_classifier.md         # 人格分类引擎
│   ├── material_standardizer_a.md        # A 模式材料标准化
│   ├── material_standardizer_b.md        # B 模式材料标准化
│   ├── material_standardizer_c.md        # C 模式材料标准化
│   └── result_packager.md                # 结果包装器
├── references/
│   ├── personality_system.md             # 12 类人格完整定义
│   └── evidence_schema.md                # 人格证据包 schema
├── tools/
│   ├── feishu_auto_collector.py          # 飞书自动采集
│   ├── feishu_parser.py                  # 飞书消息 JSON 解析
│   ├── feishu_browser.py                 # 飞书文档浏览器读取
│   ├── feishu_mcp_client.py             # 飞书 MCP 客户端
│   ├── dingtalk_auto_collector.py        # 钉钉自动采集
│   └── email_parser.py                   # 邮件解析
├── image/                                # 12 类人格画像图
└── output/
    ├── index.html                        # 12 类人格总览页
    ├── gggg.html ... wdws.html           # 各人格结果页
    └── assets/
        ├── page.css                      # 样式（深色/浅色主题）
        ├── page.js                       # 渲染逻辑
        └── personality-data.js           # 12 类人格数据
```

---

## 🙏 致谢

B 模式的聊天记录采集工具（飞书、钉钉、邮件解析等）来自 [dot-skill (colleague-skill)](https://github.com/titanwings/colleague-skill/tree/dot-skill) 项目，该项目基于 MIT 许可证开源。感谢 [@titanwings](https://github.com/titanwings) 的工作。

---

## 🔒 隐私与数据安全

- **所有数据均在本地处理**：CTI 不会将你的聊天记录、分析结果或任何个人数据上传到任何服务器
- **不收集任何用户数据**：Skill 本身不包含任何数据收集、追踪或上报逻辑
- **分析过程完全离线**：人格分类由你本地运行的 AI Agent 完成，数据不离开你的设备
- **结果页纯静态**：生成的 HTML 结果页是纯前端静态文件，无后端、无网络请求、无 Cookie
- **输出产物与 Skill 分离**：生成的结果页存放在你指定的输出目录，不会写入 Skill 源码目录

---

## 📄 License

MIT License © [墨玩AI](https://github.com/limowan)

---

## 👋 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱

> 你以为自己是"随便侠"？你的聊天记录可不这么说。

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

<img src="https://raw.githubusercontent.com/limowan/mowan-mc-type/main/wechat_qrcode.jpg" alt="墨玩AI 公众号二维码" width="200" />
