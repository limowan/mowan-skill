---
name: mowan-CodeX_Session_Resume
description: 修复 Codex Desktop 在切换账号登录、API Key、自定义模型供应商或模型配置后，左侧会话列表消失、历史对话看不到、会话索引不完整的问题。适用于会话文件还在本地，但 UI 侧边栏隐藏或丢失历史记录的场景。
metadata:
  short-description: 修复 Codex 会话列表消失
---

# mowan-CodeX_Session_Resume

当用户说 Codex / CodeX 左侧会话没了、切换 provider 后历史消失、从 API 切回账号后会话不见、换模型供应商后看不到旧对话时，使用本 Skill。

## 先问清楚

先用大白话问用户：

> 你这次主要改了什么？是从账号登录切到 API Key、从 API Key 切回账号、换了模型供应商，还是只换了模型名称？

如果用户不确定，继续说：

> 没关系，我先只读检查。重点看三件事：会话文件还在不在、数据库里 provider 是什么、左侧会话索引是不是空了。

## 配置规则

本 Skill 使用配置文件，避免把不同用户的路径写死。

- 示例配置：`config.example.json`
- 正式配置：`config.json`
- 真实配置必须被 `.gitignore` 排除，不要提交或分享。

首次运行时，如果没有 `config.json`：

1. 让用户复制 `config.example.json` 为 `config.json`。
2. 引导用户填写：
   - `codex_home`：Codex 数据目录，通常是 `~/.codex`
   - `backup_root`：备份放哪里，建议放在 Codex 数据目录下的 `backups`
3. 写入或修改配置前，先把将要使用的关键路径展示给用户确认。

`current_provider` 不写进配置文件，因为它会随着用户切换账号、API Key、供应商或模型配置变化。每次运行时必须先只读查看 `codex_home/config.toml` 里的 `model_provider`，把它作为默认建议目标，但不能自动执行：

> 我检查到当前 Codex 配置里的 provider 是 `<当前 provider>`，历史会话里还有 `<旧 provider>`。这通常说明你已经切到新 provider 了。要不要把所有历史会话的 provider 统一改成当前的 `<当前 provider>`？

用户明确确认后，才能继续修复。

写入前还必须二次确认。也就是说：用户第一次确认目标 provider 后，先展示将要执行的修复计划；用户第二次明确同意后，才能真正改文件。

如果环境里有可交互提问工具，每次最多问 1-3 个短问题；没有就直接在对话里引导。

## 安全原则

- 修复前必须备份。
- 不要删除缓存、会话、数据库或历史文件，除非用户明确确认。
- 对 JSONL 文件只改第一条 `session_meta.payload.model_provider`，不要全文替换。
- 对 SQLite 只改必要字段：`threads.model_provider`。

## 诊断步骤

先只读检查：

```bash
CODEX_HOME="<从 config.json 读取 codex_home>"
awk -F'=' '/^model_provider[[:space:]]*=/{gsub(/[ \"'\"']/, "", $2); print $2; exit}' "$CODEX_HOME/config.toml"
sqlite3 "$CODEX_HOME/state_5.sqlite" \
  "SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider;"
sqlite3 "$CODEX_HOME/state_5.sqlite" \
  "SELECT archived, COUNT(*) FROM threads GROUP BY archived;"
wc -l "$CODEX_HOME/session_index.jsonl"
find "$CODEX_HOME/sessions" "$CODEX_HOME/archived_sessions" \
  -type f -name '*.jsonl' | wc -l
```

常见判断：

- 数据库有线程，但 UI 为空：多半是侧边栏索引问题。
- `threads.model_provider` 同时存在新旧 provider：多半是 provider 过滤或回填问题。
- 重启后 provider 又变回旧值：说明 JSONL 会话文件首行 `session_meta` 还保留旧 provider。
- `session_index.jsonl` 行数明显少、或 ID 重复：需要重建索引。

只读检查完成后必须停下来问用户，不能自动进入修复：

> 我现在看到了这些结果：当前配置 provider 是……，历史 provider 分布是……，索引行数是……。你要不要把所有历史会话统一成当前配置里的 `<当前 provider>`？确认后我再备份并给你看修复计划。

如果没有读到当前配置里的 provider，或用户明确说不要用当前 provider，再让用户手动指定目标 provider：

> 我没能稳定读到当前 provider，或者你不想统一成当前 provider。你希望把历史会话统一成哪个 provider？

用户回答后，再做二次确认：

> 我将把历史会话统一成 `<provider>`，并先备份到 `<backup_root>/session-restore-时间戳`。会修改 `state_5.sqlite`、会话 JSONL 的 `session_meta`、`session_index.jsonl`。你确认现在执行吗？

只有用户第二次明确确认“执行 / 确认 / 可以 / 开始”后，才能写入。

## 标准修复流程

1. 按配置里的 `backup_root` 创建时间戳备份。
2. 备份：
   - `state_5.sqlite`
   - `session_index.jsonl`
   - `.codex-global-state.json`
   - `sessions/`
   - `archived_sessions/`
3. 把 `state_5.sqlite` 的 `threads.model_provider` 改成用户确认的目标 provider，默认是当前 Codex 配置里的 provider。
4. 把所有会话 JSONL 的 `session_meta.payload.model_provider` 改成用户确认的目标 provider。
5. 用 SQLite 中未归档线程重建 `session_index.jsonl`。
6. 让用户完全重启 Codex Desktop 验证。

可以直接在 Codex 里修复，不需要修复前退出。只有遇到数据库锁、写入失败、或修完 UI 仍不刷新时，再让用户完全退出后重试或验证。

详细命令、标准流程和回滚方式见：`references/session-restore-guide.md`。

## 输出要求

最后只总结这些：

- 用户这次变更类型是什么。
- 备份放在哪里。
- 改了哪些文件。
- 修复前后数量变化。
- 下一步让用户如何验证。

不要输出原始会话正文、密钥、真实个人路径。
