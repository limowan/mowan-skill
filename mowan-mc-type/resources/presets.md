# 风格预设提示词库

本文件包含 6 种风格预设的完整字段，使用时需将对应预设的所有字段组装为风格提示词。

## 组装模板

对于每个预设，按以下模板拼装为风格提示词：

```
风格名称：{name}
整体氛围：{atmosphere}
适用内容：{suitableFor}
配色方向：{palette}
排版调性：{typographyTone}
当前正文基线字号：16px。
当前标题指定字号：H1 28px；H2 20px；H3 17px。
重要说明：本次生成必须严格使用这一套字号体系。正文、H1、H2、H3 不允许自行改成其他字号。相同层级的元素字号必须全文统一，不允许同一篇文章里出现同层级字号不一致的情况。
标题处理：{headingStrategy}
段落节奏：{paragraphRhythm}
强调方式：{emphasisStrategy}
引用处理：{quoteStrategy}
分隔与转场：{dividerStrategy}
列表呈现：{listStrategy}
结尾方式：{endingStrategy}
可用块型：{blockVocabulary 各项用 ；拼接}
排版纪律：{compositionRules 各项用 ；拼接}
避免倾向：{antiPatterns 各项用 ；拼接}
```

---

## 1. 极简理性（rational）

- **name**：极简理性
- **description**：理性克制的知识型排版，信息优先，留白有序。
- **hint**：适合知识拆解、教程、方法论类文章。
- **atmosphere**：理性克制、信息优先、安静专业。
- **suitableFor**：知识拆解、教程指南、经验方法论、分析解读。
- **palette**：以黑白灰为基底，搭配一个低饱和度的冷色调作为点缀强调色，整体色相不超过 3 个。
- **typographyTone**：无衬线体，字重保持克制，标题与正文层级清晰但不张扬。
- **headingStrategy**：标题保持清晰的层级关系，章节分区明确，不需要花哨的装饰性标题块。
- **paragraphRhythm**：段距均匀稳定，阅读节奏平稳，减少情绪化的跳跃。
- **emphasisStrategy**：重点段落少量强调即可，优先用浅底色或细边线表示，不要堆叠卡片。
- **quoteStrategy**：引用块保持简洁，用单层浅背景或左边线即可。
- **dividerStrategy**：分隔线简洁，用普通 hr 即可。
- **listStrategy**：列表要整齐、规则、以信息传达为导向。
- **endingStrategy**：结尾平稳收束，不做强视觉封板。
- **compatibilityNotes**：保持单层结构、低装饰、高保真，确保公众号粘贴稳定。
- **blockVocabulary**：
  - chapter-divider：标题前后留足呼吸空间的章节头，用细线或细边线建立秩序
  - quiet-emphasis：浅底或细边框的低调重点块
  - plain-quote：克制的引用块，不要大面积视觉打断
  - utility-list：规则清晰的单列信息列表
- **compositionRules**：
  - 整篇最多 3-4 种块型，避免每段都长得不一样
  - 标题样式最多 2 种变体
  - 强调块数量少而精准
  - 主要通过留白、字号差异和边线来建立层次
- **antiPatterns**：
  - 不要全篇堆灰底块和左边线
  - 不要出现网页卡片感或广告感
  - 不要让列表看起来像 PPT
  - 不要靠堆砌粗体来制造假重点

---

## 2. 温暖故事感（warm-story）

