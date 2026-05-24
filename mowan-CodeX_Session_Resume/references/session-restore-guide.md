# Codex 会话恢复标准流程

## 适用场景

用户在 Codex Desktop 中做了这些操作后，左侧会话列表消失或历史变少：

- 从账号登录切到 API Key
- 从 API Key 切回账号登录
- 切换模型供应商 provider
- 切换自定义 API 供应商
- 改了模型配置后旧会话看不到

目前经验看，问题通常不是“会话真的没了”，而是本地会话索引、provider 标记、会话文件元数据不一致。

## 核心结论

只改 SQLite 不够。

Codex 可能会在重启时从会话 JSONL 文件的第一条 `session_meta` 重新回填数据库。如果 JSONL 里还是旧 provider，之前改过的 SQLite 可能又被写回旧值。

标准修复要同步三层：

1. SQLite 线程表：`$CODEX_HOME/state_5.sqlite`
2. 会话 JSONL 元数据：`$CODEX_HOME/sessions/**/*.jsonl` 和 `$CODEX_HOME/archived_sessions/*.jsonl`
3. 侧边栏索引：`$CODEX_HOME/session_index.jsonl`

`current_provider` 不放进 `config.json`，因为它经常变化。每次修复时必须从 Codex 当前配置里只读查看，作为默认建议目标：

```bash
CODEX_HOME="<配置中的 codex_home>"
CURRENT_PROVIDER="$(awk -F'=' '/^model_provider[[:space:]]*=/{gsub(/[ \"'\"']/,\"\",$2); print $2; exit}' "$CODEX_HOME/config.toml")"
printf '当前 provider: %s\n' "$CURRENT_PROVIDER"
```

读到 `model_provider` 后，优先询问用户是否把所有历史会话统一成当前 provider。不要因为读到了 `model_provider` 就自动修复。只读查看即可，不要输出 API Key。

## 只读检查

```bash
CODEX_HOME="<配置中的 codex_home>"
CURRENT_PROVIDER="$(awk -F'=' '/^model_provider[[:space:]]*=/{gsub(/[ \"'\"']/,\"\",$2); print $2; exit}' "$CODEX_HOME/config.toml")"
printf '当前 provider: %s\n' "$CURRENT_PROVIDER"

sqlite3 "$CODEX_HOME/state_5.sqlite" \
  "SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider ORDER BY COUNT(*) DESC;"

sqlite3 "$CODEX_HOME/state_5.sqlite" \
  "SELECT archived, COUNT(*) FROM threads GROUP BY archived;"

wc -l "$CODEX_HOME/session_index.jsonl"

find "$CODEX_HOME/sessions" "$CODEX_HOME/archived_sessions" \
  -type f -name '*.jsonl' | wc -l
```

检查完成后必须暂停，向用户复述结果，并优先建议统一成当前 provider：

```text
我检查到：
- Codex 当前配置里的 provider 可能是：<读取到的 provider>
- 数据库里的 provider 分布是：<统计结果>
- 会话 JSONL 里的 provider 分布是：<统计结果>
- session_index.jsonl 行数是：<行数>

这通常说明你已经把 Codex 切到 <读取到的 provider> 了。要不要把所有历史会话统一成当前 provider：<读取到的 provider>？
确认后我再备份，并给你看修复计划。
```

没有用户确认，不进入备份和修复步骤。

如果没读到当前 provider，或用户明确说不要统一成当前 provider，再请用户手动指定目标 provider：

```text
我没能稳定读到当前 provider，或者你不想统一成当前 provider。
你希望把历史会话统一成哪个 provider？
```

用户确认目标 provider 后，还要做二次确认。二次确认必须包含：

- 目标 provider
- 备份目录
- 将要改的文件类型
- 不会删除任何会话或缓存

建议话术：

```text
二次确认一下：我将把历史会话统一成 <provider>。
我会先备份到 <backup_root>/session-restore-时间戳。
随后只修改三类内容：
1. state_5.sqlite 里的 threads.model_provider
2. sessions/ 和 archived_sessions/ 中 JSONL 第一条 session_meta.payload.model_provider
3. session_index.jsonl

我不会删除任何会话、缓存或数据库。你确认现在执行吗？
```

没有第二次明确确认，不进入备份和修复。

统计 JSONL 首行 `session_meta` 的 provider：

```bash
find "$CODEX_HOME/sessions" "$CODEX_HOME/archived_sessions" \
  -type f -name '*.jsonl' -print0 |
xargs -0 node -e '
const fs=require("fs");
const counts={};
for (const f of process.argv.slice(1)) {
  const line=fs.readFileSync(f,"utf8").split(/\r?\n/,1)[0];
  if (!line) continue;
  try {
    const o=JSON.parse(line);
    if (o.type==="session_meta") {
      const p=o.payload?.model_provider || "(空)";
      counts[p]=(counts[p]||0)+1;
    }
  } catch {}
}
console.log(JSON.stringify(counts,null,2));
'
```

## 备份

备份目录应来自 `config.json` 的 `backup_root`。如果没配置，先问用户放哪里。

```bash
CODEX_HOME="<配置中的 codex_home>"
BACKUP_ROOT="<配置中的 backup_root>"
stamp="$(date +%Y%m%d-%H%M%S)"
backup_dir="$BACKUP_ROOT/session-restore-$stamp"
mkdir -p "$backup_dir/sessions" "$backup_dir/archived_sessions"

sqlite3 "$CODEX_HOME/state_5.sqlite" ".backup '$backup_dir/state_5.sqlite'"
cp -p "$CODEX_HOME/session_index.jsonl" "$backup_dir/session_index.jsonl" 2>/dev/null || true
cp -p "$CODEX_HOME/.codex-global-state.json" "$backup_dir/.codex-global-state.json" 2>/dev/null || true
rsync -a --include='*/' --include='*.jsonl' --exclude='*' "$CODEX_HOME/sessions/" "$backup_dir/sessions/"
rsync -a --include='*.jsonl' --exclude='*' "$CODEX_HOME/archived_sessions/" "$backup_dir/archived_sessions/" 2>/dev/null || true

echo "$backup_dir"
```

