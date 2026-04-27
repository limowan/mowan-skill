# Remotion 编码规范与渲染命令

## 命令

```bash
# 创建项目
cd 源文件 && npx create-video@latest remotion

# 预览
cd remotion && npx remotion preview

# 渲染
npx remotion render src/index.ts {CompositionId} ../../产物/视频片段/{name}.mp4
```

## 设计要求

- 开始写 React 组件前，先根据"视频设计方案"确定场景清单和视觉系统
- 视觉系统至少包括：主色/强调色、字体层级、卡片/标签样式、转场节奏
- 面向小白的解释视频，优先使用可视化隐喻，不要做成 PPT 翻页
- 短视频表达要有节奏：开头抓人，中段不断给反馈，结尾回收记忆点

## GPU 渲染规则

- **Windows + NVIDIA**：不要依赖 `npx remotion render --hardware-acceleration`，该参数在 Windows 下不能让 H.264 走 GPU。先让 Remotion 生成高质量中间产物，再用 FFmpeg `h264_nvenc` 一次性编码最终 MP4
- **MacBook**：优先使用 `npx remotion render ... --hardware-acceleration=if-possible`；如果要确认一定走 GPU，先用 `--hardware-acceleration=required` 渲染 10 秒样本
- **不支持 GPU 时**：保持 CPU `libx264 -crf 18`，确保稳定出片

## 适用场景

产品宣传片、品牌化视频、数据可视化、批量生成、系列视频。