- **name**：温暖故事感
- **description**：柔和温暖的叙事型排版，有陪伴感和情绪节奏。
- **hint**：适合个人故事、成长复盘、情感表达类文章。
- **atmosphere**：温暖亲切、有陪伴感、叙事化节奏。
- **suitableFor**：成长复盘、故事分享、价值观表达、经验感悟。
- **palette**：奶油白、暖米色、陶土棕、蜂蜜金色调，允许少量温暖橙棕做强调。
- **typographyTone**：字形亲和柔软，节奏舒展，重点依靠呼吸感和暖色块而非强对比。
- **headingStrategy**：标题保留层级但转场更柔和，不要过于生硬的结构线。
- **paragraphRhythm**：节奏舒展，情绪段落允许更明显的留白停顿。
- **emphasisStrategy**：用浅暖底色做柔和的强调块，圆角可以有但不要过重。
- **quoteStrategy**：引用块做成陪伴式提示，强调阅读停顿和情绪过渡。
- **dividerStrategy**：分隔线尽量轻，起换气作用即可。
- **listStrategy**：列表自然融入正文语气，不要太强的表格感。
- **endingStrategy**：结尾柔和收束，可以略微抬高情绪。
- **compatibilityNotes**：避免网页卡片感，用浅背景和留白替代阴影。
- **blockVocabulary**：
  - soft-chapter：柔和的章节头，靠留白和暖色细边线过渡
  - companion-note：浅暖底陪伴式重点块，用于价值判断和感受表达
  - story-pause：较轻的引用停顿块，承接情绪
  - gentle-closing：轻抬情绪的结尾落点
- **compositionRules**：
  - 视觉重点要少，不要把每个感受句都做成卡片
  - 暖色只做提气用，不要大面积铺满
  - 留白服务叙事节奏，不能稀释信息密度
  - 同一类暖底块不要连续出现超过 2 次
- **antiPatterns**：
  - 不要做成甜品店海报或鸡汤卡片墙
  - 不要大面积深色底配白字
  - 不要用过于童趣的图形化块面
  - 不要让列表脱离正文语气

---

## 3. 商务专业（business-pro）

- **name**：商务专业
- **description**：正式稳重的专业排版，结构感强，信息密度高。
- **hint**：适合商业分析、行业报告、方案汇报类文章。
- **atmosphere**：专业可信、逻辑清晰、稳重理性。
- **suitableFor**：商业分析、行业观察、方案总结、策略建议。
- **palette**：石墨黑、雾灰、冷白为底，搭配一个商务蓝或墨绿作为主强调色。
- **typographyTone**：理性有报告感，信息效率高，标题像章节摘要，正文像专业评论。
- **headingStrategy**：标题要像报告章节一样，层级清楚、逻辑感强。
- **paragraphRhythm**：正文可以更紧凑，但仍需保持公众号的可读性。
- **emphasisStrategy**：重点段适合做边框型信息块或摘要块，视觉上保持正式感。
- **quoteStrategy**：引用块做成报告注释式的强调，但不要太像 PPT 卡片。
- **dividerStrategy**：分隔线干净利落，用于强调章节推进。
- **listStrategy**：列表像条款要点，适合结论式表达。
- **endingStrategy**：结尾有结论感和判断力，不要抒情化收束。
- **compatibilityNotes**：避免多栏和网页卡片，用边框和标题节奏建立专业感。
- **blockVocabulary**：
  - report-heading：像报告章节的标题块，强调结构而非情绪
  - summary-box：边框型摘要块，用于结论或判断句
  - annotation-quote：注释式引用块，适合定义和补充说明
  - decision-list：条款式的清晰行动建议列表
- **compositionRules**：
  - 整篇保持稳定基线，不要忽大忽小
  - 强调块优先用边框和浅灰底，不要显得像营销海报
  - 列表和表格是信息工具不是装饰组件
  - 结尾要形成判断闭环
- **antiPatterns**：
  - 不要使用夸张大色块或情绪化配色
  - 不要做成 SaaS 仪表盘或 PPT 封面
  - 不要堆叠过多圆角卡片
  - 不要让重点块和正文反差过强

---

## 4. 编辑长文风（magazine）

