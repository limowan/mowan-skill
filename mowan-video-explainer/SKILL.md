---
name: mowan-video-explainer
description: |
  视频解读助手。将技术报告、产品文档、文章、Skill 等内容转化为科普/解读视频。
  先做视频方案设计（2-3 个方案对比），用户确认后再生成脚本、动画、配音、字幕，合成终版视频。
  工具不限于 Remotion，AI 根据内容需求自由选择和创造动效方案。
  使用场景：
  - "帮我做个视频解读这篇报告"、"做个产品介绍视频"
  - "把这个 Skill 做成演示视频"、"科普一下这个技术"
  - "做个解读视频"、"视频解读"、"做视频"
  - "帮我把这篇文章做成视频"、"技术科普视频"
version: "2.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion, TodoWrite
---

> **语言**: 本 Skill 使用简体中文交互。
>
> **兼容环境**: Claude Code、Cursor、Codex 等支持 Skill 的 AI 编程工具。
>
> **执行根目录**: 所有 `Bash` 命令中的相对路径基于本 `SKILL.md` 所在目录。

# 墨玩视频解读 · mowan-video-explainer

将技术报告、产品文档、文章、Skill 等内容，转化为面向普通人的科普/解读视频。

## 触发条件

当用户说以下任意内容时启动：
- `/video-explainer`
- "帮我做个视频解读"、"做个产品介绍视频"、"把这个做成视频"
- "科普一下这个技术"、"做个解读视频"、"视频解读"

---

