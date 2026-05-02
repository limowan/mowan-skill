# Node.js 技术栈安全清单

检测信号：`package.json`、`node_modules/`、`.js`/`.ts` 文件

---

## 原型链污染 (Prototype Pollution)

**检查方法**：
- Grep 深度合并/递归赋值函数：`merge(`、`extend(`、`deepMerge(`、`_.merge(`、`_.defaultsDeep(`
- 检查是否接受用户输入作为对象键名
- 攻击向量：`{"__proto__": {"isAdmin": true}}`、`{"constructor": {"prototype": {"isAdmin": true}}}`

**判定标准**：
- 用户输入直接用于对象属性赋值且无过滤 → High
- 使用了已知有漏洞的 lodash 版本的 merge → High

---

## npm 供应链安全

**检查方法**：
- 运行 `npm audit`（如果可用）
- 检查 `package-lock.json` 是否提交（确保依赖版本锁定）
- 检查是否有可疑的 `preinstall`/`postinstall` 脚本
- 检查依赖名称是否可能是 typosquatting（如 `lodahs` vs `lodash`）

---

## Express 特定

1. **中间件顺序**：安全中间件（helmet、cors、rate-limit）是否在路由之前
2. **错误处理**：默认错误处理器是否泄露堆栈信息（生产环境应自定义）
3. **信任代理**：`trust proxy` 设置是否正确（影响 IP 获取和速率限制）
4. **Body 解析**：`express.json()` 的 `limit` 是否设置（防止大 payload 攻击）

---

## 正则表达式 DoS (ReDoS)

**检查方法**：
- Grep 用户输入传入正则匹配的代码
- 检查正则是否有嵌套量词（如 `(a+)+`、`(a|a)*`）
- 这类正则在特定输入下会导致指数级回溯

**判定标准**：
- 用户输入直接用于正则匹配且正则有回溯风险 → Medium

---

## 服务端模板注入

**检查方法**：
- EJS: `ejs.render(userInput)` → Critical
- Pug: 用户输入作为模板内容 → Critical
- Handlebars: 检查是否注册了不安全的 helper

---

## 文件系统操作

**检查方法**：
- Grep: `fs.readFile`、`fs.writeFile`、`fs.unlink`、`path.join`
- 检查路径是否包含用户输入
- `path.join('/base', userInput)` 不能防止 `../` 穿越（需要 `path.resolve` + 前缀检查）

---

## 环境变量

- `NODE_ENV` 是否在生产环境设为 `production`
- 敏感环境变量是否通过 `process.env` 正确读取（而非硬编码）
- 前端框架（Next.js/Vite/CRA）的环境变量前缀规则是否遵守
