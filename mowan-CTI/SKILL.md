name: mowan-cti
description: "墨玩 CTI 人格侧写 · 基于对话痕迹的人格分类 Skill | Conversation Trace Indicator — personality profiling from chat traces"
argument-hint: "[A/B/C]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **语言**: 本 Skill 使用简体中文交互。
>
> **执行根目录**: 所有 `Bash` 命令在本 `SKILL.md` 所在目录执行。`prompts/...`、`references/...`、`tools/...` 均为相对路径。

# CTI 人格侧写

**Conversation Trace Indicator** — 不是你说自己是谁，而是你留下的对话痕迹暴露了你是谁。

## 触发条件

当用户说以下任意内容时启动：
- `/cti`
- "帮我做人格测评"
- "测一下我的聊天人格"
- "CTI 测评"
- "人格侧写"

兼容宿主：Claude Code、OpenClaw、Hermes、Codex

---

## 工具使用规则

| 任务 | 使用工具 |
|------|---------|
| 读取 PDF / 图片 / MD / TXT | `Read` 工具 |
| 解析飞书消息 JSON 导出 | `Bash` → `python3 tools/feishu_parser.py` |
| 飞书全自动采集 | `Bash` → `python3 tools/feishu_auto_collector.py` |
| 钉钉全自动采集 | `Bash` → `python3 tools/dingtalk_auto_collector.py` |
| 解析邮件 .eml/.mbox | `Bash` → `python3 tools/email_parser.py` |
| 写入文件 | `Write` / `Edit` 工具 |

---

## 主流程：6 步

### Step 1：来源分流

首次进入时，展示以下引导：

```
欢迎来到 CTI 人格侧写。

这不是问卷测试。
我们会根据你的对话痕迹，判断你更像哪一类聊天人格。

请选择这次测评的材料来源：

  A. 复制提示词分析
     把我给你的提示词发给任意大模型（Gemini / GPT / Claude / 豆包），再把结果贴回来

  B. 聊天记录导入
     上传飞书、钉钉、微信等聊天记录

  C. AI 记忆导入
     上传 GPT、Claude、Gemini 等 AI 聊天 / 记忆内容
```

如果用户在触发时已带参数（如 `/cti A`），直接进入对应模式。

---

### Step 2：材料接收

根据用户选择的模式收集材料。

#### A 模式：复制提示词分析

1. 读取 `prompts/external_analysis_prompt.md`
2. 将提示词完整输出给用户，告诉他：
   - 复制这段提示词
   - 粘贴到任意大模型（Gemini / GPT / Claude / 豆包 / DeepSeek）
   - 让模型基于与你的聊天历史做分析
   - 把模型返回的分析结果贴回来
3. 等待用户贴回分析结果
4. 进入 Step 3

#### B 模式：聊天记录导入

展示支持的导入方式：

```
支持以下方式导入聊天记录：

  [1] 直接粘贴
      把聊天文本复制进来（最轻量）

  [2] 上传文件
      PDF / 图片截图 / 导出 JSON / 邮件 .eml

  [3] 飞书自动采集
      输入姓名，自动拉取消息记录

  [4] 钉钉自动采集
      输入姓名，自动拉取文档和消息

可以混用多种方式。
```

按用户选择执行：

**[1] 直接粘贴**：用户粘贴的内容直接作为原材料。

**[2] 上传文件**：
- PDF / 图片：`Read` 工具直接读取
- 飞书消息 JSON：
  ```bash
  python3 tools/feishu_parser.py --file {path} --target "{name}" --output /tmp/cti_feishu_out.txt
  ```
- 邮件 .eml / .mbox：
  ```bash
  python3 tools/email_parser.py --file {path} --target "{name}" --output /tmp/cti_email_out.txt
  ```
- MD / TXT：`Read` 工具直接读取

**[3] 飞书自动采集**：
```bash
python3 tools/feishu_auto_collector.py --setup  # 首次使用
python3 tools/feishu_auto_collector.py \
  --name "{name}" \
  --output-dir /tmp/cti_knowledge/{slug} \
  --msg-limit 500
```

**[4] 钉钉自动采集**：
```bash
python3 tools/dingtalk_auto_collector.py --setup  # 首次使用
python3 tools/dingtalk_auto_collector.py \
  --name "{name}" \
  --output-dir /tmp/cti_knowledge/{slug} \
  --msg-limit 500 \
  --show-browser
```

