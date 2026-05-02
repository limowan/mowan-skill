# 基础设施安全清单

覆盖 Web 服务器、容器、CI/CD、安全响应头、CORS 等基础设施层面的安全检查。

---

## Web 服务器配置

### Nginx

**检查项**：

1. **敏感文件暴露**
   - 是否拦截了 `.env`、`.git/`、`.svn/`、`.log`、`.sql`、`.db`、`.sqlite`
   - 是否拦截了 `node_modules/`、`vendor/`、`__pycache__/`
   - 是否拦截了备份文件（`.bak`、`.old`、`.tmp`、`.swp`）
   - 数据目录（如 `/data/`）是否禁止访问

2. **目录列表**
   - `autoindex` 是否关闭（默认关闭，但要确认）

3. **版本信息**
   - `server_tokens off;` 是否配置（隐藏 Nginx 版本）

4. **请求限制**
   - 是否配置了 `client_max_body_size`（防止大文件上传攻击）
   - 是否配置了 `limit_req` / `limit_conn`（基础限流）

5. **代理安全**
   - 反向代理是否正确传递了客户端真实 IP
   - 是否限制了可信的 `X-Forwarded-For` 来源
   - 上游服务是否只监听 localhost

### Apache

**检查项**：
- `.htaccess` 是否正确配置
- `Options -Indexes` 是否设置
- `ServerSignature Off` 和 `ServerTokens Prod`
- `AllowOverride` 是否过于宽松

---

## 安全响应头

### 检查项

| 头部 | 作用 | 检查方法 |
|------|------|---------|
| `X-Content-Type-Options: nosniff` | 防止 MIME 类型嗅探 | Grep 响应头设置代码或 Nginx 配置 |
| `X-Frame-Options: DENY/SAMEORIGIN` | 防止点击劫持 | 同上 |
| `Content-Security-Policy` | 防止 XSS、数据注入 | 检查策略是否过于宽松（`unsafe-inline`、`unsafe-eval`、`*`） |
| `Strict-Transport-Security` | 强制 HTTPS | 检查 `max-age` 是否足够长（建议 >= 1年） |
| `Referrer-Policy` | 控制 Referer 泄露 | 建议 `same-origin` 或 `strict-origin-when-cross-origin` |
| `Permissions-Policy` | 限制浏览器功能 | 检查是否禁用了不需要的功能（camera、microphone、geolocation） |
| `X-XSS-Protection` | 已废弃，但不应设为 `0` | 现代浏览器已移除，CSP 替代 |

### 判定标准

- 完全缺失安全响应头 → Low（除非有具体利用场景则升级）
- CSP 使用了 `unsafe-inline` + `unsafe-eval` → Medium（削弱了 XSS 防护）
- 缺少 HSTS 且站点处理敏感数据 → Medium

---

## CORS 配置

### 检查项

1. **Origin 校验**
   - `Access-Control-Allow-Origin: *` → 如果接口需要认证则为 High
   - 动态反射 Origin 而无白名单校验 → High
   - 正则匹配 Origin 但正则有缺陷（如 `.*\.example\.com` 匹配 `evil-example.com`）→ High

2. **凭证传递**
   - `Access-Control-Allow-Credentials: true` + `Allow-Origin: *` → 浏览器会拒绝，但代码逻辑有问题
   - `Credentials: true` + 动态反射 Origin → Critical（任意站点可带 Cookie 请求）

3. **预检请求**
   - `Access-Control-Allow-Methods` 是否过于宽松
   - `Access-Control-Allow-Headers` 是否允许了不必要的自定义头

---

## Docker 安全

### 检查项

1. **镜像安全**
   - 是否使用了官方基础镜像
   - 基础镜像是否指定了具体版本（非 `latest`）
   - 是否使用了多阶段构建（减少最终镜像中的构建工具）

2. **运行时安全**
   - 容器是否以 root 运行（检查 `USER` 指令）
   - 是否使用了 `--privileged` 模式
   - 是否挂载了 Docker socket（`/var/run/docker.sock`）

3. **敏感信息**
   - Dockerfile 中是否用 `ENV` 设置了密钥（会留在镜像层中）
   - 是否用 `COPY` 复制了 `.env` 文件到镜像中
   - 构建参数（`ARG`）中是否包含密钥（会留在镜像历史中）
   - docker-compose.yml 中是否硬编码了敏感环境变量

4. **网络隔离**
   - 是否暴露了不必要的端口
   - 内部服务是否只在内部网络可达
   - 数据库端口是否暴露到宿主机

---

## CI/CD 管道安全

### 检查项

1. **Secrets 管理**
   - CI 配置中是否硬编码了密钥（应使用 CI 平台的 secret 管理）
   - Secret 是否在日志中被打印（检查 `echo $SECRET`、debug 输出）
   - PR 从 fork 提交时是否能访问 secrets

2. **第三方 Action/Plugin**
   - GitHub Actions 是否锁定了 SHA 版本（而非 tag，tag 可被覆盖）
   - 是否使用了来源不明的第三方 Action
   - Action 的权限是否最小化

3. **构建产物安全**
   - 构建产物是否包含源码或 source map
   - 构建产物是否包含测试凭证
   - 部署脚本是否有适当的权限控制

4. **管道权限**
   - CI 服务账号的权限是否最小化
   - 是否有分支保护规则（防止直接推送到 main）
   - 部署到生产是否需要人工审批

---

## TLS/SSL 配置

### 检查项

1. **协议版本**
   - 是否禁用了 SSLv3、TLS 1.0、TLS 1.1
   - 是否支持 TLS 1.2 和 TLS 1.3

2. **证书**
   - 证书是否即将过期
   - 证书链是否完整
   - 是否使用了自签名证书（生产环境）

3. **密码套件**
   - 是否禁用了弱密码套件（RC4、DES、3DES、NULL）
   - 是否优先使用前向保密（ECDHE）

---

## 文件上传安全

### 检查项

1. **文件类型校验**
   - 是否只检查了扩展名（可绕过：`shell.php.jpg`、`shell.php%00.jpg`）
   - 是否检查了 MIME type（Content-Type 头可伪造）
   - 是否检查了文件内容/魔术字节（最可靠）

2. **存储安全**
   - 上传文件是否存储在 Web 可访问目录外
   - 文件名是否重新生成（防止路径穿越和覆盖）
   - 上传目录是否禁止执行脚本

3. **大小限制**
   - 是否有文件大小限制
   - 是否有上传频率限制

4. **危险文件类型**
   - 是否允许上传 `.php`、`.jsp`、`.asp`、`.exe`、`.sh`、`.bat`
   - SVG 文件是否可能包含 XSS（SVG 可内嵌 JavaScript）
   - ZIP 文件解压是否有 Zip Slip 防护
