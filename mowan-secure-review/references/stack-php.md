# PHP 技术栈安全清单

检测信号：`composer.json`、`.php` 文件、`artisan`（Laravel）、`symfony`

---

## 类型混淆 (Type Juggling)

PHP 的松散比较（`==`）在安全场景中极其危险。

**检查方法**：
- Grep 认证/授权代码中的 `==` 比较（应使用 `===`）
- 特别关注：密码比较、token 验证、权限检查
- `"0e123" == "0e456"` 在 PHP 中为 `true`（科学计数法）
- `0 == "any-string"` 在 PHP < 8.0 中为 `true`

**判定标准**：
- 认证逻辑中使用 `==` 比较密码/token → High
- PHP >= 8.0 已修复部分问题，但仍需检查

---

## 反序列化

**检查方法**：
- Grep: `unserialize(`，检查输入来源
- 用户可控数据传入 `unserialize()` → Critical（可 RCE）
- 安全替代：`json_decode()`、`json_encode()`

**框架特定**：
- Laravel: 检查是否使用了不安全的序列化 Cookie（`APP_KEY` 泄露 + 序列化 Cookie = RCE）

---

## 文件包含

**检查方法**：
- Grep: `include`、`require`、`include_once`、`require_once`
- 检查路径是否包含用户输入
- 本地文件包含 (LFI): `include("pages/" . $_GET['page'] . ".php")`
- 远程文件包含 (RFI): `allow_url_include = On`（检查 php.ini）

**判定标准**：
- 用户输入直接进入 include 路径 → Critical
- `allow_url_include` 开启 → High

---

## 危险函数

**Grep 以下函数 + 检查输入来源**：
- 命令执行: `exec`、`system`、`passthru`、`shell_exec`、`popen`、`proc_open`、反引号
- 代码执行: `eval`、`assert`、`preg_replace` (带 `/e` 修饰符，PHP < 7.0)
- 文件操作: `file_get_contents`、`file_put_contents`、`fopen`、`readfile`、`move_uploaded_file`

---

## Laravel 特定

1. **Mass Assignment**: 检查 `$fillable` / `$guarded` 是否正确配置
2. **SQL 注入**: `DB::raw()`、`whereRaw()`、`selectRaw()` 中的用户输入
3. **CSRF**: 检查 `VerifyCsrfToken` 中间件的排除列表
4. **Debug 模式**: `APP_DEBUG=true` 在生产环境 → 泄露完整堆栈和环境变量
5. **APP_KEY**: 泄露后可伪造加密数据、解密 Cookie → Critical

---

## PHP 配置 (php.ini)

**检查项**：
- `display_errors = Off`（生产环境）
- `expose_php = Off`（隐藏 PHP 版本）
- `allow_url_include = Off`
- `allow_url_fopen` — 如果不需要应关闭
- `open_basedir` — 限制文件访问范围
- `disable_functions` — 禁用危险函数
- `session.cookie_httponly = 1`
- `session.cookie_secure = 1`（HTTPS 环境）
- `session.use_strict_mode = 1`