收集完成后，需要确认目标人物：
- 如果材料中有多人发言，询问用户要分析谁
- 提取目标人物的发言内容

#### C 模式：AI 记忆导入

展示支持的导入方式：

```
支持以下方式导入 AI 聊天记录：

  [1] 直接粘贴
      把 AI 对话内容复制进来

  [2] 上传导出文件
      GPT 导出的 JSON / Claude 导出 / Gemini 导出 / 其他平台导出

  [3] 粘贴 AI 记忆摘要
      如果平台有"记忆"功能，把记忆内容贴过来
```

C 模式的分析重点与 B 不同：
- B 看的是"人与人聊天时的社会人格"
- C 看的是"人与 AI 相处时暴露的认知人格"

C 模式特别关注：
- 提问习惯（追问型 / 接受型 / 质疑型）
- 任务拆解方式
- 情绪投射方式
- 依赖型 / 控制型 / 反复修改型特征
- 决策委托程度

---

### Step 3：材料标准化

不管来源是 A / B / C，都统一整理成一份**人格证据包**。

读取对应模式的标准化提示词：
- A 模式 → `prompts/material_standardizer_a.md`
- B 模式 → `prompts/material_standardizer_b.md`
- C 模式 → `prompts/material_standardizer_c.md`

输出统一的人格证据包结构：

```yaml
source_type: A / B / C
material_summary: 材料概述（2-3句话）
speaking_style: 表达风格特征
decision_style: 决策方式（直觉型/分析型/拖延型/控制型/委托型）
emotion_style: 情绪表达方式（外放/压抑/波动/平稳/深夜爆发）
relationship_style: 关系姿态（主导/配合/回避/依赖/表面配合实际主导）
pace_style: 节奏习惯（快速响应/深夜活跃/拖延/碎片化/集中爆发）
revision_style: 自我修正习惯（反复修改/一次定稿/推翻重来/微调完善）
question_style: 提问风格（追问型/接受型/质疑型/沉默型）
conflict_style: 冲突处理方式（正面刚/冷处理/转移话题/自我消化）
representative_quotes: 3-5句代表性原话
risk_flags: 置信度风险标记（材料不足/单一来源/可能有表演成分）
```

**关键原则**：
- A 模式：外部模型只是"材料生成器"，不是"最终裁判"。Skill 要做二次标准化，不直接采信外部模型的人格结论。
- B 模式：需要去噪（系统消息、表情包、转发垃圾），聚焦目标人物发言。
- C 模式：重点提取与 AI 交互中暴露的认知模式，而非对话内容本身。

---

### Step 4：人格打分

读取 `prompts/personality_classifier.md`，用人格证据包匹配 12 类人格。

参考 `references/personality_system.md` 中的 12 类人格定义。

输出：

```
主人格：{code} · {name}
命中理由：
1. ...
2. ...
3. ...

副人格：{code} · {name}
命中理由：
1. ...
2. ...

置信度：高 / 中 / 低
置信度说明：{为什么是这个置信度}
```

如果置信度为"低"，告知用户并建议补充材料。

---

### Step 5：结果包装

读取 `prompts/result_packager.md`。

从 `references/personality_system.md` 中取对应人格的完整资产：
- 人格代号、名称
- 副标题
- 毒舌简介
- 典型聊天语录
- 损友点评
- 配色方案
- 画像图路径

组装结果展示，包含：

**第一层：一句话结果**
```
你的 CTI 人格类型是：{code} · {name}
{oneLiner}
```

**第二层：主结果卡**
- 人格名 + 副标题
- 毒舌简介
- 配图

**第三层：分析依据**
- 从证据包中提取的命中理由
- 典型原话佐证

**第四层：损友点评**
- 对应人格的损友点评

---

### Step 6：结果输出

分两步：先在对话中展示结果，再生成可浏览的结果页。

#### 6a：对话内展示

直接在对话中展示完整结果，格式化输出（第一层到第四层内容）。

#### 6b：生成结果页 HTML

对话展示完成后，**自动进入结果页生成流程**：

**确定输出目录：**

