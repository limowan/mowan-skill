# 🖌️ 墨成AI排版（mowan-mc-type）

> 将 Markdown 文章一键转换为微信公众号精美排版 HTML

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**公众号：墨玩AI** · **License：MIT**

---

## ✨ 这是什么

墨成AI排版是一个 Claude Code Skill，让你可以直接在 Claude Code 对话中将 Markdown 文章转换为**微信公众号精美排版**的 HTML。

输入一篇 Markdown → AI 帮你选风格、排版、加导航和关注卡片 → 输出可直接粘贴到公众号后台的 HTML。

### 核心特点

- 🎨 **6 种精心设计的风格预设**，覆盖知识型、故事型、商务型到高传播力风格
- 📋 **自动生成滑动卡片导航**（默认开启），支持 3 种导航样式
- 🫶 **自动生成引导关注卡片**（默认开启），文末"点赞·在看·转发"三连
- 💊 **可选胶囊标签**，降低读者认知负载
- 📤 **可选发布到草稿箱**，自动对接微信发布类 Skill
- ✅ **100% 微信公众号兼容**，所有样式内联，逐条踩坑验证
- 🤖 **AI 主动推荐风格**，根据文章内容类型智能匹配

---

## 🚀 快速开始

安装到你的 Claude Code 技能目录后，在对话中说：

```
帮我排版这篇文章
```

或者直接粘贴 Markdown 内容，AI 会自动触发排版流程。

### 触发词

- 「排版」「公众号排版」
- 「Markdown 转公众号」「帮我排版成公众号文章」
- 「微信排版」「生成公众号 HTML」
- 「mc-type」「墨成排版」

---

## 🎨 6 种风格预设

| 风格 | 一句话概括 | 适合场景 |
|------|-----------|---------| 
| **极简理性** | 理性克制，信息优先 | 知识拆解、教程、方法论 |
| **温暖故事感** | 温暖真诚，陪伴叙事 | 成长复盘、个人故事、感悟 |
| **商务专业** | 专业正式，信息密度高 | 商业分析、行业报告、策略总结 |
| **编辑长文风** | 杂志社论，章节推进感 | 长文、观点文章、复盘 |
| **视觉杂志大片** | 多彩高级，杂志页面感 | 深度特稿、人物稿、专题 |
| **新媒体高亮风** | 醒目易读，传播感强 | 热点解读、观点输出、知识传播 |

---

## 📋 附加组件

| 组件 | 默认 | 说明 |
|------|------|------|
| 📋 卡片导航 | ✅ 开启 | 文章顶部的章节目录区，支持滑动卡片（默认）、仪表盘、标题卡片 3 种样式 |
| 🫶 引导关注卡片 | ✅ 开启 | 文末"点赞·在看·转发"互动按钮区 |
| 💊 胶囊标签 | ❌ 关闭 | 段首【核心观点】【Step 1】等引导标签 |
| 📤 发布到草稿箱 | ❌ 关闭 | 排版后自动寻找微信发布 Skill 推送到草稿箱 |

---

## 📁 文件结构

```
mowan-mc-type/
├── SKILL.md                    # 工作流编排（流程控制）
├── README.md                   # 项目说明（本文件）
└── resources/
    ├── presets.md               # 6 种风格预设提示词
    ├── nav-cards.md             # 3 种卡片导航提示词
    ├── follow-card.md           # 引导关注卡片提示词
    └── wechat-rules.md          # 公众号兼容约束 + 输出规则
```

---

## 📄 License

MIT License

```
MIT License

Copyright (c) 2026 墨玩AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👋 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法。

> 写完文章还要花半小时排版，这件事困扰了我很久。所以我做了这个工具——希望排版不再是负担，而是写作的最后一点小享受。[→ 读读这个故事](https://mp.weixin.qq.com/s/lC98DDwDB3aqKj129lC-Hw)

<table>
  <thead>
    <tr>
      <th style="background-color: #f8fafc; text-align: left; width: 110px; border-bottom: 2px solid #e5e7eb; padding: 8px 12px;">平台</th>
      <th style="background-color: #f8fafc; text-align: left; border-bottom: 2px solid #e5e7eb; padding: 8px 12px;">链接</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight: 500; border: 1px solid #e5e7eb; padding: 8px 12px;">📕 小红书</td>
      <td style="border: 1px solid #e5e7eb; padding: 8px 12px;"><a href="https://xhslink.com/m/3Ks23mHtPrL" target="_blank">墨玩AI</a></td>
    </tr>
    <tr>
      <td style="font-weight: 500; border: 1px solid #e5e7eb; padding: 8px 12px;">💬 公众号</td>
      <td style="border: 1px solid #e5e7eb; padding: 8px 12px;">微信搜「墨玩AI」或扫码关注 ↓</td>
    </tr>
  </tbody>
</table>

<img src="https://raw.githubusercontent.com/limowan/mowan-mc-type/main/wechat_qrcode.jpg" alt="墨玩AI 公众号二维码" width="200" />

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=limowan/mowan-mc-type&type=Date)](https://star-history.com/#limowan/mowan-mc-type&Date)
