---
name: mowan-mc-type
description: |
  墨成AI排版 —— 将 Markdown 文章转换为微信公众号精美排版的 HTML。
  支持 6 种风格预设（极简理性、温暖故事感、商务专业、编辑长文风、视觉杂志大片、新媒体高亮风），
  自动生成滑动卡片导航、引导关注卡片，输出可直接粘贴到公众号编辑器的内联样式 HTML。
  当用户说「排版」「公众号排版」「Markdown 转公众号」「帮我排版成公众号文章」
  「微信排版」「生成公众号 HTML」「mc-type」「墨成排版」时使用此 skill。
  也适用于：用户提供了一段 Markdown 内容并希望得到精美的公众号排版输出。
---

# 墨成AI排版 · 工作流编排

本文件是 Skill 的**流程编排器**。具体的提示词、规则和 HTML 结构模板存放在 `resources/` 文件夹中。

执行本 Skill 时，**必须先读取对应的资源文件**再开始生成。

---

## 资源文件索引

| 文件 | 内容 | 何时读取 |
|------|------|---------| 
| `resources/presets.md` | 6 种风格预设的完整提示词（每个预设 15+ 字段） | 用户选定风格后 |
| `resources/nav-cards.md` | 3 种卡片导航样式的提示词 | 卡片导航开启时 |
| `resources/follow-card.md` | 引导关注卡片的提示词 | 关注卡片开启时 |
| `resources/wechat-rules.md` | 公众号兼容性约束 + 系统提示词模板 + 输出规则 + 胶囊标签提示词 | **每次都必须读取** |

---

## 执行流程

### 第一步：读取输入

1. 用户提供 Markdown 文本来源：
   - 直接粘贴 Markdown 文本
   - 提供 `.md` 文件路径 → 读取文件内容
   - 提供 URL → 抓取内容转为 Markdown
2. 读取完毕后，确认 Markdown 内容长度和章节数量

### 第二步：分析文章类型并推荐风格

**必须主动推荐，不要让用户自己猜选哪个。**

先快速判断文章类型，然后从下表推荐 2-3 个最合适的风格：

| 文章类型 | 首选推荐 | 备选推荐 |
|---------|---------|---------| 
| 知识教程、方法论 | 极简理性 | 商务专业 |
| 个人故事、成长复盘 | 温暖故事感 | 编辑长文风 |
| 商业分析、行业报告 | 商务专业 | 极简理性 |
| 热点解读、观点输出 | 新媒体高亮风 | 编辑长文风 |
| 深度特稿、人物稿 | 视觉杂志大片 | 编辑长文风 |
| 案例拆解、经验总结 | 新媒体高亮风 | 商务专业 |

向用户展示推荐时，用简短文字说明每个风格的「一句话概括」和「为什么适合这篇文章」。

### 第三步：确认附加组件

向用户确认以下 4 个开关（告知默认值）：

| 组件 | 默认值 | 说明 |
|------|-------|------|
| 📋 卡片导航 | ✅ 开启，滑动卡片样式 | 文章顶部的章节目录区 |
| 🫶 引导关注卡片 | ✅ 开启 | 文末"点赞·在看·转发"互动区 |
| 💊 胶囊标签 | ❌ 关闭 | 段首【核心观点】【Step 1】等标签 |
| 📤 发布到草稿箱 | ❌ 关闭 | 排版完成后自动寻找可用的微信公众号发布类 Skill，将排版结果推送到公众号草稿箱 |

如果用户开启卡片导航，追问导航样式（默认滑动卡片）：
- 滑动卡片（默认）— 横向可滑动
- 仪表盘 — SaaS 风格网格
- 标题卡片 — 简洁纵向列表

如果用户开启引导关注卡片，可追问：
- 引导文案：默认"既然看到这里了，随手点赞、在看、转发三连吧"
- 致谢文案：默认不显示（用户可自定义，如"谢谢！"）

### 第四步：读取资源文件并组装提示词

**这是核心步骤。必须从资源文件中读取完整提示词，不能凭记忆笼统生成。**

1. **必读** `resources/wechat-rules.md`：
   - 提取「公众号兼容性约束」全文
   - 提取「系统提示词模板」并根据开关状态拼装豁免项/禁止项
   - 提取「输出规则」全文
   - 提取对应的「胶囊标签提示词」（开/关版本）

