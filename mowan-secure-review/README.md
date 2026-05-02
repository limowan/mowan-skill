<div align="center">

# 🔐 墨玩安全审计（攻击者视角）

### *"不是检查你有没有锁门，而是试试能不能撬开。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-black)](https://github.com/limowan/mowan-skill)

<br>

<table>
<tr><td align="left">

🎯 &nbsp;以精英渗透测试专家的视角，对项目进行全面代码级安全审计<br>
🔍 &nbsp;自动检测技术栈，动态加载对应攻击清单<br>
⚡ &nbsp;找的是真实可利用的漏洞，不是理论风险清单

</td></tr>
</table>

<br>

[✨ 核心特点](#-核心特点) · [🎯 支持的项目类型](#-支持的项目类型) · [⚡ 安装](#-安装) · [🚀 使用](#-使用) · [🔧 工作原理](#-工作原理) · [📂 项目结构](#-项目结构)

</div>

---

## ✨ 核心特点

| 特点 | 说明 |
|------|------|
| **攻击者视角** | 不是合规检查，而是模拟精英黑客尝试攻破你的系统 |
| **自动技术栈检测** | 自动识别项目语言、框架、基础设施，加载对应攻击清单 |
| **全项目审计** | 不只看 git diff，而是审计整个项目的安全状况 |
| **真实漏洞优先** | 每个发现都有完整的攻击路径，不报"理论上可能有问题" |
| **攻击链分析** | 主动寻找可串联的漏洞组合，发现单独看不严重但组合后致命的问题 |
| **环境变量重点检查** | 把 .env、配置文件、环境变量泄露作为重点攻击面 |

---

## 🎯 支持的项目类型

| 类型 | 技术栈 |
|------|--------|
| Web 应用 | PHP/Laravel、Node.js/Express、Python/Django/Flask/FastAPI、Java/Spring、Go |
| 前端应用 | React、Vue、Angular、Next.js、Nuxt.js |
| 移动端 | iOS (Swift/ObjC)、Android (Kotlin/Java)、Flutter、React Native |
| 小程序 | 微信小程序、支付宝小程序 |
| API 服务 | RESTful、GraphQL |
| AI 应用 | LLM 集成、RAG 系统、AI Agent |

---

## ⚡ 安装

打开你的 Claude Code / Hermes / OpenClaw / Codex，让 Agent 帮你装：

```
帮我安装一下 https://github.com/limowan/mowan-skill/tree/main/mowan-secure-review 这个 Skill
```

---

## 🚀 使用

安装后，在任意项目目录中输入：

```
/secure-review
```

或者用自然语言：

```
帮我做安全审计
查一下这个项目有没有漏洞
看看安全不安全
```

Skill 会自动检测项目技术栈，按 5 个阶段进行审计：

1. **侦察** — 识别技术栈、映射项目结构
2. **攻击面测绘** — 枚举所有入口点和用户输入位置
3. **漏洞猎杀** — 系统性寻找可利用的漏洞
4. **AI 专项检查** — 如果项目包含 AI 组件，检查提示词注入等
5. **报告生成** — 输出结构化的安全审计报告

---

## 🔧 工作原理

```
Phase 0: 侦察
    扫描 manifest 文件 + Grep 框架特征 → 检测技术栈
    ↓
Phase 1: 攻击面测绘
    枚举路由/API → 标记认证边界 → 定位输入点 → 盘点敏感数据
    ↓
Phase 2: 漏洞猎杀
    加载通用清单 + 技术栈专项清单 → 追踪数据流 → 确认可利用性
    ↓
Phase 3: AI 专项（条件执行）
    提示词注入 → 模型端点安全 → 输出安全 → 数据泄露
    ↓
Phase 4: 报告生成
    执行摘要 → 漏洞详情（含攻击路径）→ 攻击链 → 修复优先级
```

### 检查覆盖范围

| 类别 | 检查内容 |
|------|---------|
| OWASP Top 10 | 访问控制、加密失败、注入、不安全设计、配置错误、脆弱组件、认证失败、数据完整性、日志监控、SSRF |
| 注入攻击 | SQL/NoSQL 注入、命令注入、XSS、路径穿越、SSRF、CSRF、模板注入、Header 注入 |
| 认证授权 | 密码存储、会话管理、JWT 实现、OAuth、密码重置、MFA、速率限制、账号枚举 |
| 密钥泄露 | 硬编码凭证、.env 泄露、环境变量在错误信息/日志/前端/Docker 中泄露、Git 历史中的密钥 |
| 基础设施 | Nginx/Apache 配置、安全响应头、CORS、Docker 安全、CI/CD 管道、TLS、文件上传 |
| 业务逻辑 | 支付篡改、竞态条件、越权、流程绕过、速率限制绕过 |
| AI/LLM | 提示词注入、系统 Prompt 泄露、模型端点安全、输出安全、数据泄露、Agent 工具安全 |

---

## 📂 项目结构

```
mowan-secure-review/
├── SKILL.md                              # Skill 主入口（5阶段流程）
├── README.md                             # 项目说明（本文件）
├── .gitignore
├── references/
│   ├── attack-mindset.md                 # 攻击者人设与方法论
│   ├── severity-definitions.md           # 严重程度定义
│   ├── checklist-universal.md            # OWASP Top 10 通用清单
│   ├── checklist-input-validation.md     # 注入类攻击清单
│   ├── checklist-secrets.md              # 密钥/凭证/环境变量泄露
│   ├── checklist-auth.md                 # 认证授权深度检查
│   ├── checklist-infra.md                # 基础设施安全
│   ├── checklist-business-logic.md       # 业务逻辑漏洞
│   ├── checklist-ai-llm.md              # AI/LLM 安全专项
│   ├── stack-php.md                      # PHP 专项
│   ├── stack-node.md                     # Node.js 专项
│   ├── stack-python.md                   # Python 专项
│   ├── stack-frontend.md                 # React/Vue/Angular 专项
│   ├── stack-mobile.md                   # iOS/Android 专项
│   ├── stack-miniprogram.md              # 微信/支付宝小程序专项
│   ├── stack-java.md                     # Java/Spring 专项
│   ├── stack-go.md                       # Go 专项
│   └── report-template.md               # 报告模板
└── output/                               # 生成的报告（gitignored）
```

---

## 🔒 隐私与数据安全

- **所有分析均在本地完成**：不会将你的代码上传到任何服务器
- **只读审计**：Skill 不会修改被审计项目的任何文件
- **不生成攻击代码**：报告描述攻击路径用于防御，不生成实际 exploit
- **报告在对话中输出**：你决定是否保存，Skill 不自动写入文件

---

## 📄 License

MIT License © [墨玩AI](https://github.com/limowan)

---

## 👋 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱

> 安全不是一次性的检查，而是持续的对抗。

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