## 修复

设置目标 provider。这里的值必须来自用户确认；默认建议可以来自当前 Codex 配置，但不能自动决定：

```bash
CODEX_HOME="<配置中的 codex_home>"
CURRENT_PROVIDER="<用户确认的 provider>"
```

更新 SQLite：

```bash
sqlite3 "$CODEX_HOME/state_5.sqlite" \
  "UPDATE threads SET model_provider='$CURRENT_PROVIDER' WHERE model_provider <> '$CURRENT_PROVIDER';
   SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider;"
```

更新 JSONL 首行 `session_meta.payload.model_provider`：

```bash
CODEX_HOME="$CODEX_HOME" CURRENT_PROVIDER="$CURRENT_PROVIDER" node <<'NODE'
const fs = require('fs');
const path = require('path');

const CODEX_HOME = process.env.CODEX_HOME;
const CURRENT_PROVIDER = process.env.CURRENT_PROVIDER;
if (!CODEX_HOME) throw new Error('CODEX_HOME is required');
if (!CURRENT_PROVIDER) throw new Error('CURRENT_PROVIDER is required');

const roots = [
  path.join(CODEX_HOME, 'sessions'),
  path.join(CODEX_HOME, 'archived_sessions'),
];
let filesChanged = 0;
let linesChanged = 0;

function walk(dir) {
  if (!fs.existsSync(dir)) return;
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const st = fs.statSync(full);
    if (st.isDirectory()) walk(full);
    else if (name.endsWith('.jsonl')) processFile(full);
  }
}

function processFile(file) {
  const text = fs.readFileSync(file, 'utf8');
  const hadTrailingNewline = text.endsWith('\n');
  const lines = text.split('\n');
  if (hadTrailingNewline) lines.pop();
  let changed = false;

  const out = lines.map((line) => {
    if (!line.trim()) return line;
    let obj;
    try { obj = JSON.parse(line); } catch { return line; }
    if (obj?.type === 'session_meta' && obj.payload && obj.payload.model_provider !== CURRENT_PROVIDER) {
      obj.payload.model_provider = CURRENT_PROVIDER;
      changed = true;
      linesChanged += 1;
      return JSON.stringify(obj);
    }
    return line;
  });

  if (changed) {
    fs.writeFileSync(file, out.join('\n') + (hadTrailingNewline ? '\n' : ''));
    filesChanged += 1;
  }
}

for (const root of roots) walk(root);
console.log(JSON.stringify({ filesChanged, linesChanged }, null, 2));
NODE
```

重建 `session_index.jsonl`：

```bash
CODEX_HOME="$CODEX_HOME" node <<'NODE'
const fs = require('fs');
const { execFileSync } = require('child_process');

const CODEX_HOME = process.env.CODEX_HOME;
if (!CODEX_HOME) throw new Error('CODEX_HOME is required');

const db = `${CODEX_HOME}/state_5.sqlite`;
const indexPath = `${CODEX_HOME}/session_index.jsonl`;

const sql = `SELECT json_object(
  'id', id,
  'thread_name', CASE WHEN title IS NULL OR title = '' THEN first_user_message ELSE title END,
  'updated_at', strftime('%Y-%m-%dT%H:%M:%fZ', updated_at, 'unixepoch')
) FROM threads WHERE archived = 0 ORDER BY updated_at ASC;`;

const output = execFileSync('sqlite3', ['-noheader', db, sql], { encoding: 'utf8' });
const lines = output.split(/\r?\n/).filter(Boolean).map((line) => {
  const obj = JSON.parse(line);
  if (!obj.thread_name) obj.thread_name = 'Untitled';
  return JSON.stringify(obj);
});

fs.writeFileSync(indexPath, lines.join('\n') + '\n');
console.log(JSON.stringify({ written: lines.length }, null, 2));
NODE
```

## 验证

```bash
sqlite3 "$CODEX_HOME/state_5.sqlite" \
  "SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider;
   SELECT COUNT(*) FROM threads WHERE archived=0;"

node <<'NODE'
const fs=require('fs');
const p=`${process.env.CODEX_HOME}/session_index.jsonl`;
const rows=fs.readFileSync(p,'utf8').trim().split(/\n/).filter(Boolean).map(JSON.parse);
const ids=rows.map(x=>x.id);
console.log(JSON.stringify({ lines: rows.length, unique: new Set(ids).size }, null, 2));
NODE
```

修复前不强制退出 Codex Desktop；可以直接在 Codex 里完成修复。修复后让用户完全退出并重新打开 Codex Desktop 验证。如果遇到数据库锁、写入失败、或 UI 不刷新，再提示用户退出后重试。

## 回滚

使用之前输出的备份目录：

```bash
CODEX_HOME="<配置中的 codex_home>"
backup_dir="<备份目录>"

cp -p "$backup_dir/session_index.jsonl" "$CODEX_HOME/session_index.jsonl"
cp -p "$backup_dir/.codex-global-state.json" "$CODEX_HOME/.codex-global-state.json" 2>/dev/null || true
cp -p "$backup_dir/state_5.sqlite" "$CODEX_HOME/state_5.sqlite"
rsync -a "$backup_dir/sessions/" "$CODEX_HOME/sessions/"
rsync -a "$backup_dir/archived_sessions/" "$CODEX_HOME/archived_sessions/" 2>/dev/null || true
```
