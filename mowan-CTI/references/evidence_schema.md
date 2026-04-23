# CTI 人格证据包 Schema

> 统一中间层数据结构说明。无论材料来源是 A / B / C，最终都归一成这个结构。

---

## 设计原则

人格证据包是 CTI 的核心中间层。它解耦了"采集层"和"分类层"：

- A / B / C 三种模式只在采集层不同
- 分类引擎只吃这一个结构
- 结果包装器也只读分类引擎的输出

这样做的好处：分类逻辑只写一套，结果映射只写一套，后续加新来源只需要写新的 standardizer。

## 字段定义

```yaml
# === 元信息 ===
source_type: string
  # 材料来源模式
  # 枚举值：A / B / C
  # A = 外部大模型分析结果回填
  # B = 真实聊天记录导入
  # C = AI 平台聊天/记忆导出

material_summary: string
  # 材料概述，2-3 句话
  # 描述材料的来源、数量、时间跨度
  # 示例："来自 Gemini 的行为分析结果，覆盖了 9 个维度中的 7 个，缺少冲突处理和节奏习惯的信息。"

# === 行为特征维度 ===
speaking_style: string
  # 表达风格特征
  # 包括：消息长度、口头禅、句式习惯、标点偏好、emoji 使用
  # 示例："短句为主，高频使用省略号和'哈哈哈'，几乎不用感叹号，偶尔发语音代替打字"

decision_style: string
  # 决策方式
  # 主类型（选一个）：直觉型 / 分析型 / 拖延型 / 控制型 / 委托型
  # + 具体表现描述
  # 示例："拖延型 — 面对多个选项时倾向于说'回头再说'，经常在 deadline 前才做决定，但决定后很少反悔"

emotion_style: string
  # 情绪表达方式
  # 主类型（选一个）：外放型 / 压抑型 / 波动型 / 平稳型 / 深夜爆发型
  # + 具体表现描述
  # 示例："深夜爆发型 — 白天消息简短理性，凌晨后开始发长段感性内容，第二天假装没发过"

relationship_style: string
  # 关系姿态
  # 主类型（选一个）：主导型 / 配合型 / 回避型 / 依赖型 / 表面配合实际主导型
  # + 具体表现描述
  # 示例："表面配合实际主导型 — 嘴上说'你定就好'，但会用微妙方式引导对方选自己想要的选项"

pace_style: string
  # 节奏习惯
  # 主类型（选一个）：快速响应型 / 深夜活跃型 / 拖延型 / 碎片化型 / 集中爆发型
  # + 具体表现描述
  # 示例："碎片化型 — 全天零散发消息，没有固定活跃时段，经常一条消息分三条发"

revision_style: string
  # 自我修正习惯
  # 主类型（选一个）：反复修改型 / 一次定稿型 / 推翻重来型 / 微调完善型
  # + 具体表现描述
  # 示例："反复修改型 — 经常撤回消息重发，对已确认的方案反复推翻，口头禅是'等等我再想想'"

question_style: string
  # 提问风格
  # 主类型（选一个）：追问型 / 接受型 / 质疑型 / 沉默型
  # + 具体表现描述
  # 示例："追问型 — 每个回答都会触发新问题，平均追问 3-4 轮，不接受模糊答案"

conflict_style: string
  # 冲突处理方式
  # 主类型（选一个）：正面刚型 / 冷处理型 / 转移话题型 / 自我消化型
  # + 具体表现描述
  # 示例："冷处理型 — 不满时不直接表达，而是减少回复频率和字数，用句号代替感叹号"

# === 证据 ===
representative_quotes: list[string]
  # 3-5 句代表性原话
  # 每句后面用括号标注体现了什么特征
  # 示例：
  #   - "算了全部推翻，我重新说需求"（反复修改、推翻重来）
  #   - "你说的都对，但我就是感觉不太对"（直觉决策、不信逻辑）
  #   - "嗯嗯好的收到"（已读乱回、敷衍回复）

# === 风险评估 ===
risk_flags: list[string]
  # 置信度风险标记
  # 常见标记：
  #   - "材料不足"：总材料量太少，可能不准
  #   - "单一来源"：只有一种场景的材料（如只有工作群）
  #   - "原话不足"：代表性原话 < 3 句
  #   - "可能有表演成分"：材料来自正式场合，用户可能在"演"
  #   - "外部模型美化"：A 模式特有，外部模型可能讨好用户
  #   - "缺少维度"：某些行为维度完全没有信息
  #   - "人机 ≠ 人际"：C 模式特有，AI 对话行为不完全等于人际行为
```

## 维度与人格的关联矩阵

每个人格的核心判据依赖不同维度。以下是关键关联：

| 人格 | 核心依赖维度 | 辅助维度 |
|------|------------|---------|
| GGGG 改改改改 | revision_style | decision_style |
| 3:00 凌晨三点兽 | pace_style, emotion_style | speaking_style |
| BLBL 散装弹珠 | speaking_style | question_style |
| SUIB 随便侠 | decision_style, relationship_style | conflict_style |
| YDLH 已读乱回 | speaking_style | question_style, pace_style |
| 6+1 第六感战士 | decision_style | conflict_style |
| DSSQ 毒舌菩萨 | speaking_style, relationship_style | conflict_style |
| ZZZZ 人形咕咕机 | pace_style | revision_style |
| MFMF 嘴硬王 | emotion_style, speaking_style | conflict_style |
| KBKB 控制欲保安 | relationship_style, decision_style | question_style |
| QXJZ 情绪锦鲤 | emotion_style | pace_style |
| WDWS 十万个为什么 | question_style | decision_style |