- **name**：编辑长文风
- **description**：像杂志社论的编辑感排版，强化章节节奏和重点提炼。
- **hint**：适合长文章、复盘文章、故事与分析混合型内容。
- **atmosphere**：有编辑感、节奏感、章节推进力。
- **suitableFor**：长文输出、观点文章、复盘总结、人物故事与分析的混合内容。
- **palette**：纸白、近黑为基底，搭配一个编辑蓝或暗橘等主强调色，加一个细微的点缀色。
- **typographyTone**：像现代杂志社论式的正文排版，标题像编辑标题，重点句像被主编标注出来。
- **headingStrategy**：标题层级分明，章节之间需要有明显的转场感。
- **paragraphRhythm**：正文应有快慢交替，普通段落与重点段、摘录段交错出现。
- **emphasisStrategy**：核心观点做成主编摘录式的强调块，数量少但存在感强。
- **quoteStrategy**：引用块做成杂志式停顿块，用边框或浅底帮助提速阅读。
- **dividerStrategy**：用干净的 hr 拉开篇章，不做装饰性分隔。
- **listStrategy**：列表做成编辑式条目区，保持单列阅读。
- **endingStrategy**：结尾让收束句突出，形成落点。
- **compatibilityNotes**：重点是编辑感而非网页感，避免阴影和复杂嵌套。
- **blockVocabulary**：
  - editor-heading：有转场感的章节头
  - pause-quote：用于转折句或反差句的短停顿块
  - editor-pullquote：主编摘录式的核心论断重点块，全文不超过 2-3 个
  - utility-panel：给建议和步骤用的利落信息区
  - closing-mark：结尾落点块，简洁有收束感
- **compositionRules**：
  - 整篇最多 4 种块型，标题最多 2 种变体
  - 不同内容角色必须有差异处理
  - 同一种强调块不要连续出现超过 2 次
  - 颜色像杂志栏目系统，纯色、克制、少而准
- **antiPatterns**：
  - 不要整篇只有黑白灰加左边线标题
  - 不要把所有重点句都做成同一种灰底块
  - 不要出现网页卡片或海报式大字感
  - 不要让结尾和中间重点块长得一模一样

---

## 5. 视觉杂志大片（magazine-designer）

- **name**：视觉杂志大片
- **description**：高完成度的杂志感排版，有主题色系统、彩色关键词、丰富的视觉层次。
- **hint**：适合深度特稿、人物稿、热点深度复盘、需要强视觉呈现的内容。
- **atmosphere**：活泼高级、丰富多彩但不杂乱、有强视觉秩序和编辑审美感。
- **suitableFor**：深度特稿、人物稿、专题稿、需要明显页面感和章节仪式感的内容。
- **palette**：建立完整的主题色系统（主色、辅助色、浅色高亮背景、深色高亮文字）。关键词和重点句使用彩色强调，不能全篇只有黑色加粗。
- **typographyTone**：像经过版式设计的杂志内页，标题有仪式感，关键词醒目但不破坏阅读节奏。
- **headingStrategy**：每个层级标题的视觉样式必须不同。一级章节用彩色背景条或渐变色块；二级标题用彩色下划线衬底或胶囊样式；三级标题用左侧彩色竖条或彩色加粗。绝对不能所有层级都用同一种左边线。
- **paragraphRhythm**：段落节奏有明显快慢变化。关键词使用主题色彩色加粗或彩色下划线。每段正文最多 2-3 处彩色关键词，不能句句高亮。
- **emphasisStrategy**：多种强调手法混合使用——彩色加粗、彩色下划线、胶囊标签、浅色底高亮条，交替使用形成丰富层次。
- **quoteStrategy**：引用块像精修过的杂志引言区，使用主题色左边框加浅色渐变背景。
- **dividerStrategy**：章节间用带中心装饰的分隔线或纯留白转场，不要用普通无装饰的 hr。
- **listStrategy**：列表使用带主题色编号徽章的条目区，有模块化的视觉感。
- **endingStrategy**：结尾形成杂志式落版感，可用浅色收束区或安静留白，避免大块深色高亮。
- **compatibilityNotes**：允许渐变背景和装饰边框，但避免 fixed、grid、多栏拼贴和外链资源。所有装饰都用内联 style 实现。
- **blockVocabulary**：
  - magazine-heading：杂志式章节头，使用彩色背景条或渐变色块
  - colored-subtitle：彩色衬底的二级标题，用渐变下划线效果或胶囊样式
  - theme-quote：带主题色边框和浅色渐变背景的引言区
  - keyword-highlight：关键词彩色强调，彩色加粗、彩色下划线、胶囊标签三种交替使用
  - number-list：带主题色数字徽章的条目区
  - decorated-divider：带中心装饰小图标的分隔线
