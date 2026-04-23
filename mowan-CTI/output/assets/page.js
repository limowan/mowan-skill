(function () {
  const data = window.CTI_PERSONALITIES || {};

  /* ============ 主题切换 ============ */
  function initTheme() {
    const saved = localStorage.getItem("cti-theme");
    if (saved) {
      document.documentElement.setAttribute("data-theme", saved);
    }
  }

  function createThemeToggle() {
    const btn = document.createElement("button");
    btn.className = "theme-toggle";
    btn.setAttribute("aria-label", "切换主题");
    function updateIcon() {
      const isLight = document.documentElement.getAttribute("data-theme") === "light";
      btn.innerHTML = isLight
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
    }
    updateIcon();
    btn.addEventListener("click", function () {
      const current = document.documentElement.getAttribute("data-theme");
      const next = current === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("cti-theme", next);
      updateIcon();
    });
    document.body.appendChild(btn);
  }

  initTheme();

  function applyTheme(p) {
    const r = document.documentElement;
    r.style.setProperty("--page-accent", p.palette.accent);
    r.style.setProperty("--page-accent-deep", p.palette.deep);
    r.style.setProperty("--page-accent-soft", p.palette.soft);
    r.style.setProperty("--page-accent-ink", p.palette.ink);
    r.style.setProperty("--glow", p.palette.accent + "26");
    r.style.setProperty("--deco-gradient", "linear-gradient(135deg, " + p.palette.accent + " 0%, " + p.palette.deep + " 100%)");
  }

  /* ============ 头像 helpers ============ */
  function avatarImg(p) {
    return `<div class="chat-avatar"><img src="${p.image}" alt="${p.name}" onerror="this.parentElement.innerHTML='<span>${p.name.charAt(0)}</span>'" /></div>`;
  }
  function otherAvatar() {
    return `<div class="chat-avatar chat-avatar-other"><span>友</span></div>`;
  }

  /* ============ 结果页 ============ */
  function renderPage(p) {
    applyTheme(p);
    document.title = `${p.code} · ${p.name} | CTI 人格侧写`;

    var hasResult = !!p.matchPercent;

    /* 匹配度徽章 */
    var matchHtml = "";
    if (hasResult) {
      var hitCount = 0;
      var totalDims = 0;
      if (p.dimensions) {
        totalDims = p.dimensions.length;
        p.dimensions.forEach(function (d) { if (d.score >= 3) hitCount++; });
      }
      var confLabel = p.confidence === "high" ? "高置信" : p.confidence === "medium" ? "中置信" : "低置信";
      matchHtml = `
        <div class="match-badge">
          <div class="match-percent">${p.matchPercent}<span class="match-percent-sign">%</span></div>
          <div class="match-meta">
            <span class="match-meta-label">匹配度</span>
            <span class="match-meta-detail">精准命中 ${hitCount}/${totalDims} 维度</span>
            <span class="match-confidence"><span class="match-confidence-dot"></span>${confLabel}</span>
          </div>
        </div>
      `;
    }

    /* 维度评分卡片 */
    var dimensionHtml = "";
    if (hasResult && p.dimensions && p.dimensions.length) {
      var cardsHtml = p.dimensions.map(function (d, i) {
        var pct = Math.round((d.score / 5) * 100);
        return `
          <div class="dim-card" style="animation-delay:${(0.1 + i * 0.06)}s">
            <div class="dim-card-header">
              <div>
                <span class="dim-card-id">D${i + 1}</span>
                <span class="dim-card-name">${d.name}</span>
              </div>
              <div class="dim-card-score">
                <span class="dim-card-level">${d.level}</span>
                <span class="dim-card-value">${d.score}分</span>
              </div>
            </div>
            <div class="dim-card-bar"><div class="dim-card-bar-fill" style="width:${pct}%"></div></div>
            <div class="dim-card-desc">${d.desc}</div>
          </div>
        `;
      }).join("");

      dimensionHtml = `
        <div class="content-card dimension-section">
          <h2>评判维度</h2>
          <div class="dimension-grid">${cardsHtml}</div>
        </div>
      `;
    }

    /* 命中理由 */
    var hitReasonsHtml = "";
    if (hasResult && p.hitReasons && p.hitReasons.length) {
      var liHtml = p.hitReasons.map(function (r) { return "<li>" + r + "</li>"; }).join("");
      hitReasonsHtml = `
        <div class="hit-reasons">
          <div class="hit-reasons-title">命中理由</div>
          <ol>${liHtml}</ol>
        </div>
      `;
    }

    var quotesHtml = p.quotes
      .map(function (q, i) {
        var isRight = i % 2 === 1;
        var side = isRight ? "chat-right" : "chat-left";
        var av = isRight ? avatarImg(p) : otherAvatar();
        return `<div class="chat-row ${side}">${av}<div class="chat-bubble">${q}</div></div>`;
      })
      .join("");

    var html = `
      <div id="resultApp">
        <div class="nav-bar">
          <span class="nav-badge">CTI PROFILE</span>
        </div>

        <div class="page-body">
          <div class="profile-hero" id="profileHero">
            <div class="profile-hero-image-wrap" id="heroImageWrap">
              <img src="${p.image}" alt="${p.name}" onerror="this.parentElement.outerHTML='<div class=\\'profile-hero-fallback\\'><span>${p.code}</span></div>'" onload="document.getElementById('profileHero').classList.add('has-image')" />
            </div>
            <div class="profile-hero-info">
              <div class="profile-code">${p.code}</div>
              <h1 class="profile-name">${p.name}</h1>
              <p class="profile-subtitle">${p.subtitle}</p>
              ${matchHtml}
              <div class="profile-tag">${p.oneLiner}</div>
            </div>
          </div>

          <div class="result-content">
            ${dimensionHtml}

            <div class="content-card">
              <h2>人格解析</h2>
              <div class="intro-text">${p.intro}</div>
              ${hitReasonsHtml}
            </div>

            <div class="content-card">
              <h2>典型聊天记录</h2>
              <div class="wechat-chat">${quotesHtml}</div>
            </div>

            <div class="content-card">
              <h2>损友点评</h2>
              <div class="comment-card"><p>${p.comment}</p></div>
            </div>
          </div>

          <div class="page-footer">
            <div class="footer-badge">GENERATED BY CTI AI</div>
          </div>
        </div>
      </div>
    `;

    var shell = document.querySelector(".shell");
    if (shell) shell.outerHTML = html;

    /* 入场动画 delay */
    document.querySelectorAll(".content-card").forEach(function (el, i) {
      el.style.animationDelay = (0.15 + i * 0.12) + "s";
    });
    document.querySelectorAll(".chat-row").forEach(function (el, i) {
      el.style.animationDelay = (0.4 + i * 0.08) + "s";
    });

    /* 维度进度条动画：延迟触发 */
    setTimeout(function () {
      document.querySelectorAll(".dim-card-bar-fill").forEach(function (el) {
        el.style.width = el.style.width; /* force reflow for transition */
      });
    }, 300);
  }

  /* ============ 总览页 ============ */
  function renderIndex() {
    document.title = "CTI 聊天人格侧写 · 12类图鉴";
    const list = Object.values(data);

    const cardsHtml = list
      .map(function (p) {
        return `
        <a href="./${p.slug}.html" class="personality-card" style="--card-accent:${p.palette.accent}">
          <div class="card-avatar">
            <img src="${p.image}" alt="${p.name}" onerror="this.style.display='none'" />
          </div>
          <div class="card-info">
            <div class="card-name-row">
              <span class="card-name">${p.name}</span>
              <span class="card-code">${p.code}</span>
            </div>
            <div class="card-line">${p.oneLiner}</div>
          </div>
        </a>
      `;
      })
      .join("");

    const html = `
      <div id="indexApp">
        <div class="index-header">
          <div class="index-logo">CTI</div>
          <h1 class="index-title">聊天人格侧写</h1>
          <p class="index-desc">不是你说自己是谁，而是你留下的对话痕迹暴露了你是谁。</p>
        </div>
        <div class="index-grid">${cardsHtml}</div>
        <div class="page-footer">
          <div class="footer-badge">CONVERSATION TRACE INDICATOR</div>
        </div>
      </div>
    `;

    const shell = document.querySelector(".shell");
    if (shell) shell.outerHTML = html;

    /* 总览卡片入场动画 delay */
    document.querySelectorAll(".personality-card").forEach(function (el, i) {
      el.style.animationDelay = (0.05 + i * 0.06) + "s";
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    createThemeToggle();
    if (window.CTI_PAGE_KEY) {
      var p = data[window.CTI_PAGE_KEY];
      if (p) renderPage(p);
    } else {
      renderIndex();
    }
  });
})();
