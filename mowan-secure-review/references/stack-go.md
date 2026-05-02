# Go 技术栈安全清单

检测信号：`go.mod`、`go.sum`、`.go` 文件

---

## 竞态条件

Go 的 goroutine 并发模型使竞态条件成为常见问题。

**检查方法**：
- 共享变量是否有 `sync.Mutex` / `sync.RWMutex` 保护
- 是否使用了 channel 而非共享内存通信
- map 的并发读写是否使用了 `sync.Map` 或加锁
- 如果可用，运行 `go build -race` 检测竞态

**判定标准**：
- 涉及资金/权限的共享状态无并发保护 → High
- 非关键路径的竞态 → Medium

---

## SQL 注入

**检查方法**：
- Grep: `fmt.Sprintf("SELECT`、`fmt.Sprintf("INSERT`、`fmt.Sprintf("UPDATE`、`fmt.Sprintf("DELETE`
- 字符串拼接 SQL → High
- 安全模式：`db.Query("SELECT * FROM users WHERE id = ?", id)`（参数化查询）

**ORM 检查**：
- GORM: `db.Where("name = ?", name)` → 安全
- GORM: `db.Where(fmt.Sprintf("name = '%s'", name))` → 不安全

---

## 命令注入

**检查方法**：
- Grep: `exec.Command(`、`exec.CommandContext(`
- 检查命令参数是否包含用户输入
- `exec.Command("sh", "-c", userInput)` → Critical
- `exec.Command("ls", userInput)` → 参数注入风险（Medium）

---

## 模板注入

**检查方法**：
- `html/template` 默认自动转义 HTML → 安全
- `text/template` 不做转义 → 如果输出到 HTML 则有 XSS 风险
- Grep: `text/template` 用于 HTTP 响应 → Medium

---

## 路径穿越

**检查方法**：
- Grep: `os.Open(`、`os.ReadFile(`、`http.ServeFile(`、`http.FileServer(`
- `filepath.Join` 不能防止 `../` 穿越（需要 `filepath.Clean` + 前缀检查）
- `http.FileServer` 是否限制了服务目录

---

## unsafe 包

**检查方法**：
- Grep: `unsafe.Pointer`
- `unsafe` 包绕过了 Go 的类型安全和内存安全
- 检查使用场景是否合理

**判定标准**：
- `unsafe` 用于处理用户输入 → High
- `unsafe` 用于性能优化的内部逻辑 → Info（但需审查）

---

## HTTP 安全

1. **超时配置**
   - `http.Server` 是否设置了 `ReadTimeout`、`WriteTimeout`、`IdleTimeout`
   - 未设置超时 → 可被 Slowloris 攻击（Medium）

2. **CORS**
   - 检查 CORS 中间件配置
   - `AllowAllOrigins: true` + 认证接口 → High

3. **TLS**
   - 是否使用了 `http.ListenAndServeTLS`
   - TLS 配置是否禁用了弱协议和弱密码套件

---

## 依赖安全

- 运行 `govulncheck`（如果可用）
- 检查 `go.sum` 是否提交（确保依赖完整性）
- 检查是否有 `replace` 指令指向本地路径（不应出现在生产代码中）

---

## 错误处理

- Go 的错误处理模式（`if err != nil`）是否被正确遵循
- 是否有被忽略的错误返回值（`result, _ := someFunc()`）
- 错误信息是否泄露了内部细节给用户
