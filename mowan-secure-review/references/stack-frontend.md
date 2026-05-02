# 前端技术栈安全清单

检测信号：`react`/`vue`/`angular`/`svelte` 在 package.json 依赖中，`.jsx`/`.tsx`/`.vue` 文件

---

## React 特定

1. **dangerouslySetInnerHTML**
   - Grep: `dangerouslySetInnerHTML`
   - 检查 `__html` 的值是否包含用户输入或未清洗的外部数据
   - 如果值来自 API 且 API 返回用户生成内容 → High（存储型 XSS）
   - 如果值来自可信的 CMS 且经过清洗 → Info

2. **URL 注入**
   - `href={userInput}` — 如果 userInput 可以是 `javascript:alert(1)` → Medium
   - 检查是否校验了 URL 协议（只允许 http/https）
   - `window.location = userInput` → Medium

3. **服务端渲染 (SSR) XSS**
   - Next.js `getServerSideProps` 返回的数据是否包含未转义的用户输入
   - 序列化到 `__NEXT_DATA__` 的数据是否可能包含 XSS payload

4. **状态泄露**
   - Redux/Zustand store 中是否存储了不应暴露给前端的敏感数据
   - SSR 时服务端状态是否泄露到客户端（hydration 数据）

---

## Vue 特定

1. **v-html 指令**
   - Grep: `v-html`
   - 与 React 的 `dangerouslySetInnerHTML` 同等风险
   - 检查绑定的值是否包含用户输入

2. **模板编译**
   - `Vue.compile(userInput)` → Critical（模板注入）
   - 运行时模板编译（`template` 选项接受用户输入）→ Critical

3. **Nuxt.js**
   - `asyncData` / `fetch` 返回的数据是否安全
   - 服务端 API 密钥是否泄露到客户端 bundle

---

## Angular 特定

1. **bypassSecurityTrust***
   - Grep: `bypassSecurityTrustHtml`、`bypassSecurityTrustScript`、`bypassSecurityTrustUrl`
   - 每个使用点都需要确认输入来源是否可信

2. **模板注入**
   - 用户输入是否被用作 Angular 模板（`{{userInput}}` 在服务端拼接）

---

## 通用前端安全

### Source Map 泄露

- 检查生产构建是否生成了 `.map` 文件
- 检查 `.map` 文件是否可通过 Web 访问
- Source map 泄露完整源码 → Medium

### localStorage / sessionStorage

- 是否在 localStorage 中存储了 JWT Token（XSS 可读取）→ Medium
- 是否在 localStorage 中存储了敏感用户数据
- 建议：敏感 token 存储在 HttpOnly Cookie 中

### postMessage

- Grep: `window.postMessage`、`addEventListener('message'`
- 接收 message 时是否校验了 `event.origin`
- 未校验 origin → Medium（跨域消息伪造）

### 第三方脚本

- 是否引入了第三方 JS（广告、分析、聊天插件）
- 第三方脚本是否使用了 SRI（Subresource Integrity）
- 第三方脚本可以访问页面上的所有数据

### 依赖安全

- 运行 `npm audit`（如果可用）
- 检查是否有已知 XSS 漏洞的前端库
- 检查 CDN 引用的库版本