- **compositionRules**：
  - 先建立主题色系统，全篇所有彩色元素都从这个系统取色
  - 关键词必须使用彩色强调，绝对不能全篇只有黑色加粗
  - 每个标题层级必须有明显不同的视觉样式
  - 强视觉块型最多 5 种，像一本杂志的统一设计语言
  - 彩色强调密度适中，每段最多 2-3 处
- **antiPatterns**：
  - 绝对不能退化成普通公众号模板（左边线+灰底块+普通 hr+纯黑加粗）
  - 不能所有标题都用同一种样式
  - 不能全篇只有黑色加粗
  - 不要做成 PPT 或海报
  - 不要让颜色失控，所有彩色元素必须来自主题色系统

---

## 6. 新媒体高亮风（pop-notes）

- **name**：新媒体高亮风
- **description**：爆款公众号常用的高亮式排版，重点词醒目，模块标题带关键词副标签。
- **hint**：适合大众传播、观点输出、热点拆解、知识分享。
- **atmosphere**：醒目易读、传播感强、节奏明快。
- **suitableFor**：热点解读、观点输出、知识传播、大众向长文。
- **palette**：白底为主，搭配一到两个高亮色（如薄荷绿、天蓝、桃橙），使用浅底版本。
- **typographyTone**：以传播效率为优先，重点像被荧光笔划过，但整体保持干净。
- **headingStrategy**：章节标题采用左侧竖杠加内容的堆叠布局。容器内部分三行：第一行是大数字编号（如 01），第二行是中文大标题，第三行是关键词副标签。竖杠效果使用 border-left 实现。
- **paragraphRhythm**：正文保持普通阅读节奏，关键段落可通过加粗小标题做引言。
- **emphasisStrategy**：允许使用高亮底纹、整块浅底和关键词色块。
- **quoteStrategy**：引用块做成传播感较强的金句条，但不宜过于夸张。
- **dividerStrategy**：分隔较弱，主要靠高亮小标题和重点块完成节奏切换。
- **listStrategy**：列表做成浅底圆角条目，适合经验点和建议点。
- **endingStrategy**：结尾形成便于记忆和转发的落点，避免大块深色高亮。
- **compatibilityNotes**：高亮感来自浅色背景和边框。章节标题的竖杠用 border-left 实现（不要用 td 背景色做竖杠，确保公众号兼容）。所有 table 必须设 border-collapse:collapse，所有 td 设 border:none。
- **blockVocabulary**：
  - numbered-heading：左侧主题色竖杠加右侧堆叠内容的章节标题（大编号+中文标题+关键词副标签）
  - highlight-heading：高亮底条或描边框的辅助标题
  - keyword-marker：关键词短高亮，像荧光笔划过
  - quote-strip：传播感金句条
  - note-chip-list：浅底圆角条目列表
  - closing-highlight：高亮收束句
- **compositionRules**：
  - 高亮是重点引导，不能变成全文背景色
  - 同一种高亮颜色贯穿全文
  - 章节标题竖杠用 border-left 实现
  - 正文和非高亮区域保持纯白底，需要强调时只用主题色极浅版本
- **antiPatterns**：
  - 不要像中学生手账本
  - 不要所有句子都加底色
  - 不要用 table td 背景色做竖杠
  - 关键词副标签不能省略
  - 正文段落不要使用灰色背景，非白色背景必须是主题色的极浅版本
