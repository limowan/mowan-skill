# HyperFrames 编码规范与渲染命令

## 命令

```bash
# 初始化项目
cd 源文件/hyperframes && npx hyperframes init

# 验证
npx hyperframes lint

# 渲染
npx hyperframes render --output ../../产物/视频片段/{name}.mp4
```

## 编码规范

- 每个 timed 元素必须有 `class="clip"` + `data-start` + `data-duration` + `data-track-index`
- Timeline 必须 paused 并注册到 `window.__timelines`
- 使用 Google Fonts（`Noto Sans SC`）确保跨平台一致

## 适用场景

图文视频、标题卡、字幕、转场、快速排版类视频。
