/* Mawid · Shared interactive behaviors
   Loaded on every sub-page. */

(function () {
  "use strict";

  /* ===== Language toggle =====
     Page text is baked into the HTML at build time (scripts/build.mjs), so
     there is nothing to translate here. We only remember the visitor's
     explicit choice in a cookie; vercel.json reads it so an Arabic-default
     redirect never overrides someone who picked English (or vice versa). */
  function bindLangToggle() {
    document.querySelectorAll("[data-lang]").forEach(function (el) {
      el.addEventListener("click", function () {
        var lang = el.getAttribute("data-lang") === "ar" ? "ar" : "en";
        document.cookie = "mawid_lang=" + lang + "; path=/; max-age=31536000; SameSite=Lax";
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

  /* ===== Contact form → app.mawid.ai/api/public/lead ===== */
  function bindContactForm() {
    var form = document.getElementById("contact-form");
    if (!form) return;
    var success = document.getElementById("contact-success");
    var errorBox = document.getElementById("contact-error");
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

      var fd = new FormData(form);
      var sp = new URLSearchParams(window.location.search);
      var utm = {};
      ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"].forEach(function (k) {
        if (sp.get(k)) utm[k] = sp.get(k);
      });
      var gclidMatch = document.cookie.match(/(?:^|; )mawid_gclid=([^;]+)/);
      var subject = form.querySelector("#cf-subject");
      var subjectLabel = subject && subject.selectedIndex >= 0 ? subject.options[subject.selectedIndex].text : "";
      var payload = {
        source: "contact",
        name: fd.get("name") || undefined,
        email: fd.get("email") || undefined,
        businessName: fd.get("business") || undefined,
        message: ((subjectLabel ? "[" + subjectLabel + "] " : "") + (fd.get("message") || "")).slice(0, 2000),
        website: fd.get("website") || undefined,
        locale: document.documentElement.getAttribute("lang") === "ar" ? "ar" : "en",
        pageUrl: window.location.href.slice(0, 500),
        referrer: (document.referrer || "").slice(0, 500) || undefined,
        utm: utm,
        gclid: sp.get("gclid") || (gclidMatch ? decodeURIComponent(gclidMatch[1]) : undefined)
      };

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add("is-loading");
      }
      if (errorBox) errorBox.hidden = true;

      fetch("https://app.mawid.ai/api/public/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function () {
          form.style.display = "none";
          if (success) success.classList.add("shown");
          /* Only count the conversion once the server has saved the lead. */
          if (typeof window.gtag === "function") {
            window.gtag("event", "generate_lead", { source: "contact_form", subject: fd.get("subject") });
          }
          if (typeof window.fbq === "function") {
            window.fbq("track", "Contact", { content_name: "Contact form" });
          }
        })
        .catch(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove("is-loading");
          }
          if (errorBox) errorBox.hidden = false;
        });
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
