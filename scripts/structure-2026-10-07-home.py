"""One-off structural edits to index.html + ar/index.html (2026-10-07).

Pairs with copy-2026-10-07-home.py. Removes UI for features Mawid doesn't
have, wires the setup-call form to the real lead endpoint, and drops the
in-browser translation (text is baked into the HTML by build.mjs).
Every replacement must match exactly once per file, or the script aborts.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

def sub_once(s, pattern, repl, label, flags=re.S):
    new, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f'ABORT: {label}: matched {n} times')
    return new

FEAT3_VISUAL = '''<div class="feat-visual">
          <div class="feat-cust">
            <div class="cust-head">
              <span data-i18n="feat.3.head">Today · Thursday</span>
              <span class="cust-count">4</span>
            </div>
            <div class="cust-row">
              <div class="cust-meta">
                <div class="cust-name" data-i18n="feat.3.r1n">Maysa</div>
                <div class="cust-sub" data-i18n="feat.3.r1s">10:00 – 18:00 · 5 bookings</div>
              </div>
              <span class="cust-tag tag-reg" data-i18n="feat.3.tagOn">On shift</span>
            </div>
            <div class="cust-row">
              <div class="cust-meta">
                <div class="cust-name" data-i18n="feat.3.r2n">Hessa</div>
                <div class="cust-sub" data-i18n="feat.3.r2s">Day off</div>
              </div>
              <span class="cust-tag tag-lapsed" data-i18n="feat.3.tagOff">Off</span>
            </div>
            <div class="cust-row">
              <div class="cust-meta">
                <div class="cust-name" data-i18n="feat.3.r3n">Dhuhr prayer</div>
                <div class="cust-sub" data-i18n="feat.3.r3s">12:05 – 12:35 · nobody can book</div>
              </div>
              <span class="cust-tag tag-vip" data-i18n="feat.3.tagAuto">Auto</span>
            </div>
            <div class="cust-row">
              <div class="cust-meta">
                <div class="cust-name" data-i18n="feat.3.r4n">Noura</div>
                <div class="cust-sub" data-i18n="feat.3.r4s">14:00 – 22:00 · 3 bookings</div>
              </div>
              <span class="cust-tag tag-reg" data-i18n="feat.3.tagOn">On shift</span>
            </div>
          </div>
        </div>'''

VT_GRID = '''<div class="vt-grid">
            <div class="vt-card">
              <div class="vt-head" data-i18n="feat.6.t1">Salon · service + stylist</div>
              <div class="vt-rows">
                <div class="vt-row"><span class="vt-l" data-i18n="feat.6.t1a">Service</span><span class="vt-r" data-i18n="feat.6.t1av">Color + cut</span></div>
                <div class="vt-row"><span class="vt-l" data-i18n="feat.6.t1b">Stylist</span><span class="vt-r" data-i18n="feat.6.t1bv">Maysa</span></div>
                <div class="vt-row"><span class="vt-l" data-i18n="feat.6.t1c">When</span><span class="vt-r" data-i18n="feat.6.t1cv">Fri 10:00</span></div>
              </div>
            </div>
            <div class="vt-card">
              <div class="vt-head" data-i18n="feat.6.t2">Restaurant · reservation</div>
              <div class="vt-rows">
                <div class="vt-check"><span class="vt-box done"></span><span data-i18n="feat.6.t2a">Party of 4</span></div>
                <div class="vt-check"><span class="vt-box done"></span><span data-i18n="feat.6.t2b">Table capacity checked</span></div>
                <div class="vt-check"><span class="vt-box"></span><span class="vt-pending" data-i18n="feat.6.t2c">Note: patio, birthday</span></div>
              </div>
            </div>
          </div>'''

# Runtime for the homepage once translation is baked in: header scroll state,
# reveal-on-scroll, mobile menu, language choice cookie, and the setup form.
RUNTIME = r'''<script>
/* Mawid homepage runtime. Copy is baked into the HTML (scripts/build.mjs),
   so there is no translation step here. */
(function () {
  "use strict";
  var isAr = document.documentElement.lang === "ar";

  /* Remember an explicit language choice so the Arabic-default redirect
     (vercel.json) never overrides it. */
  document.querySelectorAll("[data-lang]").forEach(function (a) {
    a.addEventListener("click", function () {
      document.cookie = "mawid_lang=" + a.getAttribute("data-lang") + "; path=/; max-age=31536000; samesite=lax";
    });
  });

  /* Sticky header shadow */
  var header = document.getElementById("header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 12); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* Reveal on scroll. Elements already in view at load are shown at once,
     so the hero never waits on this script. */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* Setup-call form → app.mawid.ai/api/public/lead */
  var form = document.getElementById("signup-form");
  if (form) {
    var success = document.getElementById("form-success");
    var errorBox = document.getElementById("form-error");
    var submitBtn = document.getElementById("submit-btn");
    form.querySelectorAll("input, select").forEach(function (el) {
      var reset = function () { el.style.borderColor = ""; };
      el.addEventListener("input", reset);
      el.addEventListener("change", reset);
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstInvalid = null;
      form.querySelectorAll("[required]").forEach(function (el) {
        if (!el.value.trim()) { el.style.borderColor = "#E07070"; firstInvalid = firstInvalid || el; }
      });
      if (firstInvalid) { firstInvalid.focus(); return; }

      var fd = new FormData(form);
      var sp = new URLSearchParams(location.search);
      var utm = {};
      ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"].forEach(function (k) {
        if (sp.get(k)) utm[k] = sp.get(k);
      });
      var gclidMatch = document.cookie.match(/(?:^|; )mawid_gclid=([^;]+)/);
      var payload = {
        source: "home",
        businessName: fd.get("business") || undefined,
        name: fd.get("name") || undefined,
        phone: fd.get("phone") || undefined,
        country: fd.get("country") || undefined,
        vertical: fd.get("vertical") || undefined,
        website: fd.get("website") || undefined,
        locale: isAr ? "ar" : "en",
        pageUrl: location.href.slice(0, 500),
        referrer: (document.referrer || "").slice(0, 500) || undefined,
        utm: utm,
        gclid: sp.get("gclid") || (gclidMatch ? decodeURIComponent(gclidMatch[1]) : undefined)
      };

      submitBtn.classList.add("is-loading");
      submitBtn.disabled = true;
      if (errorBox) errorBox.hidden = true;

      fetch("https://app.mawid.ai/api/public/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function () {
          form.style.display = "none";
          success.classList.add("shown");
          /* Only count a lead once the server has actually saved it. */
          if (typeof gtag === "function") {
            gtag("event", "generate_lead", { source: "home_setup_form", vertical: payload.vertical, country: payload.country });
          }
          if (typeof fbq === "function") {
            fbq("track", "Lead", { content_name: "Setup call", content_category: payload.vertical });
          }
        })
        .catch(function () {
          submitBtn.classList.remove("is-loading");
          submitBtn.disabled = false;
          if (errorBox) errorBox.hidden = false;
        });
    });
  }

  /* Mobile menu */
  var btn = document.querySelector(".mobile-menu-btn");
  var menu = document.getElementById("mobile-menu");
  if (btn && menu) {
    var setOpen = function (open) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      menu.classList.toggle("open", open);
      document.body.style.overflow = open ? "hidden" : "";
    };
    btn.addEventListener("click", function () { setOpen(btn.getAttribute("aria-expanded") !== "true"); });
    menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    var mql = window.matchMedia("(min-width: 941px)");
    var onChange = function (e) { if (e.matches) setOpen(false); };
    if (mql.addEventListener) mql.addEventListener("change", onChange); else if (mql.addListener) mql.addListener(onChange);
  }
})();
</script>'''


def process(rel, is_ar):
    p = ROOT / rel
    s = p.read_text()

    # 1. AI dialect demo -> team schedule list
    s = sub_once(s, r'<div class="feat-visual">\s*<div class="feat-ai">.*?</div>\s*</div>\s*</div>(\s*</div>\s*<!-- Bilingual -->)',
                 FEAT3_VISUAL + r'\n      </div>\1', 'feat-3 visual')
    s = sub_once(s, r'<!-- AI assistant -->', '<!-- Team & schedules -->', 'feat-3 comment')

    # 2. Vertical templates visual -> business types
    s = sub_once(s, r'<div class="vt-grid">.*?</div>\s*</div>\s*</div>(?=\s*</div>\s*</div>\s*</div>\s*</div>\s*</section>)',
                 VT_GRID, 'vt-grid')
    s = sub_once(s, r'<!-- Vertical templates — large -->', '<!-- Business types — large -->', 'feat-6 comment')

    # 3. WhatsApp card link: a real booking page, not a pay/reschedule link
    s = sub_once(s, r'aria-label="Manage booking"', 'aria-label="Booking page"', 'wa link aria')
    s = sub_once(s, r'<span class="pl-url">[^<]*</span>', '<span class="pl-url">mawid.ai/book/salon-rasha</span>', 'wa link url')

    # 4. Preview tiles: illustrative numbers that match the new labels
    s = sub_once(s, r'(data-i18n="prev\.k2">[^<]*</span>\s*<div class="val">)[^<]*(</div>)', r'\g<1>4.8%\2', 'k2 val')
    s = sub_once(s, r'(data-i18n="prev\.k4">[^<]*</span>\s*<div class="val">)[^<]*(</div>)', r'\g<1>31\2', 'k4 val')

    # 5. Mockup Gregorian/Hijri toggles (not a product control) -> removed
    n_before = s.count('class="hp-toggle"')
    s = re.sub(r'\s*<div class="hp-toggle">.*?</div>', '', s, flags=re.S)
    if s.count('class="hp-toggle"') != 0 or n_before == 0:
        sys.exit('ABORT: hp-toggle removal')

    # 6. Phone mockup: "Questions? Chat on WhatsApp" (no SMS)
    s = sub_once(s, r'\s*<span class="pay-tag">SMS</span>', '', 'sms chip')

    # 7. Public roadmap with dated quarters -> removed (auditor: gives prospects a reason to wait)
    s = sub_once(s, r'<!-- ROADMAP / COMING SOON -->.*?(?=<!-- BETA CTA -->)', '', 'roadmap')

    # 8. Setup form: more business types, honeypot, error message
    s = sub_once(s, r'(<option value="salon"[^>]*data-i18n="beta\.v\.salon"[^>]*>[^<]*</option>)',
                 r'\1\n                  <option value="barbershop" data-i18n="beta.v.barber">Barbershop</option>\n                  <option value="restaurant" data-i18n="beta.v.restaurant">Restaurant</option>',
                 'vertical options')
    s = sub_once(s, r'(<form id="signup-form" novalidate>)',
                 r'\1\n          <!-- Honeypot: hidden from people, filled by bots -->\n          <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">',
                 'honeypot')
    s = sub_once(s, r'(<button[^>]*id="submit-btn")', r'<p id="form-error" class="form-error" role="alert" hidden data-i18n="beta.f.error">Something went wrong. Please try again, or email hello@mawid.ai.</p>\n          \1', 'error box')

    # 9. CSS: form error message, and the hero shows immediately. Hero text
    #    used to start at opacity 0 until the reveal script ran, which made
    #    the main content appear ~10s late on phones.
    s = sub_once(s, r'(\.form-success \{ display: none;)',
                 '.form-error { color: #FFB4A8; font-size: 13px; line-height: 1.5; margin: 0 0 12px; }\n'
                 '.hero .reveal { opacity: 1; transform: none; transition: none; }\n'
                 r'\1', 'css additions')

    # 10. Replace the inline translation + demo script with the slim runtime
    s = sub_once(s, r'<script>\s*const I18N = .*?</script>', RUNTIME, 'inline runtime')

    p.write_text(s)
    print('ok', rel)


process('index.html', False)
process('ar/index.html', True)
