# 实时预览工作流

制作动画时，应该边改边看，不要盲写代码再渲染。不同工具和环境的预览方式如下。

---

## 按工具分：怎么启动预览

### Remotion

启动本地 Studio 服务：

```bash
npx.cmd remotion studio --port 3001 --no-open
```

预览地址：`http://127.0.0.1:3001/{CompositionId}`

可以带参数跳到指定帧：`http://127.0.0.1:3001/{CompositionId}?frame=75`

Studio 支持实时热更新，改代码后浏览器自动刷新。

### HyperFrames

启动本地预览服务：

```bash
npx hyperframes preview --port 3002
```

预览地址：`http://127.0.0.1:3002`

### HTML / GSAP / SVG 特效

自包含 HTML 文件，直接在浏览器打开即可预览：

```
file:///path/to/源文件/effects/spotlight-title/index.html
```

或者用简易 HTTP 服务：

```bash
cd 源文件/effects/spotlight-title && npx serve -p 3003
```

预览地址：`http://127.0.0.1:3003`

### Manim

Manim 没有实时预览服务，用低质量快速渲染代替：

```bash
py -3.12 -m manim -ql scene.py ClassName --media_dir ../../产物/视频片段
```

渲染完后用浏览器打开生成的 MP4 文件预览。

---

## 按环境分：怎么打开预览

### Codex 环境（Browser Use 内置浏览器）

Codex 不会自动打开系统浏览器。必须通过 Browser Use 插件显式打开。

先读取 Browser Use 插件说明书获取完整 API：
```
C:\Users\Limmer\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha1\skills\browser\SKILL.md
```

基本用法：

```js
const { setupAtlasRuntime } = await import(
  "C:/Users/Limmer/.codex/plugins/cache/openai-bundled/browser-use/0.1.0-alpha1/scripts/browser-client.mjs"
);

await setupAtlasRuntime({
  globals: globalThis,
  backend: "iab",
});

const tab = await agent.browser.tabs.new();
await tab.goto("http://127.0.0.1:3001/CompositionId");
```

关键点：
- `backend: "iab"` 表示 Codex in-app browser，不是系统 Chrome/Edge
- 服务启动时必须加 `--no-open`，避免尝试打开系统浏览器
- 通过 `tab.goto()` 显式导航到 localhost 地址
- 可以用 `tab.playwright.*` API 做截图、交互验证

### Claude 桌面端（Claude Preview 内置浏览器）

Claude 桌面端有内置浏览器预览能力，通过 `preview_start` 启动服务，或直接用 `navigate` 打开已启动的本地服务：

```
# 如果服务已经手动启动
navigate → http://127.0.0.1:3001/{CompositionId}

# 或者通过 .claude/launch.json 配置自动启动
preview_start → 配置好的服务名
```

也可以用 `preview_screenshot` 截图检查画面效果。

### 本地开发（系统浏览器）

直接在终端启动服务，浏览器会自动打开：

```bash
npx.cmd remotion studio
```

---

## 预览检查清单

每次预览时确认：
- 文字是否清晰可读（字号、对比度）
- 动画节奏是否匹配旁白时长
- 转场是否流畅，没有黑屏或闪烁
- 颜色和字体是否符合视觉系统
- 移动端比例（9:16）下内容是否被裁切
