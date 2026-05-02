# 密钥与凭证泄露清单

密钥泄露是最常见的高危漏洞之一，因为利用门槛极低——攻击者只需要找到密钥就能直接使用。

---

## 代码中的硬编码凭证

### 检查方法

**Grep 高危模式**：
```
password\s*=\s*["']
passwd\s*=\s*["']
secret\s*=\s*["']
api_key\s*=\s*["']
apikey\s*=\s*["']
access_key\s*=\s*["']
private_key\s*=\s*["']
token\s*=\s*["']
auth_token\s*=\s*["']
jwt_secret\s*=\s*["']
encryption_key\s*=\s*["']
```

**排除误报**：
- 配置模板中的占位符（`"your-api-key-here"`、`"changeme"`、`"xxx"`）
- 测试文件中的 mock 值（但要确认测试值不是真实凭证）
- 环境变量读取（`process.env.API_KEY`、`os.getenv("API_KEY")`）

### 判定标准

- 真实 API Key / 密码硬编码在源码中 → Critical
- 默认密码未强制修改 → High
- 测试环境凭证硬编码（但与生产环境不同）→ Medium
- 占位符/示例值 → 不报

---

## 环境变量安全

### 检查方法

**1. .env 文件泄露**
- 检查 `.env` 是否在 `.gitignore` 中
- 检查 git 历史中是否曾提交过 `.env`（`git log --all --diff-filter=A -- .env`）
- 检查 `.env.example` / `.env.sample` 中是否包含真实值而非占位符
- 检查是否存在 `.env.production`、`.env.local` 等变体且未被 gitignore

**2. 环境变量在错误信息中泄露**
- 检查错误处理代码是否会输出完整的环境信息
- PHP: `phpinfo()` 暴露所有环境变量
- Python Django: `DEBUG=True` 时错误页面显示 settings（含环境变量）
- Node.js: 未捕获异常的堆栈信息是否包含环境变量值
- 检查自定义错误页面是否泄露了 `process.env`、`os.environ`、`$_ENV`

**3. 环境变量在日志中泄露**
- Grep 日志语句，检查是否记录了包含敏感环境变量的对象
- 检查启动日志是否打印了配置信息（含数据库连接串、密钥等）
- 检查 debug 日志级别下是否会输出请求上下文（可能含环境变量）

**4. 环境变量在前端泄露**
- 检查前端构建配置是否将服务端环境变量注入到客户端 bundle
- Next.js: 只有 `NEXT_PUBLIC_` 前缀的变量应暴露给前端
- Vite: 只有 `VITE_` 前缀的变量应暴露给前端
- Create React App: 只有 `REACT_APP_` 前缀的变量应暴露给前端
- Grep 前端代码中的 `process.env`，检查是否引用了非公开变量

**5. 环境变量在 Docker/K8s 中泄露**
- 检查 Dockerfile 中是否用 `ENV` 设置了敏感值（会留在镜像层中）
- 检查 docker-compose.yml 中是否硬编码了敏感环境变量
- 检查 K8s manifest 中 Secret 是否以明文存储
- 检查 CI/CD 配置中 secret 是否正确标记为 masked

**6. 默认/弱环境变量值**
- 检查是否有 fallback 默认值：`os.getenv("JWT_SECRET", "default-secret")`
- 检查 secret 生成逻辑是否使用了安全随机数
- 检查是否有环境变量值为空时的处理逻辑（空 secret 可能导致认证绕过）

### 判定标准

- .env 文件包含真实凭证且未被 gitignore → Critical
- 环境变量通过错误页面泄露（含数据库连接串/密钥）→ High
- 服务端环境变量泄露到前端 bundle → High
- Docker ENV 中硬编码敏感值 → High
- 环境变量有不安全的默认 fallback 值 → High
- .env.example 包含真实值 → Medium
- 启动日志打印了敏感配置 → Medium
- 环境变量为空时无安全处理 → Medium

---

## 配置文件中的凭证

### 检查方法

**Grep 配置文件**：
- `config.json`、`config.yml`、`config.xml`、`settings.py`、`application.properties`
- 检查数据库连接串是否包含明文密码
- 检查 SMTP 配置是否包含明文密码
- 检查第三方服务配置是否包含 API Key

**检查 gitignore**：
- 包含凭证的配置文件是否被 gitignore 排除
- 是否提供了 `config.example.json` 等模板文件

### 判定标准

- 包含真实凭证的配置文件被提交到仓库 → Critical
- 配置文件未被 gitignore 但当前不含凭证 → Medium（风险）

---

## Git 历史中的凭证

### 检查方法

- 检查 `.gitignore` 是否是后来才添加的（之前可能已提交过敏感文件）
- 如果可以运行 bash：`git log --all --diff-filter=D -- "*.env" "*.pem" "*.key"`
- 检查是否有 commit message 提到"remove secret"、"delete key"等

### 判定标准

- Git 历史中存在真实凭证（即使已删除）→ High（需要轮换凭证）
- 无法确认是否轮换过 → 标记为需要确认

---

## 前端代码中的凭证

### 检查方法

**Grep 前端源码**（JS/TS 文件）：
- API Key、Secret、Token 的硬编码
- 第三方服务的客户端密钥（注意区分公开密钥和私密密钥）
- Firebase 配置（`apiKey` 是公开的，但 `serviceAccountKey` 不是）

**检查构建产物**：
- Source map 是否在生产环境可访问（`.map` 文件）
- 构建产物中是否包含了不应暴露的环境变量

### 判定标准

- 私密 API Key 在前端代码中 → Critical
- 公开客户端 Key 在前端（如 Firebase apiKey、Stripe publishable key）→ Info（正常）
- Source map 在生产环境可访问 → Medium

---

## 私钥文件

### 检查方法

**Glob 搜索**：
- `*.pem`、`*.key`、`*.p12`、`*.pfx`、`*.jks`
- `id_rsa`、`id_ed25519`（SSH 私钥）
- `*.keystore`

**检查 gitignore**：
- 上述文件类型是否被排除

### 判定标准

- 私钥文件在仓库中 → Critical
- 私钥文件在 gitignore 中但存在于工作目录 → 确认是否安全存储

---

## 第三方服务凭证

### 检查方法

**常见第三方服务 Key 模式**：
- AWS: `AKIA[0-9A-Z]{16}`
- Google: `AIza[0-9A-Za-z_-]{35}`
- Stripe: `sk_live_[0-9a-zA-Z]{24,}`
- 支付宝: 应用私钥、支付宝公钥
- 微信: `AppSecret`、商户密钥
- SendGrid / Mailgun: API Key
- Slack: `xoxb-`、`xoxp-`、`xoxs-`

### 判定标准

- 任何第三方服务的私密凭证在代码中 → Critical
- 已过期/已轮换的凭证在 git 历史中 → Info（但建议确认）