```
结果页已准备好生成。

请指定输出目录（生成的文件会放在这里）：
  默认：{用户当前项目根目录}/cti-output

直接回车使用默认路径，或输入自定义路径。
```

> **重要**：输出目录必须在 Skill 目录之外。生成的结果页是用户的个人产物，不应污染 Skill 源码目录。

**生成文件：**

确定输出目录 `{OUTPUT_DIR}` 后，生成以下文件结构：

```
{OUTPUT_DIR}/
├── {slug}.html             # 用户的主人格结果页
└── assets/
    ├── page.css            # 从 Skill 的 output/assets/page.css 复制
    ├── page.js             # 从 Skill 的 output/assets/page.js 复制
    └── personality-data.js # 注入用户个人测评数据的版本
```

> **人格画像图不复制**：personality-data.js 中的 image 路径直接使用 Skill 目录的绝对路径（如 `file:///...mowan-CTI/image/KBKB · 控制欲保安.png`），避免重复拷贝大图文件。
> 
> **只生成单个结果页**：不生成总览页（index.html），只输出用户命中的主人格对应的 `{slug}.html`。页面直接展示结果，无返回总览按钮。

**personality-data.js 数据注入：**

从 Skill 的 `output/assets/personality-data.js` 读取基础 12 类人格数据，然后在用户命中的主人格条目中注入个人测评结果字段：

```javascript
// 在主人格的对象中追加以下字段：
matchPercent: {匹配百分比},
confidence: "{high|medium|low}",
hitReasons: ["{命中理由1}", "{命中理由2}", "{命中理由3}"],
dimensions: [
  { name: "{维度名}", level: "{S|A|B|C}", score: {1-5}, desc: "{描述}" },
  // ... 8 个维度
]
```

**各 HTML 文件结构：**

每个 HTML 文件结构与 `output/gggg.html` 一致：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CTI 人格侧写</title>
  <link rel="stylesheet" href="./assets/page.css" />
</head>
<body>
  <div class="shell"></div>
  <script>window.CTI_PAGE_KEY = "{CODE}";</script>
  <script src="./assets/personality-data.js"></script>
  <script src="./assets/page.js"></script>
</body>
</html>
```

- `{slug}.html`：设置对应的 `CTI_PAGE_KEY`，渲染单个人格结果页

**输出可点击链接：**

生成完成后，在对话中输出本地文件链接，用户可直接点击打开：

```
结果页已生成：

📄 你的人格结果页：file://{OUTPUT_DIR}/{slug}.html

在浏览器中打开即可查看完整结果。
```

#### 可分享文案

无论哪种输出方式，都额外提供一段可分享文案：

```
我的 CTI 测评结果：{code} · {name}
{oneLiner}

{一句吐槽版总结，适合发朋友圈/群聊}
```

---

## 12 类人格速查

| 代号 | 名字 | 核心特征 |
|------|------|---------|
| GGGG | 改改改改 | 反复修改、永远觉得差一点 |
| 3:00 | 凌晨三点兽 | 白天正常深夜发疯 |
| BLBL | 散装弹珠 | 思维跳跃、一条消息七件事 |
| SUIB | 随便侠 | 嘴上随便实际有标准答案 |
| YDLH | 已读乱回 | 精准忽略重点、回复延迟 |
| 6+1 | 第六感战士 | 靠直觉决策且经常对 |
| DSSQ | 毒舌菩萨 | 嘴上拆台手上帮忙 |
| ZZZZ | 人形咕咕机 | deadline 是用来突破的 |
| MFMF | 嘴硬王 | 明明在意嘴上说无所谓 |
| KBKB | 控制欲保安 | 聊天像开项目管理会 |
| QXJZ | 情绪锦鲤 | 情绪起伏比股票刺激 |
| WDWS | 我的我的 | 行走的十万个为什么 |

---

## 注意事项

1. **娱乐定位**：CTI 是娱乐向人格侧写，不是心理学诊断工具。结果展示时保持轻松吐槽风格。
2. **隐私保护**：不存储用户聊天记录原文，分析完成后不保留原始材料。
3. **多人格可能**：大多数人会同时命中 2-3 个人格特征，主人格 + 副人格的组合更准确。
4. **材料质量**：材料越多越准。单条消息或极短对话可能导致低置信度结果。