2. **必读** `resources/presets.md`：
   - 找到用户选定的风格预设
   - 按「组装模板」将预设的所有字段拼装为风格提示词

3. **按需读取** `resources/nav-cards.md`（卡片导航开启时）：
   - 找到用户选择的导航样式
   - 提取对应的完整提示词

4. **按需读取** `resources/follow-card.md`（引导关注卡片开启时）：
   - 提取完整提示词
   - 替换 {followCardLeadText} 和 {followCardFooterText}

### 第五步：Markdown 转 HTML

将用户提供的 Markdown 内容转换为基础 HTML。转换规则：

| Markdown 语法 | HTML 输出 |
|--------------|----------|
| `# 标题` | `<h1>` |
| `## 二级标题` | `<h2>` |
| `### 三级标题` | `<h3>` |
| `**加粗**` | `<strong>` |
| `*斜体*` | `<em>` |
| `> 引用` | `<blockquote>` |
| `- 列表` / `* 列表` | `<ul><li>` |
| `1. 有序列表` | `<ol><li>` |
| `` `行内代码` `` | `<code>` |
| ` ```代码块``` ` | `<pre><code>` |
| `---` | `<hr>` |
| `[链接](URL)` | `<a href="URL">` |
| `![图片](URL)` | `<img src="URL">` |
| `| 表格 |` | `<table>` |

### 第六步：生成排版 HTML

以「你自己就是那个排版 AI」的角色，按照组装好的提示词规则，将基础 HTML 转换为精美排版 HTML。

生成顺序：
1. 卡片导航区（如开启）→ 放在 HTML 最开头
2. 正文排版 → 按风格预设设计所有元素
3. 引导关注卡片（如开启）→ 放在 HTML 最末尾

基础排版参数：
- 正文字号：16px
- 行高：1.8
- 段间距：1.5em
- 字体栈：`"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`

### 第七步：封装输出文件（含一键复制逻辑）

⚠️ **关键原理**：公众号编辑器只接受**渲染后的富文本**，不接受 HTML 源代码。如果用户直接复制 HTML 代码粘贴到公众号，公众号会显示原始代码文字。正确做法是：在浏览器中渲染 HTML → 通过 JavaScript 将渲染内容以 `text/html` MIME 类型写入系统剪贴板 → 粘贴到公众号时就是富文本排版。

