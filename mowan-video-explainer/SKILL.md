---
name: mowan-video-explainer
description: |
  视频解读助手。将技术报告、产品文档、文章、Skill 等内容转化为科普/解读视频。
  自动选择工具链（Manim/HyperFrames/Remotion），生成脚本、动画、配音、字幕，合成终版视频。
  使用场景：
  - "帮我做个视频解读这篇报告"、"做个产品介绍视频"
  - "把这个 Skill 做成演示视频"、"科普一下这个技术"
  - "做个解读视频"、"视频解读"、"做视频"
  - "帮我把这篇文章做成视频"、"技术科普视频"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion, TodoWrite
---

> **语言**: 本 Skill 使用简体中文交互。
>
> **兼容环境**: Claude Code、Cursor、Codex 等支持 Skill 的 AI 编程工具。
>
> **执行根目录**: 所有 `Bash` 命令中的相对路径基于本 `SKILL.md` 所在目录。`templates/...`、`tools/...` 均为相对路径。

# 墨玩视频解读 · mowan-video-explainer

将技术报告、产品文档、文章、Skill 等内容，转化为面向普通人的科普/解读视频。

## 触发条件

当用户说以下任意内容时启动：
- `/video-explainer`
- "帮我做个视频解读"
- "做个产品介绍视频"
- "把这个做成视频"
- "科普一下这个技术"
- "做个解读视频"
- "视频解读"

---

## 主流程：7 步

### Step 1：环境检测 & 依赖检查

#### 1a. 检测运行环境

```
检测当前环境：
- 当前目录存在 CLAUDE.md → Claude Code 环境
- 当前目录存在 AGENTS.md 但无 CLAUDE.md → Codex 环境
- 都不存在 → 询问用户确认环境
```

读取当前工作目录的 `CLAUDE.md`（或 `AGENTS.md`），从中获取：
- 视频工作区根目录路径
- 目录结构规范
- 工具链配置
- 约束规则

如果当前工作目录没有 `CLAUDE.md`，读取本 Skill 的 `templates/workspace-claude.md` 模板，询问用户视频工作区路径后，替换占位符并创建。同时创建 `AGENTS.md`（从 `templates/workspace-agents.md`）。

#### 1b. 依赖检查

运行 `tools/check_deps.py` 检测以下依赖的安装状态：

| 依赖 | 必须/可选 | 用途 |
|------|----------|------|
| FFmpeg | 必须 | 视频编码、合成 |
| Python 3.12 + Manim | 按需 | 技术原理动画 |
| Node.js + HyperFrames | 按需 | 图文视频、标题卡、转场 |
| Node.js + Remotion | 按需 | 产品宣传片、批量生成 |
| edge-tts | 按需 | TTS 自动配音 |
| openai-whisper | 按需 | 真人录音转字幕 |

缺少必须依赖时，给出安装命令并询问用户是否安装。可选依赖在 Step 2 确定工具链后再检查。

---

### Step 2：素材分析 & 类型判断

#### 2a. 读取素材

用户可能提供以下形式的输入：
- 本地文件路径（PDF、Markdown、Word、TXT）
- URL（文章链接、GitHub README）
- 直接粘贴的文本内容
- 截图/图片

读取素材内容，提取关键信息：
- 主题和核心观点
- 内容结构（章节、段落）
- 关键数据和图表
- 技术深度（面向专业人士 vs 面向小白）

#### 2b. 自动判断视频类型

根据素材内容特征，匹配最合适的视频类型和工具组合：

| 视频类型 | 识别信号 | 推荐工具 |
|---------|---------|---------|
| 技术原理科普 | 含公式、算法、架构图、论文格式 | Manim + HyperFrames |
| 产品宣传片 | 含品牌信息、功能列表、市场定位 | Remotion |
| 产品演示/教程 | 含操作步骤、截图、使用说明 | HyperFrames + 录屏 |
| 文章解读 | 公众号/博客文章、观点类内容 | HyperFrames |
| Skill/工具演示 | SKILL.md、README、CLI 文档 | HyperFrames + 录屏 |
| 数据可视化 | 大量数据、统计报告、对比表格 | Manim |
| 批量生成/模板化 | 系列内容、多语言需求 | Remotion |

