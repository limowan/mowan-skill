# Manim 编码规范与渲染命令

## 渲染命令

```bash
# 低质量预览（快速验证）
py -3.12 -m manim -ql scene_{name}.py {ClassName} --media_dir ../../产物/视频片段

# 确认效果后，高清渲染
py -3.12 -m manim -qh scene_{name}.py {ClassName} --media_dir ../../产物/视频片段
```

Manim 必须用 `py -3.12 -m manim`（Python 3.14 不兼容）。

## 编码规范

- 背景色统一深色（`#1a1a2e`）
- 中文字体用 `Microsoft YaHei`（Windows）或 `PingFang SC`（Mac）
- 颜色方案保持一致（在文件头定义常量）
- `self.wait()` 时间要匹配旁白时长，不要提前 FadeOut 到黑屏
- 每个场景文件对应脚本的一个段落

## 适用场景

算法动画、数学可视化、技术原理推导、公式演绎、几何变换。
