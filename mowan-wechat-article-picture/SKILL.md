---
name: mowan-wechat-article-picture
description: |
  公众号文章配图总控 Skill。用于给 Markdown 公众号草稿生成封面图和正文配图，按配置识别公众号、整理提示词和图片产物，并回填到文章中。
  使用场景：
  - "给这篇公众号文章做封面和配图"
  - "调用公众号配图流程"
  - "给公众号文章生成封面图"
  - "把配图插入公众号文章"
---

# 公众号文章配图总控

本 Skill 负责调度整套流程：读取配置、识别公众号、检查目录、生成封面、规划正文配图、调用生图能力、整理产物、回填 Markdown。

它不替代 `baoyu-article-illustrator`。正文配图继续复用 baoyu 的内容分析、风格候选和插图位置判断；在 Codex 环境中，最终生图默认使用 Codex 内置 `image_gen` 直出 PNG。

## ⚠️ 执行优先级

本 Skill 规则优先级高于 memory、旧经验、通用图片生成习惯。冲突时以本 Skill 为准。
Codex 环境下生图**只能用内置 `image_gen`**，禁止 Pillow/PIL/SVG/cairosvg/ImageMagick/matplotlib/本地脚本等任何替代方式。
本地命令只允许：建目录、复制生成图片、保存提示词、回填 Markdown、检查路径。
每次生图前必须对用户明示实际使用的生图方式。

## 配置优先

运行前必须先读取当前 Skill 目录下的 `config.json`。

- 如果 `config.json` 不存在，读取 `config.example.json`，让用户按示例提供真实路径。
- `vaultRoot` 是 Obsidian Vault 根目录，不是图片输出目录。
- 每个公众号的文章识别、头像、关注卡片和图片输出目录都从 `accounts[]` 读取。
- 不要在流程里写死某个公众号名称、路径、头像或关注卡片规则。

配置字段说明见 `config.example.json`。

## 首次使用配置向导

如果 `config.json` 不存在、字段不完整，或关键路径检测失败，必须先进入配置向导，不要直接要求用户自己编辑 JSON。

配置向导规则：

- 优先使用宿主环境的 AskUserQuestion 工具逐项提问；如果当前环境没有 AskUserQuestion，就用普通对话逐项提问。
- 不要一次性抛出完整 JSON；要按步骤引导用户理解每个字段是干嘛的。
- 每次最多问 1-3 个短问题，用户回答后再继续下一步。
- 所有路径都允许用户给绝对路径；生成配置时统一写成 `/` 形式。
- 写入或更新 `config.json` 前，先给用户展示将要写入的关键信息并确认。

建议提问顺序：

1. 询问 Obsidian Vault 根目录，也就是整个知识库的根目录。
2. 询问要配置几个公众号，以及每个公众号名称。
3. 询问每个公众号文章路径里稳定出现的识别关键词，作为 `pathMatchers`。
4. 询问每个公众号图片产物要放在哪里，作为 `outputRoot`。
5. 询问每个公众号封面是否需要头像；需要时再问头像路径。
6. 询问每个公众号文末是否需要关注卡片；需要时再问关注卡片路径。
7. 询问正文配图右下角是否展示公众号名称，默认关闭。
8. 检查 `requiredSkills[]` 中的依赖 Skill 是否存在。
9. 检查当前环境可用的生图方式：Codex 默认内置 `image_gen`；其它环境优先使用 `imageGenerationSkills[]`。

依赖检查：

- 正文配图分析依赖 `baoyu-article-illustrator`。
- 如果本机没有该 Skill，提示用户安装：`https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-article-illustrator/SKILL.md`。
- 依赖没装好时，不要跳过正文配图风格候选；可以只生成封面，或等用户装好后继续正文配图。

## 使用前先做

