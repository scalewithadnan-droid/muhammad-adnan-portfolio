/* Adnan Afzal — site interactions. Vanilla JS + GSAP/ScrollTrigger (vendored). */
(function () {
  "use strict";

  var html = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasGSAP = typeof window.gsap !== "undefined";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Navigation ---------- */
  var nav = $(".nav");
  var progress = $(".nav__progress");
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (nav) {
      nav.classList.toggle("is-scrolled", y > 24);
      var goingDown = y > lastY;
      nav.classList.toggle("is-hidden", goingDown && y > 640 && !html.classList.contains("menu-open"));
    }
    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = "scaleX(" + (max > 0 ? Math.min(1, y / max) : 0) + ")";
    }
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var burger = $(".burger");
  var mmenu = $(".mmenu");
  function setMenu(open) {
    html.classList.toggle("menu-open", open);
    if (burger) {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    if (mmenu) {
      mmenu.setAttribute("aria-hidden", String(!open));
      if (open) { var first = $("a", mmenu); if (first) setTimeout(function () { first.focus(); }, 300); }
    }
  }
  if (burger) burger.addEventListener("click", function () { setMenu(!html.classList.contains("menu-open")); });
  if (mmenu) $$("a", mmenu).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && html.classList.contains("menu-open")) { setMenu(false); if (burger) burger.focus(); }
  });

  /* Active section highlighting (homepage) */
  var navLinks = $$('.nav__links a[href*="#"]');
  if (navLinks.length && "IntersectionObserver" in window) {
    var map = {};
    navLinks.forEach(function (a) {
      var id = a.getAttribute("href").split("#")[1];
      var sec = id && document.getElementById(id);
      if (sec) map[id] = a;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          navLinks.forEach(function (a) { a.removeAttribute("aria-current"); });
          map[en.target.id].setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ---------- Expertise card spotlight ---------- */
  $$(".xcard").forEach(function (card) {
    card.addEventListener("pointermove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- Filtering (case studies + blog) ---------- */
  function setupFilter(groupSel, itemSel) {
    $$(groupSel).forEach(function (group) {
      var scope = group.closest("[data-filter-scope]") || document;
      var items = $$(itemSel, scope);
      var buttons = $$("[data-filter]", group);
      buttons.forEach(function (btn) {
        var f = btn.getAttribute("data-filter");
        var count = f === "all" ? items.length : items.filter(function (it) { return (it.getAttribute("data-cats") || "").split(" ").indexOf(f) > -1; }).length;
        var c = $(".filter__count", btn); if (c) c.textContent = count;
        btn.addEventListener("click", function () {
          buttons.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
          btn.setAttribute("aria-pressed", "true");
          var shown = 0;
          items.forEach(function (it) {
            var match = f === "all" || (it.getAttribute("data-cats") || "").split(" ").indexOf(f) > -1;
            it.classList.toggle("is-hidden", !match);
            if (match) shown++;
          });
          var live = $("[data-filter-live]", scope);
          if (live) live.textContent = shown + (shown === 1 ? " project" : " projects") + " shown";
          if (hasGSAP && !reduce) {
            gsap.fromTo(items.filter(function (i) { return !i.classList.contains("is-hidden"); }),
              { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, stagger: 0.06, ease: "power3.out", clearProps: "transform" });
          }
          if (window.ScrollTrigger) ScrollTrigger.refresh();
        });
      });
    });
  }
  setupFilter(".filters", ".case, .bitem");

  /* ---------- Growth Operating System ---------- */
  var GOS = {
    acquisition: {
      n: "01", t: "Acquisition",
      p: "Buy and earn the right users, not just the cheapest installs. Campaign structure, bidding and creative are judged on downstream value — retention and revenue — so spend scales without diluting quality.",
      lever: "Campaign structure, bid strategy, creative testing, channel mix",
      signal: "CPI, install-to-D1 quality, cohort ROAS"
    },
    conversion: {
      n: "02", t: "Store Conversion",
      p: "The store page is the last step of every paid and organic journey. Icons, screenshots, video and metadata are tested so that every click you pay for has the best chance of becoming an install.",
      lever: "Keyword architecture, creative sets, localisation, store experiments",
      signal: "Page-view to install rate by source, keyword rank"
    },
    activation: {
      n: "03", t: "Activation",
      p: "The first session decides whether acquisition money was well spent. Onboarding, first-time user experience and early events are instrumented so drop-off is visible and fixable.",
      lever: "FTUE flow, tutorial pacing, early event tracking",
      signal: "Tutorial completion, first-session length, D0 events"
    },
    retention: {
      n: "04", t: "Retention",
      p: "Retention is the multiplier on every other stage. Cohorts are read by source, country and creative, and live-ops, push and remote-config tests are used to keep users coming back.",
      lever: "Live-ops cadence, push / messaging, remote config tests",
      signal: "D1 / D7 / D30 retention by cohort"
    },
    monetization: {
      n: "05", t: "Monetization",
      p: "Revenue is designed alongside the experience, not bolted on. Ad mediation, placements, frequency and IAP tiers are tested against retention so ARPDAU improves without breaking the product.",
      lever: "Mediation & bidding, placement tests, IAP pricing",
      signal: "ARPDAU, LTV curves, eCPM by network"
    },
    optimization: {
      n: "06", t: "Optimization",
      p: "Every stage feeds signal back into the next decision. Attribution, analytics and revenue data are connected into one decision-ready view so budgets move to what actually compounds.",
      lever: "Attribution, dashboards, cohort analysis, forecasting",
      signal: "Blended ROAS, payback period, LTV:CAC"
    }
  };
  var gosNodes = $$(".gos__node");
  var gosKeys = Object.keys(GOS);
  var panel = $(".gos__panel");
  var currentStage = gosNodes.length ? "acquisition" : null;
  function setStage(key) {
    var d = GOS[key]; if (!d || !panel || key === currentStage) return;
    currentStage = key;
    gosNodes.forEach(function (n) {
      var on = n.getAttribute("data-stage") === key;
      n.classList.toggle("is-active", on);
      n.setAttribute("aria-pressed", String(on));
    });
    var fill = function () {
      $(".gos__step", panel).textContent = "STAGE " + d.n + " / 06";
      $("h3", panel).textContent = d.t;
      $("p", panel).textContent = d.p;
      $("[data-lever]", panel).textContent = d.lever;
      $("[data-signal]", panel).textContent = d.signal;
    };
    if (hasGSAP && !reduce) {
      gsap.to(panel.children, { opacity: 0, y: 8, duration: 0.18, stagger: 0.02, onComplete: function () {
        fill(); gsap.to(panel.children, { opacity: 1, y: 0, duration: 0.4, stagger: 0.04, ease: "power3.out" });
      } });
    } else fill();
  }
  gosNodes.forEach(function (node) {
    var key = node.getAttribute("data-stage");
    var group = $$(".gos__node", node.parentNode.closest(".gos__svg, .gos__list") || document);
    node.addEventListener("click", function () { setStage(key); });
    node.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) setStage(key); });
    node.addEventListener("keydown", function (e) {
      var i = group.indexOf(node), step = 0;
      if (e.key === "Enter" || (e.key === " " && node.tagName !== "BUTTON")) { e.preventDefault(); setStage(key); }
      if (e.key === "ArrowRight" || e.key === "ArrowDown") step = 1;
      if (e.key === "ArrowLeft" || e.key === "ArrowUp") step = -1;
      if (step) { e.preventDefault(); var nx = group[(i + step + group.length) % group.length]; nx.focus(); setStage(nx.getAttribute("data-stage")); }
    });
  });

  /* ---------- Contact form → mailto (no fake success) ---------- */
  var form = $("#brief");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = $(".form__status", form);
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var v = function (n) { return (form.elements[n] && form.elements[n].value || "").trim(); };
      var subject = "Consultation brief: " + (v("type") || "Mobile growth") + " — " + v("name");
      var body = [
        "Name: " + v("name"),
        "Email: " + v("email"),
        "Consultation type: " + v("type"),
        "App / game link: " + (v("link") || "—"),
        "",
        "What I'd like to solve:",
        v("message")
      ].join("\n");
      var to = form.getAttribute("data-to");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      if (status) status.textContent = "Your email app should now open with this brief pre-filled. Nothing is sent until you press send there. If nothing opened, email " + to + " directly.";
    });
  }

  /* ---------- Page transitions ---------- */
  var overlay = $(".ptrans");
  function isInternalPage(a) {
    if (!a || a.target === "_blank" || a.hasAttribute("download")) return false;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(mailto:|tel:|javascript:)/i.test(href)) return false;
    var url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return false;
    if (url.pathname === location.pathname && url.hash) return false;
    return true;
  }
  if (overlay && hasGSAP && !reduce) {
    gsap.set(overlay, { scaleY: 1, transformOrigin: "top" });
    gsap.to(overlay, { scaleY: 0, duration: 0.7, ease: "power4.inOut", delay: 0.05 });
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      var a = e.target.closest("a");
      if (!isInternalPage(a)) return;
      e.preventDefault();
      var dest = a.href;
      gsap.set(overlay, { transformOrigin: "bottom" });
      gsap.to(overlay, { scaleY: 1, duration: 0.5, ease: "power4.inOut", onComplete: function () { location.href = dest; } });
    });
    window.addEventListener("pageshow", function (e) { if (e.persisted) gsap.set(overlay, { scaleY: 0 }); });
  }

  /* ---------- Custom cursor (desktop, fine pointer) ---------- */
  if (!reduce && hasGSAP && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    var cursor = document.createElement("div");
    cursor.className = "cursor"; cursor.setAttribute("aria-hidden", "true");
    cursor.innerHTML = '<div class="cursor__dot"></div><div class="cursor__ring"><span></span></div>';
    document.body.appendChild(cursor);
    html.classList.add("has-cursor");
    var dot = $(".cursor__dot", cursor), ring = $(".cursor__ring", cursor), label = $("span", ring);
    var dx = gsap.quickTo(dot, "x", { duration: 0.12, ease: "power3" }), dy = gsap.quickTo(dot, "y", { duration: 0.12, ease: "power3" });
    var rx = gsap.quickTo(ring, "x", { duration: 0.45, ease: "power3" }), ry = gsap.quickTo(ring, "y", { duration: 0.45, ease: "power3" });
    window.addEventListener("pointermove", function (e) { if (!cursor.dataset.on) { cursor.dataset.on = "1"; gsap.to(cursor, { opacity: 1, duration: 0.3 }); } dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY); });
    document.addEventListener("pointerover", function (e) {
      var v = e.target.closest("[data-cursor]");
      var h = e.target.closest("a, button, [role=button], .gos__node, input, select, textarea");
      cursor.classList.toggle("is-view", !!v);
      cursor.classList.toggle("is-hover", !v && !!h);
      label.textContent = v ? v.getAttribute("data-cursor") : "";
    });
    document.documentElement.addEventListener("mouseleave", function () { cursor.dataset.on = ""; gsap.to(cursor, { opacity: 0, duration: 0.2 }); });
  }

  /* ---------- Counters ---------- */
  function formatNum(n, dec) { return dec ? n.toFixed(dec) : Math.round(n).toString(); }
  function runCounter(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var dec = parseInt(el.getAttribute("data-decimals") || "0", 10);
    var out = $(".n", el) || el;
    if (!hasGSAP || reduce) { out.textContent = formatNum(target, dec); return; }
    var o = { v: 0 };
    gsap.to(o, { v: target, duration: 1.8, ease: "power3.out", onUpdate: function () { out.textContent = formatNum(o.v, dec); } });
  }

  /* ---------- Split words ---------- */
  function splitWords(el) {
    var nodes = Array.prototype.slice.call(el.childNodes);
    nodes.forEach(function (node) {
      if (node.nodeType === 3) {
        var parts = node.textContent.split(/(\s+)/);
        var frag = document.createDocumentFragment();
        parts.forEach(function (p) {
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(" ")); return; }
          var w = document.createElement("span"); w.className = "line word"; w.style.display = "inline-block";
          var i = document.createElement("span"); i.textContent = p; w.appendChild(i); frag.appendChild(w);
        });
        node.parentNode.replaceChild(frag, node);
      } else if (node.nodeType === 1 && node.tagName !== "BR") {
        splitWords(node);
      }
    });
  }

  /* ---------- No GSAP / reduced motion fallback ---------- */
  if (!hasGSAP || reduce) {
    html.classList.add("ready", "ready-fallback");
    $$("[data-count]").forEach(runCounter);
    return;
  }

  /* =====================  GSAP motion  ===================== */
  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: "power3.out" });
  html.classList.add("ready");


  /* Hero entrance */
  var hero = $(".hero, .phero");
  if (hero) {
    var tl = gsap.timeline({ delay: 0.1 });
    var step = function (sel, vars, pos) {
      var els = $$(sel, hero);
      if (els.length) tl.from(els, vars, tl.getChildren().length ? pos : 0);
    };
    step("[data-hero='eyebrow']", { opacity: 0, y: 14, duration: 0.7 });
    step("h1 .line > span", { yPercent: 115, rotate: 2, duration: 1.15, stagger: 0.09, ease: "power4.out" }, "-=0.45");
    step("[data-hero='fade']", { opacity: 0, y: 22, duration: 0.8, stagger: 0.06 }, "-=1");
    step("[data-hero='visual']", { opacity: 0, scale: 0.96, duration: 1.2, ease: "power2.out" }, "-=1.1");
    step(".hv-float", { opacity: 0, y: 30, duration: 0.9, stagger: 0.12 }, "-=0.8");
    step(".hv-bar", { scaleY: 0, transformOrigin: "50% 100%", duration: 0.9, stagger: 0.04 }, "-=1");
    tl.add(function () { $$("[data-count]", hero).forEach(runCounter); }, "-=0.9");

    var drawPaths = $$(".hv-line", hero);
    drawPaths.forEach(function (p) {
      var len = p.getTotalLength ? p.getTotalLength() : 600;
      gsap.fromTo(p, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: 2, ease: "power2.inOut", delay: 1 });
    });

    /* Mouse + scroll parallax on hero visual */
    var visual = $(".hero__visual", hero);
    if (visual && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      var floats = $$(".hv-float", visual);
      var setters = floats.map(function (f) {
        return { x: gsap.quickTo(f, "x", { duration: 1, ease: "power3" }), y: gsap.quickTo(f, "y", { duration: 1, ease: "power3" }), d: parseFloat(f.getAttribute("data-depth") || "1") };
      });
      hero.addEventListener("pointermove", function (e) {
        var cx = (e.clientX / window.innerWidth - 0.5), cy = (e.clientY / window.innerHeight - 0.5);
        setters.forEach(function (s) { s.x(cx * 24 * s.d); s.y(cy * 24 * s.d); });
      });
    }
    if (visual) {
      gsap.to(visual, { yPercent: 10, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
    }
  }

  /* Generic reveals */
  ScrollTrigger.batch("[data-reveal]", {
    start: "top 88%",
    once: true,
    onEnter: function (batch) { gsap.to(batch, { opacity: 1, y: 0, duration: 1, stagger: 0.08, overwrite: true }); }
  });

  /* Word-by-word headings */
  $$("[data-split]").forEach(function (el) {
    splitWords(el);
    gsap.from($$(".word > span", el), {
      yPercent: 110, duration: 1, stagger: 0.035, ease: "power4.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true }
    });
  });

  /* Statement colour scrub (about) */
  $$("[data-scrub-words]").forEach(function (el) {
    splitWords(el);
    var words = $$(".word > span", el);
    gsap.fromTo(words, { color: "#7d8694" }, {
      color: "#f4f5f6", stagger: 0.1, ease: "none",
      scrollTrigger: { trigger: el, start: "top 80%", end: "bottom 45%", scrub: true }
    });
  });

  /* Image clip reveal */
  $$("[data-clip]").forEach(function (el) {
    var img = $("img, svg", el);
    gsap.fromTo(el, { clipPath: "inset(12% 8% 12% 8% round 24px)" }, {
      clipPath: "inset(0% 0% 0% 0% round 20px)", duration: 1.4, ease: "power3.inOut",
      scrollTrigger: { trigger: el, start: "top 85%", once: true }
    });
    if (img) gsap.fromTo(img, { scale: 1.18 }, { scale: 1, duration: 1.8, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 85%", once: true } });
  });

  /* Parallax helpers */
  $$("[data-parallax]").forEach(function (el) {
    var amt = parseFloat(el.getAttribute("data-parallax")) || 10;
    gsap.fromTo(el, { yPercent: -amt }, { yPercent: amt, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true } });
  });

  /* Counters outside hero */
  $$("[data-count]").forEach(function (el) {
    if (el.closest(".hero")) return;
    ScrollTrigger.create({ trigger: el, start: "top 90%", once: true, onEnter: function () { runCounter(el); } });
  });

  /* Growth OS: draw connectors & reveal nodes; auto-advance stage with scroll */
  var gos = $(".gos");
  if (gos) {
    $$(".gos__path", gos).forEach(function (p) {
      var len = p.getTotalLength();
      gsap.fromTo(p, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, ease: "none", scrollTrigger: { trigger: gos, start: "top 75%", end: "center 50%", scrub: true } });
    });
    gsap.from($$(".gos__svg .gos__node", gos), { opacity: 0, scale: 0.85, transformOrigin: "50% 50%", duration: 0.7, stagger: 0.1, ease: "back.out(1.6)", scrollTrigger: { trigger: gos, start: "top 70%", once: true } });
    var userPicked = false;
    gosNodes.forEach(function (n) { n.addEventListener("click", function () { userPicked = true; }); });
    ScrollTrigger.create({
      trigger: gos, start: "top 55%", end: "bottom 45%",
      onUpdate: function (self) {
        if (userPicked) return;
        var idx = Math.min(gosKeys.length - 1, Math.floor(self.progress * gosKeys.length));
        setStage(gosKeys[idx]);
      }
    });
  }

  /* Timeline fill */
  var tfill = $(".timeline__fill");
  if (tfill) gsap.to(tfill, { scaleY: 1, ease: "none", scrollTrigger: { trigger: ".timeline", start: "top 70%", end: "bottom 60%", scrub: true } });

  /* Horizontal case gallery (desktop only) */
  var mm = gsap.matchMedia();
  mm.add("(min-width: 961px)", function () {
    var hs = $(".hscroll[data-pin]");
    if (!hs) return;
    var track = $(".hscroll__track", hs);
    var bar = $(".hs-progress span", hs);
    var getDist = function () { return Math.max(0, track.scrollWidth - hs.clientWidth); };
    if (getDist() < 40) return;
    hs.classList.add("is-pinned");
    var tween = gsap.to(track, {
      x: function () { return -getDist(); },
      ease: "none",
      scrollTrigger: {
        trigger: hs.closest("section") || hs,
        start: "top top",
        end: function () { return "+=" + getDist(); },
        pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1,
        onUpdate: function (self) { if (bar) bar.style.transform = "scaleX(" + self.progress + ")"; }
      }
    });
    return function () { hs.classList.remove("is-pinned"); tween.kill(); gsap.set(track, { clearProps: "transform" }); };
  });

  /* Footer word drift */
  var fw = $(".footer__word");
  if (fw) gsap.fromTo(fw, { xPercent: 4 }, { xPercent: -6, ease: "none", scrollTrigger: { trigger: fw, start: "top bottom", end: "bottom top", scrub: true } });

  window.addEventListener("load", function () { ScrollTrigger.refresh(); });
})();