展示推荐结果，询问用户确认或覆盖。

#### 2c. 确认视频参数

询问用户以下参数（提供默认值）：

```
视频参数确认：
- 目标时长：[3-5分钟 / 5-10分钟 / 10分钟以上]
- 画面比例：[16:9 横版（B站/YouTube） / 9:16 竖版（小红书/抖音） / 先做横版后面再说]
- 目标受众：[技术小白 / 有一定基础 / 专业人士]
- 发布平台：[B站 / 小红书 / YouTube / 公众号 / 其他]
- 配音方式：[TTS自动生成 / 自己录音 / 先TTS后面再换]
```

---

### Step 3：创建项目目录

在视频工作区的 `01_视频草稿/` 下创建项目文件夹：

```
{workspace_root}/01_视频草稿/{project_name}/
├── 源文件/
│   ├── manim/           ← Manim 场景代码（如果用 Manim）
│   ├── hyperframes/     ← HyperFrames 项目（如果用 HyperFrames）
│   └── remotion/        ← Remotion 项目（如果用 Remotion）
├── 素材/                ← 项目专属素材
├── 产物/
│   ├── clips/           ← 各段渲染片段
│   │   └── audio/       ← 配音文件
│   └── final/           ← 最终合成视频
└── 项目说明.md
```

从 `templates/project-readme.md` 生成 `项目说明.md`，填入项目信息。

---

### Step 4：视频脚本

#### 4a. 确认脚本来源

询问用户：

```
视频脚本怎么搞？
A. AI 生成 — 我根据素材自动写完整逐字稿，你审核修改
B. 你自己写 — 你提供脚本，我来匹配动画
C. 混合模式 — 我先出初稿，你改完确认
```

#### 4b. 脚本格式

无论哪种来源，最终脚本统一为以下格式：

```markdown
## 第 N 段：{段落标题}（{时长}）— {工具}

**【画面】** {画面描述}

**【旁白】**
{旁白文案}
```

如果用户自己提供脚本：
- **推荐带时间戳格式**（更精准匹配动画）：
  ```
  [00:00-00:15] 开场 Hook：如果AI能一口气读完10本三体...
  [00:15-01:15] 问题引入：为什么长文本这么难...
  ```
- **纯文本也可以**，Skill 会根据字数和语速自动估算每段时长（中文约 3-4 字/秒）

#### 4c. AI 生成脚本的原则

- 面向目标受众调整语言难度
- 用生活化比喻解释技术概念
- 每段有明确的画面描述，方便后续制作动画
- 开场必须有 Hook（提问/悬念/数据冲击）
- 结尾有总结和 CTA（关注/点赞/下期预告）
- 控制在目标时长范围内

脚本完成后，必须展示给用户确认，确认后才进入制作。

---

### Step 5：制作动画

根据脚本逐段生成动画。不同工具的制作流程：

#### Manim 场景

```bash
# 1. 创建场景文件
# 源文件/manim/scene_{name}.py

# 2. 低质量预览（快速验证）
py -3.12 -m manim -ql scene_{name}.py {ClassName} --media_dir ../../产物/clips

# 3. 确认效果后，高清渲染
py -3.12 -m manim -qh scene_{name}.py {ClassName} --media_dir ../../产物/clips
```

Manim 编码规范：
- 背景色统一深色（`#1a1a2e`）
- 中文字体用 `Microsoft YaHei`（Windows）或 `PingFang SC`（Mac）
- 颜色方案保持一致（在文件头定义常量）
- `self.wait()` 时间要匹配旁白时长，不要提前 FadeOut 到黑屏
- 每个场景文件对应脚本的一个段落

#### HyperFrames

```bash
# 1. 初始化项目（如果还没有）
cd 源文件/hyperframes && npx hyperframes init

# 2. 编辑 index.html（clip + GSAP timeline）

# 3. 验证
npx hyperframes lint

# 4. 渲染
npx hyperframes render --output ../../产物/clips/{name}.mp4
```

HyperFrames 编码规范：
- 每个 timed 元素必须有 `class="clip"` + `data-start` + `data-duration` + `data-track-index`
- Timeline 必须 paused 并注册到 `window.__timelines`
- 使用 Google Fonts（`Noto Sans SC`）确保跨平台一致