1. 读取用户给的文章路径。
2. 读取 `config.json`。
3. 如果缺少 `config.json` 或配置不完整，先执行“首次使用配置向导”。
4. 用 `config.accounts[].pathMatchers` 匹配文章路径，识别公众号。
5. 输出确认句，例如：`识别到公众号：<accountName>，文章类型：<短篇/长文/未知>`。
6. 如果无法确定公众号，或多个账号都匹配，先问用户确认，不要猜。
7. 检查 `requiredSkills[]` 依赖是否存在；缺失时引导安装。
8. 检查运行环境：
   - Codex：默认用内置 `image_gen`。
   - Claude Code 或其它环境：先检查 `config.imageGenerationSkills[]` 中配置的生图 Skill 路径。
   - 如果配置的生图 Skill 可用，调用它并告诉用户实际使用的 Skill 名称。
   - 如果配置的生图 Skill 不可用，检索当前环境中其它可用于生图的 Skill/API，并让用户确认后再使用。
9. 检查配置中的头像、关注卡片和输出目录；缺失时让用户提供路径或修正配置。

## 输出目录规范

每篇文章按配置生成目录，默认格式为：

```text
outputRoot/
└── {YYYY}年/
    └── {M}月/
        └── {YYYY-MM-DD}-{文章标题}/
            ├── 提示词-封面.md
            ├── 提示词-插图-主题.md
            ├── 封面.png
            └── 插图-主题.png
```

目录名中的文章标题必须做 Windows 文件名清洗，去掉或替换 `\ / : * ? " < > |` 等非法字符。

中间产物只保留提示词和最终 PNG。不额外保存正文配图计划文件，不保留临时脚本、SVG、未选中变体。

## 封面图流程

封面统一使用无日期模板，见 `references/cover-prompt-template.md`。

关键规则：

- 尺寸固定为 `900×383px`（比例 2.35:1）。
- 全中文排版。
- 自动从文章提炼主标题和 2-3 个关键词。
- 自动从 5 个配色库中选择。
- 自动在杂志排版和 IP 强化排版中选择。
- 是否使用封面头像只看 `needsCoverAvatar`。
- 头像路径只看 `coverAvatarPath`。

在 Codex 中，使用内置 `image_gen` 生成后，把默认输出复制到单篇文章目录下的 `封面.png`。Markdown 不能引用 Codex 默认生成目录。

## 正文配图流程

正文配图按 baoyu 的逻辑执行：

1. 分析文章结构和小标题。
2. 识别需要视觉辅助的位置。
3. 必须给出 3 个正文配图风格候选，让用户确认后才能继续生成。
4. 即使用户说”直接执行”，也不能跳过正文配图风格确认；”直接执行”只表示不再反复确认插图数量和插入位置。
5. 为每张图生成单独提示词，保存为 `提示词-插图-主题.md`。
6. 正文配图宽度固定为 900px，高度根据内容自适应。
7. Codex 环境用内置 `image_gen` 生成 PNG。
8. 图片放入单篇文章目录根部，文件名为 `插图-主题.png`。
9. 如果账号配置 `showAccountNameOnArticleImages=true`，每张正文配图右下角必须展示 `accountName`；默认 false，不展示。

正文配图永远不使用公众号头像；头像只服务封面。

## Markdown 回填规则

- 封面放在文章最开头。
- 正文配图放在对应段落的段首，方便在草稿箱查看。
- Markdown 图片引用必须指向 `outputRoot/{YYYY}年/{M}月/{YYYY-MM-DD}-{文章标题}/封面.png` 或 `outputRoot/{YYYY}年/{M}月/{YYYY-MM-DD}-{文章标题}/插图-主题.png`，并优先转换为相对文章文件的相对路径。
- 是否追加底部关注卡片只看 `appendFollowCard`。
- 关注卡片路径只看 `followCardPath`。
- 如果文章里已有同一关注卡片或同名图片引用，不重复追加。

## 安全规则

- 不包含 API Key、Token、auth.json、代理地址、私有 Base URL。
- 不提交 `config.json`。
- 不提交头像、关注卡片、文章原文、生成图片产物。
- 仓库只保留 `config.example.json`。
- README 和示例只使用占位路径。

## 参考

- 示例配置：`config.example.json`
- 封面提示词模板：`references/cover-prompt-template.md`
- 完整工作流：`references/workflow.md`
