# mowan-skill 项目规范

## 项目概述

墨玩 AI Skills 集合，所有 Skill 在此仓库开发，通过符号链接注册到 Claude Code / Codex 环境。

- **GitHub 仓库**：https://github.com/limowan/mowan-skill
- **性质**：公开仓库，所有 mowan-* Skill 对外分享

## 私有 Skill 例外

`mowan-wechat-article-picture` 当前是本地私有 Skill，暂不按公开 Skill 流程处理。

- 可以在本仓库目录开发，并通过 junction 注册到 `~/.claude/skills/`。
- 暂不更新根目录 `README.md`，除非用户明确说“可以开源”或“可以推 GitHub”。
- `config.example.json` 可作为未来开源模板保留。
- `config.json`、头像、关注卡片、文章原文、生成图片产物默认不提交。
- 未来如果要开源，必须先做隐私扫描，确认没有真实本地路径、账号素材、密钥、代理地址和文章内容。
- 未经用户明确确认，不要 `git add` / commit / push 这个 Skill。

## 目录结构

```
mowan-skill/
├── CLAUDE.md                # 项目规范（本文件）
├── README.md                # GitHub 仓库首页展示
├── mowan-mc-type/           # 各 Skill 独立目录
│   ├── SKILL.md             # Skill 入口（必须）
│   ├── README.md            # Skill 说明文档（必须）
│   ├── prompts/             # 提示词文件
│   ├── references/          # 参考资料
│   ├── tools/               # 工具脚本
│   └── ...
├── mowan-CTI/
├── mowan-dadao-touyan/
├── mowan-content-creator/
└── mowan-sucai-sort/
```

## 符号链接注册

每个 Skill 开发完成后，需要创建符号链接到 `~/.claude/skills/`，Claude Code 才能识别。

```bash
# Windows（需管理员权限的 CMD 或 Git Bash）
# 格式：ln -s <源路径> <目标路径>

ln -s /c/AI编程项目/mowan-skill/mowan-xxx ~/.claude/skills/mowan-xxx
```

当前已注册的链接：
| Skill | 链接 |
|-------|------|
| mowan-mc-type | `~/.claude/skills/mowan-mc-type` → 本仓库 |
| mowan-sucai-sort | `~/.claude/skills/mowan-sucai-sort` → 本仓库 |
| mowan-content-creator | `~/.claude/skills/mowan-content-creator` → 本仓库 |
| mowan-dadao-touyan | `~/.claude/skills/mowan-dadao-touyan` → 本仓库 |
| mowan-CTI | `~/.claude/skills/mowan-CTI` → 本仓库 |
| mowan-video-explainer | `~/.claude/skills/mowan-video-explainer` → 本仓库 |
| mowan-secure-review | `~/.claude/skills/mowan-secure-review` → 本仓库 |

新增 Skill 后必须：
1. 创建符号链接
2. 更新本表格
3. 更新根目录 `README.md` 的 Skill 列表

## README 文档规范

每个 Skill 必须有 `README.md`，整体结构参考 `mowan-CTI/README.md`，但具体内容根据 Skill 特点自由发挥，不需要完全一致。

必须包含的部分：
- 功能简介（说清楚这个 Skill 做什么）
- 安装方式
- 使用方法
- 隐私与数据安全说明
- License（MIT）
- 关于作者（统一使用墨玩AI的社交平台链接和二维码，包含"我的产品"和"关注我"两个子区块）

可选部分（根据 Skill 复杂度决定）：
- 核心特点
- 工作原理
- 项目结构
- 致谢

关键要求：
- 安装命令统一格式：`帮我安装一下 https://github.com/limowan/mowan-skill/tree/main/[skill-name] 这个 Skill`
- 关于作者部分统一使用墨玩AI的信息，不可修改

### 关于作者区块规范

子目录 Skill 的 README 关于作者部分统一格式如下，不包含"我的 Skill"汇总表（汇总表只在根目录 README 展示）：

```markdown
## 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱

> （可选：一句话个人感悟，与当前 Skill 相关）

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
```

格式要点：
- 使用 Markdown 表格，不用 HTML `<table>`
- 问问毛选小程序二维码 width=160，引用路径 `../问问毛选小程序.png`
- 公众号二维码 width=200
- 不放"我的 Skill"汇总表，Skill 列表只在根目录 README 维护

## Git 提交规范

```
feat: 新增功能
fix: 修复问题
docs: 文档更新
refactor: 重构
chore: 杂项
```

示例：`docs: 增加 mowan-CTI 人格侧写 Skill 到 README`

## 发布流程

1. 本地开发并测试 Skill
2. 更新 Skill 自身的 `README.md`
3. 更新根目录 `README.md`（Skill 列表 + 作品表格）
4. **隐私检查**（见下方）
5. 提交并推送到 GitHub（仓库：https://github.com/limowan/mowan-skill）

## 隐私与安全检查

本仓库是公开的，推送前必须检查以下内容，发现问题必须停下来跟用户确认：

- 不得包含个人隐私信息（真实姓名、手机号、邮箱、地址、身份证号等）
- 不得包含 API Key、Token、密钥、密码等敏感凭证
- 不得包含本地绝对路径（如 `C:\Users\Limmer\...`）
- 不得包含内部系统地址、内网 URL
- 不得包含用户的聊天记录、对话历史等隐私数据
- SKILL.md 中引用的本地数据路径（如 Obsidian 目录、素材库路径）不应出现在 README 中

检查时机：
- 每次 `git add` 前，主动扫描待提交文件
- 新增 Skill 首次推送时，完整审查所有文件
- 有疑问时，列出可疑内容并询问用户是否可以推送