## 资源文件索引

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/effects-thinking.md` | 动效设计思考框架 | Step 3 视频方案设计时 |
| `references/tool-manim.md` | Manim 编码规范和渲染命令 | 确定使用 Manim 后 |
| `references/tool-hyperframes.md` | HyperFrames 编码规范和渲染命令 | 确定使用 HyperFrames 后 |
| `references/tool-remotion.md` | Remotion 编码规范和 GPU 渲染规则 | 确定使用 Remotion 后 |
| `references/tool-html-effects.md` | HTML/GSAP/SVG/Three.js 特效制作规则 | 需要制作特效片段时 |
| `references/rendering-and-encoding.md` | GPU 检测 + FFmpeg 编码参数 + 合成命令 | Step 1 环境检测 + Step 8 合成时 |
| `references/preview-workflow.md` | 实时预览工作流（按工具 + 按环境） | Step 6 制作动画时 |
| `config.example.json` | 生图能力配置示例 | Step 6 需要生成图片素材时 |

---

## 主流程：8 步

### Step 1：环境检测 & 依赖检查

#### 1a. 检测运行环境

```
检测当前环境：
- 当前目录存在 CLAUDE.md → Claude Code 环境
- 当前目录存在 AGENTS.md 但无 CLAUDE.md → Codex 环境
- 都不存在 → 询问用户确认环境
```

读取当前工作目录的 `CLAUDE.md`（或 `AGENTS.md`），获取视频工作区路径、目录结构规范等。

如果当前工作目录没有 `CLAUDE.md`，读取 `templates/workspace-claude.md` 模板，询问用户视频工作区路径后创建。同时创建 `AGENTS.md`（从 `templates/workspace-agents.md`）。

#### 1b. 依赖检查

运行 `tools/check_deps.py` 检测依赖：

| 依赖 | 必须/可选 | 用途 |
|------|----------|------|
| FFmpeg | 必须 | 视频编码、合成 |
| Python 3.12 + Manim | 按需 | 技术原理动画 |
| Node.js + HyperFrames | 按需 | 图文视频、标题卡、转场 |
| Node.js + Remotion | 按需 | 产品宣传片、批量生成 |
| edge-tts | 按需 | TTS 自动配音 |
| openai-whisper | 按需 | 真人录音转字幕 |

缺少必须依赖时给出安装命令。可选依赖在 Step 3 确定工具链后再检查。

#### 1c. GPU 渲染能力检测

运行 `python tools/check_deps.py --gpu`，详细策略见 `references/rendering-and-encoding.md`。

对用户说"默认启用 GPU 渲染，加快视频导出"即可。

---

### Step 2：素材分析

#### 2a. 读取素材

用户可能提供：本地文件（PDF、Markdown、Word、TXT）、URL、直接粘贴的文本、截图/图片。

读取素材内容，提取：主题和核心观点、内容结构、关键数据和图表、技术深度。

#### 2b. 自动判断视频类型

| 视频类型 | 识别信号 | 推荐工具 |
|---------|---------|---------|
| 技术原理科普 | 含公式、算法、架构图、论文格式 | Manim + HyperFrames |
| 产品宣传片 | 含品牌信息、功能列表、市场定位 | Remotion + 特效 |
| 产品演示/教程 | 含操作步骤、截图、使用说明 | Remotion/HyperFrames + 录屏 |
| 文章解读 | 公众号/博客文章、观点类内容 | HyperFrames/Remotion |
| Skill/工具演示 | SKILL.md、README、CLI 文档 | Remotion/HyperFrames + 录屏 |
| 数据可视化 | 大量数据、统计报告、对比表格 | Manim |

展示推荐结果，询问用户确认或覆盖。

#### 2c. 确认视频参数

```
视频参数确认：
- 目标时长：[3-5分钟 / 5-10分钟 / 10分钟以上]
- 画面比例：[16:9 横版 / 9:16 竖版 / 先做横版后面再说]
- 目标受众：[技术小白 / 有一定基础 / 专业人士]
- 发布平台：[B站 / 小红书 / YouTube / 公众号 / 其他]
- 配音方式：[TTS自动生成 / 自己录音 / 先TTS后面再换]
```

---

### Step 3：视频方案设计

读取 `references/effects-thinking.md`。

根据 Step 2 的素材分析结果，设计 **2-3 个差异明显的视频方案**。

每个方案包含：
- **方案名称**（一句话概括风格方向，如"科技感数据叙事"、"手绘故事线"、"极简留白"）
- **核心一句话**：这支视频帮观众看懂什么
- **视觉风格**：色彩、字体、镜头节奏、整体感觉
- **开场 Hook 设计**：前 5-10 秒怎么抓人
- **记忆点设计**：核心比喻 / 金句 / 视觉锚点
- **动效策略**：3-5 个关键画面的动效设计
  - 从内容需求出发，不限于任何固定列表
  - 每个动效说明：用在哪、为什么、用什么工具做
- **工具组合**：主工具 + 辅助工具，说明选择理由
- **节奏结构**：开场 → 各段节奏 → 结尾
- **这个方案的优势和局限**

方案之间应有明显差异，例如：
- 方案 A 偏科技感，Remotion 主导，数据驱动动画
- 方案 B 偏故事感，HyperFrames 图文为主，手绘风 SVG 点缀
- 方案 C 偏极简，Manim 核心动画，大量留白和节奏呼吸

展示方案后，让用户：
1. 直接选一个
2. 混搭（"A 的视觉风格 + B 的开场 Hook"）
3. 提出新方向，AI 重新设计

用户确认后，输出最终"视频设计方案"写入项目说明.md，再进入 Step 4。

---

### Step 4：创建项目目录

在视频工作区的 `01_视频草稿/` 下创建项目文件夹：

```
{workspace_root}/01_视频草稿/{project_name}/
├── 源文件/
│   ├── manim/           ← Manim 场景代码（如果用 Manim）
│   ├── hyperframes/     ← HyperFrames 项目（如果用 HyperFrames）
│   ├── remotion/        ← Remotion 项目（如果用 Remotion）
│   └── effects/         ← HTML/GSAP/SVG/Three.js 特效工程
├── 素材/
├── 产物/
│   ├── 视频片段/
│   ├── 配音文件/
│   └── 最终视频/
└── 项目说明.md
```

从 `templates/project-readme.md` 生成 `项目说明.md`，填入项目信息和确认的视频设计方案。

---

### Step 5：视频脚本

#### 5a. 确认脚本来源

```
视频脚本怎么搞？
A. AI 生成 — 我根据素材自动写完整逐字稿，你审核修改
B. 你自己写 — 你提供脚本，我来匹配动画
C. 混合模式 — 我先出初稿，你改完确认
```

默认选 C。

#### 5b. 脚本格式

```markdown
## 第 N 段：{段落标题}（{时长}）— {工具}

