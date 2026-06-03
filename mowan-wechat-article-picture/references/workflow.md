# 工作流细则

## 1. 前置检查

1. 确认文章路径存在，并读取全文。
2. 读取 Skill 目录下的 `config.json`。
3. 如果缺少 `config.json` 或配置不完整，进入“首次配置向导”。
4. 用 `accounts[].pathMatchers` 匹配文章路径。
5. 输出识别结果给用户看：`识别到公众号：<accountName>，文章类型：<短篇/长文/未知>`。
6. 没有匹配或多个匹配时，必须询问用户确认公众号。
7. 检查依赖 Skill：
   - 必须检查 `requiredSkills[]`。
   - `baoyu-article-illustrator` 用于正文配图分析、插图位置识别和风格候选。
   - 如果缺失，提示用户安装：`https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-article-illustrator/SKILL.md`。
8. 检查账号资料：
   - `needsCoverAvatar=true` 时，必须存在 `coverAvatarPath`。
   - `appendFollowCard=true` 时，必须存在 `followCardPath`。
9. 检查输出目录 `outputRoot`；不存在时创建。
10. 检查生图环境：
   - Codex：使用内置 `image_gen`。
   - 其它环境：先检查 `config.imageGenerationSkills[]` 中配置的生图 Skill 路径。
   - 配置的生图 Skill 可用时，调用该 Skill，并说明当前实际使用方式。
   - 配置的生图 Skill 不可用时，检索当前环境其它可用于生图的 Skill/API，并让用户确认后使用。

## 1.1 首次配置向导

触发条件：

- `config.json` 不存在。
- `config.json` 缺少 `vaultRoot`、`accounts`、`outputRoot` 等关键字段。
- 配置里的关键路径不存在，且无法从文章路径稳定推断。

提问方式：

- 优先使用 AskUserQuestion 工具。
- 如果当前宿主没有 AskUserQuestion，就用普通对话逐项提问。
- 不要一次性要求用户填写整份 JSON。
- 每次最多问 1-3 个短问题，解释清楚这个字段的用途。

提问顺序：

1. `vaultRoot`：问用户 Obsidian Vault 根目录在哪里。
2. `accounts[].accountName`：问用户有哪些公众号。
3. `accounts[].pathMatchers`：问每个公众号文章路径里稳定出现的关键词。
4. `accounts[].outputRoot`：问每个公众号配图产物放在哪里。
5. `needsCoverAvatar` / `coverAvatarPath`：问封面是否需要头像，需要则问头像路径。
6. `appendFollowCard` / `followCardPath`：问文末是否需要关注卡片，需要则问关注卡片路径。
7. `showAccountNameOnArticleImages`：问正文配图右下角是否展示公众号名称，默认关闭。
8. `requiredSkills`：检查 `baoyu-article-illustrator` 是否存在；缺失则提示安装链接。
9. `imageGenerationSkills`：非 Codex 环境下，问用户可用的生图 Skill 路径。

写入配置前，要用自然语言复述即将写入的配置摘要，让用户确认。

## 2. 路径生成

`vaultRoot` 是 Obsidian Vault 根目录；`outputRoot` 是某个公众号的图片产物根目录。

默认目录：

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

日期使用生图当天日期。文章标题来自 Markdown 文件名，去掉扩展名，并清洗 Windows 文件名非法字符。

## 3. 内容规划

封面图需要提炼：

- 主标题：不超过 12 个字。
- 核心关键词：2-3 个。
- 文章情绪：用于选择配色库。
- 视觉隐喻：用于右侧概念视觉或 IP 人物。

正文配图复用 baoyu 的思路：

- 根据小标题或关键段落判断插图位置。
- 每个插图位置只保存最终提示词。
- 正文配图宽度固定为 900px，高度根据内容自适应。
- 必须给用户 3 个正文配图风格候选，并等待用户确认后再生成图片。
- 封面提示词必须严格遵循 `references/cover-prompt-template.md` 的排版方案，不得自行添加模板中未要求的文字元素。
- 用户要求直接执行时，也只代表不再反复确认插图位置和数量，不能跳过风格确认。
- 如果账号配置 `showAccountNameOnArticleImages=true`，正文配图提示词里必须要求右下角展示公众号名称；默认 false。

## 4. 生成与归档

每张图都要保存提示词：

- `提示词-封面.md`
- `提示词-插图-主题.md`

最终图片只保存 PNG：

- `封面.png`
- `插图-主题.png`

不要额外保存正文配图计划文件。Codex 内置生图默认保存到 Codex 目录，生成后必须复制到单篇文章目录，不能让 Markdown 引用 Codex 默认目录。

## 5. Markdown 回填

1. 封面插入文章第一行。
2. 正文配图插入对应段落段首。
3. 引用路径必须指向单篇文章目录里的最终 PNG：`outputRoot/{YYYY}年/{M}月/{YYYY-MM-DD}-{文章标题}/封面.png` 或 `outputRoot/{YYYY}年/{M}月/{YYYY-MM-DD}-{文章标题}/插图-主题.png`。
4. Markdown 中优先使用相对文章文件的相对路径，不引用 Codex 默认目录、临时目录或旧的中间目录。
5. `appendFollowCard=true` 时，在文章末尾追加关注卡片；已存在时不重复。
6. 回填后检查所有图片路径存在。

## 6. 失败处理

- 无法识别公众号：询问用户选择公众号。
- 缺少头像或关注卡片：让用户提供路径或修正配置。
- 生图工具不可用：说明当前环境限制，询问是否改用其它生图方式。
- 图片中文字明显错误：优先重生封面；正文配图尽量少放文字。
- 路径跨环境不匹配：重新确认 `vaultRoot`、账号资料路径和输出目录。