#### Remotion

```bash
# 1. 创建项目
cd 源文件 && npx create-video@latest remotion

# 2. 开发组件（React）

# 3. 预览
cd remotion && npx remotion preview

# 4. 渲染
npx remotion render src/index.ts {CompositionId} ../../产物/clips/{name}.mp4
```

每段渲染完后，检查时长是否匹配脚本预期。

---

### Step 6：配音处理

#### 模式 A：TTS 自动生成

```bash
# 使用 edge-tts，推荐音色：
# 男声科技感：zh-CN-YunxiNeural
# 女声温柔：zh-CN-XiaoxiaoNeural
# 男声新闻播报：zh-CN-YunjianNeural

edge-tts --voice "zh-CN-YunxiNeural" --rate="-5%" \
  --text "旁白文案" \
  --write-media 产物/clips/audio/{segment}.mp3
```

每段旁白单独生成一个音频文件，方便后续逐段匹配。

#### 模式 B：真人录音

用户提供录音文件后：

1. 用 Whisper 转写出带时间戳的字幕：
   ```bash
   whisper 录音.mp3 --language zh --output_format srt --output_dir 产物/clips/audio/
   ```
2. 根据 SRT 时间戳，调整每段 Manim 动画的 `self.wait()` 时间
3. 重新渲染动画
4. 合成

#### 模式 C：先 TTS 后替换

先按模式 A 生成 TTS 版本，出预览视频。用户满意后录制真人版本，按模式 B 替换。

#### 字幕生成

无论哪种模式，都生成 SRT 字幕文件，用于：
- 视频内嵌字幕（硬字幕）
- 平台上传字幕（软字幕）

---

### Step 7：合成终版

#### 7a. 逐段合并视频+音频

每段视频和对应音频合并，视频不够长时用最后一帧填充（不是黑屏）：

```bash
ffmpeg -y -i {video}.mp4 -i {audio}.mp3 \
  -filter_complex "[0:v]scale=1920:1080,fps=30,tpad=stop=-1:stop_mode=clone:stop_duration={max_dur}[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset fast -crf 18 -c:a aac -shortest \
  {output_segment}.mp4
```

#### 7b. 拼接所有段落

```bash
ffmpeg -y \
  -i seg_01.mp4 -i seg_02.mp4 ... \
  -filter_complex "[0:v][0:a][1:v][1:a]...concat=n=N:v=1:a=1[vout][aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k \
  {final_output}.mp4
```

#### 7c. 可选：混入 BGM

```bash
# BGM 音量压低到 10-15%，不抢配音
ffmpeg -y -i {video_with_voice}.mp4 -i {bgm}.mp3 \
  -filter_complex "[1:a]volume=0.12[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac \
  {final_with_bgm}.mp4
```

免版权 BGM 来源（国内优先）：
- Pixabay Music（pixabay.com/music，国内可直接访问，CC0 协议）
- FreePD.com（公共领域，零限制）
- 爱给网（aigei.com，有免费可商用音乐区）
- 淘声网（tosound.com，免费音效和音乐）
- YouTube Audio Library（需科学上网，完全免费商用）

#### 7d. 可选：烧录字幕

```bash
ffmpeg -y -i {video}.mp4 -vf "subtitles={srt_file}:force_style='FontSize=22,FontName=Microsoft YaHei'" \
  -c:v libx264 -crf 18 -c:a copy {final_with_subs}.mp4
```

#### 7e. 输出

最终视频输出到 `产物/final/`，命名格式：`{项目名}_终版.mp4`

输出后展示：
- 文件路径和大小
- 视频时长
- 分辨率和帧率
- 提醒用户预览检查

---

## 注意事项

- 所有渲染输出统一 MP4（H.264），除非平台有特殊要求
- Manim 必须用 `py -3.12 -m manim`（Python 3.14 不兼容）
- 素材版权自查：使用外部素材前确认授权
- 视频项目不进 git（文件太大），用目录结构管理版本
- 每个步骤完成后主动告知用户进度，关键节点等待用户确认