**【画面】** {画面描述}

**【旁白】**
{旁白文案}
```

用户自己提供脚本时，推荐带时间戳格式，纯文本也可以（按中文约 3-4 字/秒估算时长）。

#### 5c. AI 生成脚本的原则

- 面向目标受众调整语言难度，用生活化比喻解释技术概念
- 开场必须有 Hook（提问/悬念/数据冲击）
- 每 20-40 秒设计一个节奏变化
- 避免平铺直叙的说明书口吻，优先"问题驱动 + 例子解释 + 一句话总结"
- 结尾有总结和 CTA

脚本完成后，展示给用户确认，确认后才进入制作。

---

### Step 6：制作动画

根据脚本逐段生成动画。读取对应工具的 reference 文件：

- 使用 Manim → 读取 `references/tool-manim.md`
- 使用 HyperFrames → 读取 `references/tool-hyperframes.md`
- 使用 Remotion → 读取 `references/tool-remotion.md`
- 需要特效片段 → 读取 `references/tool-html-effects.md`

制作原则：
- 每段先确定"这一屏观众应该记住什么"，再决定构图和动画
- 多用直观视觉语言，不要只把文字摆上去
- 字幕和标题为小白服务：短句、强重点、可扫读
- 工具可以混合使用，按效果和效率选
- **边改边看**：读取 `references/preview-workflow.md`，根据当前环境启动实时预览

#### 图片素材生成

视频制作中如需生成图片素材（封面、背景、插图、图标等），按环境选择生图方式：

- **Codex 环境**：使用内置 `image_gen` 直接生成
- **其它环境**：读取 `config.json`，调用 `imageGenerationSkills[]` 中配置的生图 Skill
  - 如果 `config.json` 不存在，读取 `config.example.json`，引导用户复制并填写真实路径
  - 如果配置的 Skill 不可用，检索当前环境其它可用的生图 Skill，让用户确认后使用

每段渲染完后，检查时长是否匹配脚本预期。

---

### Step 7：配音处理

#### 模式 A：TTS 自动生成

```bash
edge-tts --voice "zh-CN-YunxiNeural" --rate="-5%" \
  --text "旁白文案" \
  --write-media 产物/配音文件/{segment}.mp3
```

推荐音色：男声科技感 `zh-CN-YunxiNeural`、女声温柔 `zh-CN-XiaoxiaoNeural`、男声播报 `zh-CN-YunjianNeural`。

#### 模式 B：真人录音

用户提供录音后，用 Whisper 转写字幕，根据时间戳调整动画时长，重新渲染。

#### 模式 C：先 TTS 后替换

先按模式 A 出预览版，确认后录真人版替换。

#### 字幕生成

无论哪种模式，都生成 SRT 字幕文件。

---

### Step 8：合成终版

读取 `references/rendering-and-encoding.md`，按 GPU 检测结果选择编码策略。

流程：逐段合并视频+音频 → 拼接所有段落 → 可选混入 BGM → 可选烧录字幕。

也可以直接使用 `tools/merge_video.py` 一步完成合成。

最终视频输出到 `产物/最终视频/`，命名 `{项目名}_终版.mp4`。

输出后展示文件路径、大小、时长、分辨率，提醒用户预览检查。

---

## 注意事项

- 所有渲染输出统一 MP4（H.264），除非平台有特殊要求
- Manim 必须用 `py -3.12 -m manim`（Python 3.14 不兼容）
- 素材版权自查：使用外部素材前确认授权
- 视频项目不进 git（文件太大），用目录结构管理版本
- 每个步骤完成后主动告知用户进度，关键节点等待用户确认
