# Python 技术栈安全清单

检测信号：`requirements.txt`、`pyproject.toml`、`setup.py`、`Pipfile`、`.py` 文件

---

## 模板注入 (SSTI)

**检查方法**：
- Jinja2: `render_template_string(user_input)` → Critical
- Mako: `Template(user_input).render()` → Critical
- 安全模式：`render_template('page.html', name=user_input)` → 安全

**攻击向量**：
- `{{7*7}}` → 如果返回 `49`，存在 SSTI
- `{{config}}` → 泄露 Flask 配置（含 SECRET_KEY）

---

## 不安全的反序列化

**检查方法**：
- Grep: `pickle.loads(`、`pickle.load(`、`yaml.load(` (无 `Loader=SafeLoader`)
- `pickle` 反序列化不可信数据 → Critical（可 RCE）
- `yaml.load()` 默认不安全（Python < 3.9），应使用 `yaml.safe_load()`

**判定标准**：
- 用户输入传入 `pickle.loads()` → Critical
- `yaml.load()` 无 SafeLoader → High（如果输入来自用户）

---

## Django 特定

1. **SECRET_KEY**: 是否硬编码在 `settings.py` 中（应从环境变量读取）
2. **DEBUG**: 生产环境 `DEBUG = True` → 泄露完整设置和堆栈
3. **ALLOWED_HOSTS**: 是否为 `['*']`（应限制为实际域名）
4. **CSRF**: `@csrf_exempt` 装饰器的使用是否合理
5. **SQL 注入**: `.extra()`、`.raw()`、`RawSQL()` 中的用户输入
6. **ORM 绕过**: `__regex`、`__contains` 等 lookup 是否接受用户输入构造
7. **Admin**: Django Admin 是否暴露在公网且无额外保护

---

## Flask 特定

1. **SECRET_KEY**: 是否硬编码或使用弱密钥
2. **Debug 模式**: `app.run(debug=True)` 在生产环境 → 可通过 debugger PIN 获取 RCE
3. **Session**: Flask 默认使用客户端 session（签名但未加密），SECRET_KEY 泄露 = session 伪造

---

## FastAPI 特定

1. **自动文档**: `/docs` 和 `/redoc` 是否在生产环境暴露
2. **CORS**: `allow_origins=["*"]` + `allow_credentials=True` → 危险组合
3. **依赖注入**: 安全依赖（认证检查）是否正确应用到所有需要保护的路由

---

## 命令注入

**检查方法**：
- Grep: `os.system(`、`os.popen(`、`subprocess.call(.*shell=True`、`subprocess.Popen(.*shell=True`
- `shell=True` + 用户输入 → Critical
- 安全替代：`subprocess.run(['cmd', arg1, arg2], shell=False)`

---

## 路径穿越

**检查方法**：
- Grep: `open(`、`os.path.join(`
- `os.path.join('/base', user_input)` — 如果 `user_input` 以 `/` 开头，会忽略前面的路径
- 安全模式：`os.path.realpath()` + 检查是否在允许目录内

---

## 依赖安全

- 运行 `pip-audit`（如果可用）
- 检查是否使用了 `requirements.txt` 锁定版本（而非 `>=`）
- 检查是否有已知漏洞的依赖
