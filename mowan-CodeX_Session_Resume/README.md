# mowan-CodeX_Session_Resume

修复 Codex Desktop 在切换账号登录、API Key、自定义模型供应商或模型配置后，左侧会话列表消失、历史对话看不到的问题。

适用于会话文件还在本地，但 UI 侧边栏隐藏或丢失历史记录的场景。

## 核心特点

- 只读诊断优先：先检查再修复，不会误操作
- 三层同步修复：SQLite 线程表 + 会话 JSONL 元数据 + 侧边栏索引
- 当前 provider 识别：优先读取 Codex 当前配置，默认建议统一到当前 provider
- 双重确认机制：统一到当前 provider 的确认 + 修复计划确认，防止误改
- 自动备份：修复前完整备份数据库、索引和会话文件
- 支持回滚：备份完整，随时可恢复

## 适用场景

- 从账号登录切到 API Key 后会话消失
- 从 API Key 切回账号后历史不见
- 切换模型供应商（provider）后旧对话看不到
- 换了自定义 API 供应商后侧边栏为空
- 改了模型配置后会话列表变少

## 安装

```
帮我安装一下 https://github.com/limowan/mowan-skill/tree/main/mowan-CodeX_Session_Resume 这个 Skill
```

## 使用方法

直接告诉 AI：

> Codex 左侧会话没了

或者：

> 切换 provider 后历史消失了

Skill 会自动引导你完成诊断和修复。

## 工作原理

1. **配置检查**：读取 `config.json` 确定 Codex 数据目录和备份位置
2. **只读诊断**：检查 SQLite provider 分布、会话文件数量、索引完整性
3. **用户确认**：展示诊断结果，优先询问是否统一成当前 Codex 配置里的 provider
4. **备份**：完整备份数据库、索引、会话文件
5. **三层修复**：统一 SQLite、JSONL 元数据、侧边栏索引的 provider
6. **验证**：重启 Codex Desktop 确认恢复

## 配置

首次使用时，复制示例配置并填写：

```bash
cp config.example.json config.json
```

配置项：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `codex_home` | Codex 数据目录 | `~/.codex` |
| `backup_root` | 备份存放位置 | `~/.codex/backups` |

## 隐私与数据安全

- 所有操作在本地完成，不上传任何数据
- 修复前自动备份，支持完整回滚
- 不会删除任何会话、缓存或数据库
- `config.json` 通过 `.gitignore` 排除，不会被提交

## 致谢

本 Skill 的问题定位和修复思路参考了 [codex-history-sync-tool](https://github.com/GODGOD126/codex-history-sync-tool) 项目。感谢 [@GODGOD126](https://github.com/GODGOD126) 对 Codex 会话恢复场景的探索。

本 Skill 在此基础上补充了三层同步修复、当前 provider 识别、双重确认、备份和回滚流程，方便 AI Agent 在本地排障时更稳地执行。

## License

MIT

## 关于作者

**墨玩AI** — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱

> 用 Codex 的人都懂，切个 provider 会话就没了的痛。

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
