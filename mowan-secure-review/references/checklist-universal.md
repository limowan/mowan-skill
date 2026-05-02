# OWASP Top 10 通用安全清单

基于 OWASP Top 10 (2021) 映射到具体代码模式。每项给出要检查什么、怎么用 Grep/Read 检查、以及判定标准。

---

## A01: 访问控制失效 (Broken Access Control)

### 检查项

1. **IDOR（不安全的直接对象引用）**
   - Grep 所有接受 ID 参数的接口（`/user/:id`、`?order_id=`、`?file=`）
   - 检查是否校验了"当前用户是否有权访问该 ID 对应的资源"
   - 特别关注：订单详情、用户资料、文件下载、消息记录

2. **缺失的认证检查**
   - 列出所有路由/端点，标记哪些需要认证、哪些公开
   - 检查认证中间件是否覆盖了所有需要保护的路由
   - 关注：管理后台路由是否有独立的权限校验

3. **水平越权**
   - 普通用户 A 能否访问用户 B 的数据
   - 检查数据查询是否带了 `WHERE user_id = 当前用户` 条件

4. **垂直越权**
   - 普通用户能否访问管理员接口
   - 检查角色/权限校验是否在每个管理接口都执行

5. **路径穿越**
   - Grep 文件操作函数（`fopen`、`readFile`、`open`、`include`、`require`）
   - 检查文件路径是否包含用户输入
   - 检查是否过滤了 `../`、`..\\`、空字节

---

## A02: 加密失败 (Cryptographic Failures)

### 检查项

1. **密码存储**
   - Grep 密码哈希函数：是否使用 bcrypt/argon2/scrypt
   - 如果使用 MD5/SHA1/SHA256（无 salt），标记为 High
   - 检查 salt 是否为每用户独立生成

2. **敏感数据明文传输**
   - 检查是否强制 HTTPS（重定向、HSTS 头）
   - 内部服务间通信是否加密

3. **弱加密算法**
   - Grep: `DES`、`RC4`、`MD5`（用于加密而非校验）、`ECB` 模式
   - 检查 TLS 配置是否禁用了弱协议（SSLv3、TLS 1.0/1.1）

4. **密钥管理**
   - 加密密钥是否硬编码在代码中
   - 密钥轮换机制是否存在
   - 加密密钥和被加密数据是否存储在同一位置

---

## A03: 注入 (Injection)

详见 `checklist-input-validation.md`，此处仅列出检查入口。

### 检查项

1. SQL 注入 — 所有数据库查询
2. NoSQL 注入 — MongoDB 等文档数据库查询
3. OS 命令注入 — 系统命令执行
4. LDAP 注入 — 目录服务查询
5. 表达式语言注入 — 模板引擎、OGNL、SpEL
6. XSS — 所有输出到 HTML 的用户输入

---

## A04: 不安全的设计 (Insecure Design)

### 检查项

1. **业务逻辑缺陷**
   - 支付流程能否跳过步骤
   - 优惠券/折扣能否重复使用
   - 数量/金额参数是否可被篡改为负数

2. **缺少速率限制**
   - 登录接口、注册接口、密码重置、验证码发送
   - API 接口是否有全局或单用户限流

3. **竞态条件**
   - 余额扣减、库存扣减、优惠券核销是否有并发保护
   - 检查是否使用了数据库事务或分布式锁

---

## A05: 安全配置错误 (Security Misconfiguration)

### 检查项

1. **调试模式**
   - Grep: `DEBUG=true`、`debug: true`、`APP_DEBUG`、`FLASK_DEBUG`
   - 生产环境配置中是否关闭了调试模式

2. **默认凭证**
   - 检查是否存在默认管理员账号/密码
   - 数据库是否使用默认端口且无密码

3. **不必要的功能**
   - 是否暴露了 phpinfo()、/debug、/status、/metrics 等端点
   - 是否有未使用但仍可访问的 API 端点

4. **安全响应头**
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY/SAMEORIGIN`
   - `Content-Security-Policy`
   - `Strict-Transport-Security`
   - `Referrer-Policy`

5. **CORS 配置**
   - Grep: `Access-Control-Allow-Origin`
   - 是否使用了 `*` 通配符
   - 是否动态反射了请求的 Origin 而未校验白名单

6. **目录列表**
   - Web 服务器是否禁用了目录浏览
   - 静态文件目录是否暴露了源码或配置文件

---

## A06: 脆弱和过时的组件 (Vulnerable and Outdated Components)

### 检查项

1. **依赖审计**
   - 运行 `npm audit`（Node.js）、`pip-audit`（Python）、`composer audit`（PHP）
   - 检查 lock 文件中是否有已知 CVE 的依赖

2. **过时的框架版本**
   - 检查主框架版本是否在维护周期内
   - 检查是否有已知安全补丁未应用

3. **前端 CDN 引用**
   - 检查是否使用了 SRI（Subresource Integrity）
   - CDN 引用的库版本是否过时

---

## A07: 认证和身份验证失败 (Identification and Authentication Failures)

详见 `checklist-auth.md`，此处仅列出关键检查点。

1. 弱密码策略
2. 凭证填充/暴力破解防护
3. 会话管理（固定、劫持、超时）
4. 多因素认证实现
5. 密码重置流程安全性

---

## A08: 软件和数据完整性失败 (Software and Data Integrity Failures)

### 检查项

1. **不安全的反序列化**
   - Grep: `unserialize`（PHP）、`pickle.loads`（Python）、`ObjectInputStream`（Java）、`JSON.parse` + `eval`
   - 检查反序列化的输入是否来自不可信来源

2. **CI/CD 管道安全**
   - 检查 GitHub Actions / GitLab CI 配置
   - 是否有 secrets 在日志中泄露
   - 第三方 Action 是否锁定了版本（SHA 而非 tag）

3. **依赖完整性**
   - 是否使用了 lock 文件
   - 是否验证了包的完整性（checksum）

---

## A09: 安全日志和监控失败 (Security Logging and Monitoring Failures)

### 检查项

1. **敏感数据入日志**
   - Grep 日志函数，检查是否记录了密码、token、信用卡号、身份证号
   - 检查错误日志是否泄露了堆栈信息和内部路径

2. **关键操作无审计**
   - 登录成功/失败是否记录
   - 权限变更、数据删除、配置修改是否记录
   - 支付操作是否有完整审计链

3. **日志注入**
   - 用户输入写入日志前是否清洗了换行符和控制字符

---

## A10: 服务端请求伪造 (SSRF)

### 检查项

1. **URL 参数处理**
   - Grep 所有发起 HTTP 请求的代码（`curl`、`fetch`、`requests`、`HttpClient`）
   - 检查 URL 是否包含用户输入
   - 是否校验了协议（只允许 http/https）
   - 是否校验了目标 IP（禁止内网、回环、云元数据地址）

2. **DNS 重绑定防护**
   - URL 校验后是否在实际请求前重新解析了域名
   - 是否关闭了自动重定向

3. **云环境元数据**
   - 是否拦截了 `169.254.169.254`（AWS/GCP/Azure 元数据服务）
   - 是否拦截了 `100.100.100.200`（阿里云元数据）