输出文件必须使用以下模板（自带一键复制按钮和剪贴板写入脚本）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>公众号排版预览 - 墨成AI排版</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #f0f2f5;
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      padding: 20px 20px 80px;
    }
    /* 顶部工具栏 */
    .mc-toolbar {
      position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
      background: #fff; border-bottom: 1px solid #e5e7eb;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .mc-toolbar-inner {
      max-width: 620px; margin: 0 auto;
      padding: 12px 20px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .mc-toolbar-title { font-size: 15px; color: #333; font-weight: 700; }
    .mc-copy-btn {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 22px; border: none; border-radius: 8px;
      background: linear-gradient(135deg, #10B981, #059669);
      color: #fff; font-size: 14px; font-weight: 600;
      cursor: pointer; transition: all 0.2s;
      box-shadow: 0 2px 8px rgba(16,185,129,0.3);
      white-space: nowrap;
    }
    .mc-copy-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(16,185,129,0.4); }
    .mc-copy-btn:active { transform: translateY(0); }
    .mc-copy-btn.copied {
      background: linear-gradient(135deg, #6366f1, #4f46e5);
      box-shadow: 0 2px 8px rgba(99,102,241,0.3);
    }
    /* 预览容器 */
    .mc-preview {
      max-width: 580px; margin: 68px auto 0;
      background: #fff; border-radius: 12px;
      padding: 30px 20px; box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    }
    /* 底部提示 */
    .mc-footer {
      max-width: 580px; margin: 0 auto;
      text-align: center; color: #999; font-size: 12px;
      padding: 16px 0;
    }
    /* 作者卡片 */
    .mc-author-card {
      max-width: 580px; margin: 20px auto 0;
      background: #fff; border-radius: 12px;
      padding: 28px 24px; box-shadow: 0 1px 6px rgba(0,0,0,0.08);
      text-align: left;
    }
    .mc-author-card h3 {
      font-size: 17px; font-weight: 700; color: #1a1a1a;
      margin: 0 0 16px 0;
    }
    .mc-author-desc {
      font-size: 14px; color: #555; line-height: 1.6;
      margin: 0 0 16px 0;
    }
    .mc-author-story {
      font-size: 13px; color: #666; line-height: 1.7;
      margin: 0 0 20px 0;
      padding: 14px 16px;
      background: #f9fafb; border-radius: 8px;
      border-left: 3px solid #10B981;
    }
    .mc-author-story a {
      color: #059669; text-decoration: none; font-weight: 500;
    }
    .mc-author-story a:hover { text-decoration: underline; }
    .mc-author-table {
      width: 100%; border-collapse: collapse;
      margin: 0 0 20px 0;
      border: 1px solid #e5e7eb;
    }
    .mc-author-table th, .mc-author-table td {
      padding: 10px 12px;
      border: 1px solid #e5e7eb;
      vertical-align: middle;
    }
    .mc-author-table td {
      font-size: 14px; color: #333;
    }
    .mc-author-table th {
      background: #f8fafc;
      font-size: 14px; color: #475569;
      text-align: left; font-weight: 600;
      border-bottom: 2px solid #e5e7eb;
    }
    .mc-author-table .mc-platform {
      width: 110px; white-space: nowrap; font-weight: 500;
    }
    .mc-author-table a {
      color: #059669; text-decoration: none; font-weight: 500;
    }
    .mc-author-table a:hover { text-decoration: underline; }
    .mc-author-qr {
      text-align: left; padding-top: 4px;
    }
    .mc-author-qr img {
      max-width: 320px; height: auto;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <!-- 顶部工具栏 -->
  <div class="mc-toolbar">
    <div class="mc-toolbar-inner">
      <span class="mc-toolbar-title">墨成AI排版</span>
      <button class="mc-copy-btn" id="copyBtn" onclick="copyForWechat()">
        📋 一键复制到公众号
      </button>
    </div>
  </div>

  <!-- 排版预览区 -->
  <div class="mc-preview" id="articleContent">
    <!-- ===== 排版 HTML 开始（此区域内容会被复制到剪贴板）===== -->

    {生成的排版 HTML 放在这里}

    <!-- ===== 排版 HTML 结束 ===== -->
  </div>

  <!-- 操作提示 -->
  <div class="mc-footer">
    点击上方「一键复制到公众号」按钮，然后在公众号编辑器中 Ctrl+V 粘贴即可
  </div>

  <!-- 作者卡片 -->
  <div class="mc-author-card">
    <h3>关于作者</h3>
    <p class="mc-author-desc">
      <strong>墨玩AI</strong> — 独立开发者，和你一起探索 AI 在生活中的有趣用法 🌱
    </p>
    <div class="mc-author-story">
      写完文章还要花半小时排版，这件事困扰了我很久。所以我做了这个工具——希望排版不再是负担，而是写作的最后一点小享受。<a href="https://mp.weixin.qq.com/s/lC98DDwDB3aqKj129lC-Hw" target="_blank">→ 读读这个故事</a>
    </div>
    <table class="mc-author-table">
      <thead>
        <tr>
          <th style="width:110px;">平台</th>
          <th>链接</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="mc-platform">📕 小红书</td>
        <td><a href="https://xhslink.com/m/3Ks23mHtPrL" target="_blank">墨玩AI</a></td>
      </tr>
      <tr>
        <td class="mc-platform">💬 公众号</td>
        <td>微信搜「墨玩AI」或扫码关注 ↓</td>
      </tr>
      </tbody>
    </table>
    <div class="mc-author-qr">
      <img src="https://raw.githubusercontent.com/limowan/mowan-mc-type/main/wechat_qrcode.jpg" alt="墨玩AI 公众号二维码">
    </div>
  </div>

  <script>
    /**
     * 一键复制到公众号的核心逻辑
     * 原理：将 #articleContent 内的渲染后 HTML 以 text/html MIME 类型写入系统剪贴板
     * 公众号编辑器会识别 text/html 格式并解析为富文本排版
     */
    async function copyForWechat() {
      const content = document.getElementById('articleContent');
      const btn = document.getElementById('copyBtn');
      if (!content) return;

      // 获取渲染后的 HTML 内容
      const html = content.innerHTML;
      // 同时提取纯文本作为 fallback
      const plain = content.innerText || content.textContent || '';

      try {
        // 方案一（首选）：使用 Clipboard API 写入 text/html
        if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {
          await navigator.clipboard.write([
            new ClipboardItem({
              'text/html': new Blob([html], { type: 'text/html' }),
              'text/plain': new Blob([plain], { type: 'text/plain' })
            })
          ]);
          showCopySuccess(btn);
          return;
        }

        // 方案二（兼容）：创建隐藏的 contentEditable 区域，选中后 execCommand copy
        if (copyViaSelection(html)) {
          showCopySuccess(btn);
          return;
        }

        // 方案三（降级）：只能复制纯文本
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(html);
          btn.textContent = '⚠️ 已复制（纯文本模式）';
          btn.classList.add('copied');
          setTimeout(() => { btn.innerHTML = '📋 一键复制到公众号'; btn.classList.remove('copied'); }, 3000);
          return;
        }

        alert('当前浏览器不支持自动复制，请手动选中内容后 Ctrl+C 复制');
      } catch (err) {
        // Clipboard API 可能因为权限被拒绝，降级到 Selection 方案
        if (copyViaSelection(html)) {
          showCopySuccess(btn);
          return;
        }
        alert('复制失败：' + err.message);
      }
    }

    /**
     * 通过 Selection + execCommand 实现富文本复制（兼容方案）
     * 创建一个屏幕外的 contentEditable 容器，注入 HTML 让浏览器渲染，
     * 然后选中所有内容执行 copy 命令，浏览器会自动将选中的富文本写入剪贴板。
     */
    function copyViaSelection(html) {
      if (!document.queryCommandSupported || !document.queryCommandSupported('copy')) {
        return false;
      }
      var host = document.createElement('div');
      host.contentEditable = 'true';
      host.setAttribute('aria-hidden', 'true');
      host.style.cssText = 'position:fixed;left:-99999px;top:0;opacity:0;pointer-events:none;white-space:normal;';
      host.innerHTML = html;
      document.body.appendChild(host);

      var selection = window.getSelection();
      var savedRanges = [];
      if (selection) {
        for (var i = 0; i < selection.rangeCount; i++) {
          savedRanges.push(selection.getRangeAt(i).cloneRange());
        }
      }

      var range = document.createRange();
      range.selectNodeContents(host);
      if (selection) {
        selection.removeAllRanges();
        selection.addRange(range);
      }

      var copied = false;
      try { copied = document.execCommand('copy'); } catch (e) { copied = false; }

      if (selection) {
        selection.removeAllRanges();
        savedRanges.forEach(function(r) { selection.addRange(r); });
      }
      document.body.removeChild(host);
      return copied;
    }

    function showCopySuccess(btn) {
      btn.innerHTML = '✅ 已复制！去公众号粘贴吧';
      btn.classList.add('copied');
      setTimeout(function() {
        btn.innerHTML = '📋 一键复制到公众号';
        btn.classList.remove('copied');
      }, 3000);
    }
  </script>
</body>
</html>
```

### 第八步：交付

1. 将 HTML 保存为文件（保存到用户工作区或与原 Markdown 文件同目录）
2. 告知用户操作步骤：
   > **使用方法（两步搞定）：**
   > 1. **用浏览器打开**这个 HTML 文件（双击即可）— 你会看到带排版效果的预览页面
   > 2. **点击页面顶部绿色的「📋 一键复制到公众号」按钮** — 然后到公众号后台编辑器 Ctrl+V 粘贴
   >
   > ⚠️ 不要直接复制 HTML 源码！必须用浏览器打开后点按钮复制，公众号才能正确识别排版。

3. **可选：推送到草稿箱**
   如果用户开启了「发布到草稿箱」开关，完成 HTML 生成后，自动在当前环境中寻找任何可用于"发布微信公众号文章"或"推送到微信草稿箱"的 Skill。找到后，将生成的排版 HTML 作为文章正文内容传入该 Skill，协助用户完成发布。如果未找到相关 Skill，告知用户："当前环境未安装微信发布类 Skill，已为您生成本地 HTML 文件，请手动复制粘贴到公众号后台。"

---

## 注意事项

- **零改字原则**：正文文字不能有任何增删改，只能改排版和样式
- **不能凭记忆生成**：每次执行都必须从 `resources/` 读取最新的提示词
- **风格要有辨识度**：不同风格之间的排版效果必须有明显差异，不能所有风格出来都差不多
- **公众号兼容优先**：所有视觉效果都以公众号编辑器能正常渲染为前提
- **必须使用完整输出模板**：自带一键复制按钮和剪贴板脚本，不能输出裸 HTML
