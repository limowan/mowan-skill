# 输入验证与注入攻击清单

所有注入类漏洞的核心模式：**攻击者可控的输入 → 未经充分清洗 → 进入危险操作**。

审计时必须追踪完整的数据流路径，不能只看危险函数是否存在。

---

## SQL 注入

### 检查方法

**Grep 危险模式**（字符串拼接 SQL）：
- PHP: `"SELECT.*\$`、`'SELECT.*' . \$`、`query(".*\$`
- Python: `execute(f"`、`execute(".*%`、`execute(".*".format`
- Node.js: `query(\`.*\$\{`、`query(".*" +`
- Java: `"SELECT.*" \+`、`Statement` 而非 `PreparedStatement`
- Go: `fmt.Sprintf("SELECT`、`db.Query(".*" +`

**安全模式确认**：
- 参数化查询 / 预处理语句（PDO、PreparedStatement、parameterized query）
- ORM 的标准查询方法（但注意 raw query 和 where 子句中的拼接）

**ORM 绕过场景**：
- `whereRaw()`、`DB::raw()`（Laravel）
- `.extra()`、`.raw()`（Django）
- `sequelize.query()`（Sequelize）
- `$queryBuilder->where("field = '" . $input . "'")`

### 判定标准

- 用户输入直接拼接进 SQL → Critical（如果是认证/支付相关）或 High
- ORM raw query 中拼接用户输入 → High
- 使用参数化查询但参数来源不可信 → 需进一步追踪

---

## NoSQL 注入

### 检查方法

**Grep 危险模式**：
- MongoDB: `find({.*req.body`、`$where`、`$regex` 接受用户输入
- 用户输入直接作为查询对象（`db.collection.find(req.body)`）

**攻击向量**：
- `{"username": {"$gt": ""}, "password": {"$gt": ""}}` 绕过认证
- `$where` 子句中的 JavaScript 注入

### 判定标准

- 用户输入直接作为查询条件对象 → High
- `$where` 接受用户输入 → Critical（可执行任意 JS）

---

## OS 命令注入

### 检查方法

**Grep 危险函数**：
- PHP: `exec(`、`system(`、`passthru(`、`shell_exec(`、`popen(`、`` ` `` (反引号)
- Python: `os.system(`、`subprocess.call(.*shell=True`、`os.popen(`
- Node.js: `child_process.exec(`、`execSync(`（注意：`execFile` 相对安全）
- Java: `Runtime.getRuntime().exec(`、`ProcessBuilder`
- Go: `exec.Command(`

**追踪用户输入**：
- 命令字符串中是否包含用户可控的变量
- 是否使用了参数数组而非字符串拼接

**安全模式**：
- 使用参数数组（`execFile('cmd', [arg1, arg2])`）而非字符串拼接
- 白名单校验用户输入
- 避免 `shell=True`（Python）

### 判定标准

- 用户输入拼接进 shell 命令 → Critical
- 使用参数数组但未校验参数内容 → Medium（参数注入）

---

## XSS（跨站脚本）

### 检查方法

**存储型 XSS**：
- 追踪用户输入存储到数据库的路径
- 追踪从数据库读取后输出到 HTML 的路径
- 检查输出时是否做了 HTML 转义

**反射型 XSS**：
- Grep URL 参数直接输出到页面的代码
- 检查错误消息是否包含未转义的用户输入

**DOM 型 XSS**：
- Grep: `innerHTML`、`outerHTML`、`document.write`、`eval(`
- React: `dangerouslySetInnerHTML`
- Vue: `v-html`
- Angular: `bypassSecurityTrustHtml`

**框架自动转义确认**：
- React JSX 默认转义（但 `dangerouslySetInnerHTML` 除外）
- Vue 模板默认转义（但 `v-html` 除外）
- Django 模板默认转义（但 `|safe`、`{% autoescape off %}` 除外）
- PHP 需要手动 `htmlspecialchars()`

### 判定标准

- 存储型 XSS（管理后台）→ High
- 存储型 XSS（用户可见页面）→ High
- 反射型 XSS → Medium
- DOM 型 XSS（需要特定条件）→ Medium
- 框架自动转义已覆盖 → 不报

---

## 路径穿越

### 检查方法

**Grep 文件操作 + 用户输入**：
- 文件读取：`readFile`、`fopen`、`open`、`file_get_contents`
- 文件写入：`writeFile`、`fwrite`、`save`
- 文件包含：`include`、`require`（PHP）
- 文件解压：zip/tar 解压时的文件名（Zip Slip）

**检查过滤**：
- 是否过滤了 `../`、`..\\`
- 是否使用了 `path.resolve` / `realpath` 后检查是否在允许目录内
- 是否过滤了空字节 `%00`（旧版本语言）

### 判定标准

- 用户输入直接拼接文件路径且无过滤 → High
- 有 `../` 过滤但可绕过（编码、双写）→ High
- 使用 realpath + 目录白名单 → 安全

---

## SSRF（服务端请求伪造）

### 检查方法

**Grep HTTP 请求函数**：
- PHP: `file_get_contents(`、`curl_exec(`、`fopen("http`
- Python: `requests.get(`、`urllib.urlopen(`、`httpx`
- Node.js: `fetch(`、`axios(`、`http.get(`、`got(`
- Java: `HttpURLConnection`、`HttpClient`、`RestTemplate`

**检查 URL 来源**：
- URL 是否包含用户输入（直接或间接）
- 是否校验了协议（只允许 http/https）
- 是否校验了目标 IP（禁止 127.0.0.1、10.x、172.16-31.x、192.168.x、169.254.x）
- 是否关闭了自动重定向
- 是否做了 DNS 解析后的 IP 校验（防 DNS 重绑定）

### 判定标准

- 用户可控 URL 无任何校验 → High
- 有协议校验但无 IP 校验 → Medium
- 完整校验（协议 + IP + 禁止重定向 + DNS 重绑定防护）→ 安全

---

## CSRF（跨站请求伪造）

### 检查方法

**检查防护机制**：
- 是否使用了 CSRF Token
- Cookie 是否设置了 `SameSite` 属性
- 是否校验了 `Origin` / `Referer` 头

**高风险操作**：
- 密码修改、邮箱修改、手机号修改
- 支付、转账、退款
- 权限变更、角色分配
- 账号删除、数据删除

### 判定标准

- 敏感操作无任何 CSRF 防护 → High
- 有 SameSite=Lax 但敏感操作用 GET 请求 → High
- 有 SameSite=Lax + Origin 校验 → 基本安全（同域部署下）
- 有 CSRF Token + SameSite → 安全

---

## 模板注入 (SSTI)

### 检查方法

**Grep 模板渲染 + 用户输入**：
- Python Jinja2: `render_template_string(user_input)`
- Python Mako: `Template(user_input)`
- Java Freemarker/Velocity: 用户输入作为模板内容
- PHP Twig: `createTemplate(user_input)`
- Node.js: `ejs.render(user_input)`

**安全模式**：
- 用户输入作为模板变量（`render_template('page.html', name=user_input)`）→ 安全
- 用户输入作为模板内容（`render_template_string(user_input)`）→ 危险

### 判定标准

- 用户输入作为模板内容渲染 → Critical（通常可 RCE）
- 用户输入作为模板变量 → 安全（框架自动转义）

---

## Header 注入 (CRLF)

### 检查方法

- Grep 设置 HTTP 响应头的代码
- 检查头部值是否包含用户输入
- 检查是否过滤了 `\r\n`（CRLF）

### 判定标准

- 用户输入直接进入响应头且无 CRLF 过滤 → Medium
- 现代框架通常自动处理 → 确认框架版本
