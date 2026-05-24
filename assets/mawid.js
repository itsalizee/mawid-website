/* Mawid · Shared interactive behaviors
   Loaded on every sub-page. Reads from window.MAWID_I18N. */

(function () {
  "use strict";

  /* ===== Language toggle + i18n application ===== */
  var STORAGE_KEY = "mawid.locale";
  var DEFAULT = "en";

  function detectInitial() {
    /* URL is the single source of truth.
       /ar/* → Arabic. Anything else → English.
       localStorage is intentionally ignored to prevent stale state. */
    return window.location.pathname.indexOf("/ar/") !== -1 ? "ar" : "en";
  }

  function applyLocale(locale) {
    var dict = (window.MAWID_I18N && window.MAWID_I18N[locale]) || {};
    var html = document.documentElement;
    html.setAttribute("lang", locale);
    html.setAttribute("dir", locale === "ar" ? "rtl" : "ltr");

    /* Replace data-i18n strings */
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var val = dict[key];
      if (typeof val === "string") el.innerHTML = val;
    });
    /* Replace data-i18n-attr (e.g., placeholders) */
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      var pair = el.getAttribute("data-i18n-attr").split(":");
      if (pair.length !== 2) return;
      var attr = pair[0].trim();
      var key = pair[1].trim();
      var val = dict[key];
      if (typeof val === "string") el.setAttribute(attr, val);
    });

    /* Update lang toggle pressed state */
    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-lang") === locale ? "true" : "false");
    });

    try { localStorage.setItem(STORAGE_KEY, locale); } catch (e) {}
  }

  function bindLangToggle() {
    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        /* If this is an anchor with href, let browser navigate naturally —
           don't apply locale in-place because the new page will set its own. */
        if (btn.tagName === "A" && btn.getAttribute("href")) return;
        applyLocale(btn.getAttribute("data-lang"));
      });
    });
  }

  /* ===== Sticky header on scroll ===== */
  function bindStickyHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var lastY = -1;
    function update() {
      var y = window.scrollY || document.documentElement.scrollTop;
      if ((y > 8) !== (lastY > 8)) {
        header.classList.toggle("scrolled", y > 8);
      }
      lastY = y;
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  /* ===== Reveal-on-scroll ===== */
  function bindReveals() {
    if (!("IntersectionObserver" in window)) {
      document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -60px 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  }

  /* ===== FAQ accordion ===== */
  function bindFaq() {
    document.querySelectorAll(".faq-question").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var expanded = btn.getAttribute("aria-expanded") === "true";
        /* Close siblings (single-open behavior) */
        btn.closest(".faq-list").querySelectorAll(".faq-question").forEach(function (b) {
          if (b !== btn) b.setAttribute("aria-expanded", "false");
        });
        btn.setAttribute("aria-expanded", expanded ? "false" : "true");
      });
    });
  }

  /* ===== Contact form handler ===== */
  function bindContactForm() {
    var form = document.getElementById("contact-form");
    if (!form) return;
    var success = document.getElementById("contact-success");
    var submitBtn = form.querySelector("button[type=submit]");

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      /* Basic required-field validation */
      var firstInvalid = null;
      form.querySelectorAll("[required]").forEach(function (el) {
        if (!el.value.trim()) {
          el.style.borderColor = "#E07070";
          if (!firstInvalid) firstInvalid = el;
        } else {
          el.style.borderColor = "";
        }
      });
      if (firstInvalid) {
        firstInvalid.focus();
        firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add("is-loading");
      }

      var data = Object.fromEntries(new FormData(form).entries());
      data.locale = document.documentElement.getAttribute("lang");
      data.timestamp = new Date().toISOString();
      data.referrer = document.referrer || "direct";
      data.page = window.location.pathname;
      data.utm_source = new URLSearchParams(window.location.search).get("utm_source") || "";
      data.utm_medium = new URLSearchParams(window.location.search).get("utm_medium") || "";
      data.utm_campaign = new URLSearchParams(window.location.search).get("utm_campaign") || "";

      /* TODO: wire to backend endpoint
         fetch("/api/contact", {
           method: "POST",
           headers: { "Content-Type": "application/json" },
           body: JSON.stringify(data)
         });
      */
      console.log("[mawid contact form]", data);

      /* Conversion tracking */
      if (typeof window.gtag === "function") {
        window.gtag("event", "contact_submit", { method: "form", subject: data.subject });
      }
      if (typeof window.fbq === "function") {
        window.fbq("track", "Contact", { content_name: "Contact form" });
      }

      setTimeout(function () {
        form.style.display = "none";
        if (success) success.classList.add("shown");
      }, 500);
    });

    form.querySelectorAll("input, select, textarea").forEach(function (el) {
      el.addEventListener("input", function () { el.style.borderColor = ""; });
      el.addEventListener("change", function () { el.style.borderColor = ""; });
    });
  }

  /* ===== Mobile menu (hamburger) ===== */
  function bindMobileMenu() {
    var btn = document.querySelector(".mobile-menu-btn");
    var menu = document.getElementById("mobile-menu");
    if (!btn || !menu) return;
    function setOpen(open) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      menu.classList.toggle("open", open);
      document.body.style.overflow = open ? "hidden" : "";
    }
    btn.addEventListener("click", function () {
      setOpen(btn.getAttribute("aria-expanded") !== "true");
    });
    /* Close on link tap */
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    /* Close on Escape */
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") setOpen(false);
    });
    /* Close if viewport grows past mobile breakpoint */
    var mql = window.matchMedia("(min-width: 941px)");
    mql.addEventListener("change", function (e) { if (e.matches) setOpen(false); });
  }

  /* ===== Init ===== */
  function init() {
    applyLocale(detectInitial());
    bindLangToggle();
    bindStickyHeader();
    bindReveals();
    bindFaq();
    bindContactForm();
    bindMobileMenu();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
