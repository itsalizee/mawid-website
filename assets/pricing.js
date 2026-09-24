/* Mawid · Local-currency pricing (SAR · AED · QAR · KWD · USD)

   The HTML ships USD prices. This script asks the app which currencies
   Stripe can charge right now, plus the visitor's country, and re-renders
   every price in the right one: a Riyadh visitor sees SAR, Dubai AED,
   Doha QAR, Kuwait City KWD, everyone else USD.

   Source of truth is the app (lib/billing/pricing.ts via
   https://app.mawid.ai/api/public/pricing). The page never carries its own
   price table, so the site can't drift from what Checkout charges. If the
   request fails or Stripe hasn't been synced, the USD HTML stays as-is,
   which is always correct.

   Markup contract:
     <div class="tier-price" data-plan="starter">   .currency + .num re-rendered
     <div class="vert-price" data-plan="studio">    same
     <span data-price-text="studio">$180</span>     inline copy ("SAR 679")
     <div data-currency-switcher hidden></div>      chips, shown if 2+ currencies

   Choice order: ?currency=sar in the URL → the visitor's own pick
   (localStorage) → country from IP → USD.
*/
(function () {
  'use strict';

  var ENDPOINT = 'https://app.mawid.ai/api/public/pricing';
  var STORE_KEY = 'mawid.currency';
  var PENDING_CLASS = 'mawid-price-pending';
  var ORDER = ['sar', 'aed', 'qar', 'kwd', 'usd'];
  var SYMBOLS = {
    en: { usd: '$', sar: 'SAR', aed: 'AED', qar: 'QAR', kwd: 'KWD' },
    ar: { usd: '$', sar: 'ر.س', aed: 'د.إ', qar: 'ر.ق', kwd: 'د.ك' }
  };
  var CHIP_LABELS = {
    en: { usd: 'USD', sar: 'SAR', aed: 'AED', qar: 'QAR', kwd: 'KWD' },
    ar: { usd: 'دولار', sar: 'ريال سعودي', aed: 'درهم', qar: 'ريال قطري', kwd: 'دينار' }
  };

  var data = null;
  var current = 'usd';

  function lang() {
    var l = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (l.indexOf('ar') === 0) return 'ar';
    if (l) return 'en';
    return location.pathname.indexOf('/ar/') === 0 ? 'ar' : 'en';
  }

  function supported(c) {
    return !!(data && data.currencies && data.currencies.indexOf(c) !== -1);
  }

  function formatAmount(plan, c) {
    var minor = data.prices[plan] && data.prices[plan][c];
    if (typeof minor !== 'number') return null;
    var dec = data.decimals[c] || 0;
    var major = minor / Math.pow(10, dec);
    return major % 1 === 0 ? String(major) : major.toFixed(dec).replace(/0+$/, '');
  }

  function priceText(plan, c, l) {
    var amount = formatAmount(plan, c);
    if (amount === null) return null;
    var sym = SYMBOLS[l][c];
    if (c === 'usd') return '$' + amount;
    return l === 'ar' ? amount + ' ' + sym : sym + ' ' + amount;
  }

  function render() {
    if (!data) return;
    var l = lang();

    var blocks = document.querySelectorAll('[data-plan]');
    for (var i = 0; i < blocks.length; i++) {
      var el = blocks[i];
      var amount = formatAmount(el.getAttribute('data-plan'), current);
      var num = el.querySelector('.num');
      var cur = el.querySelector('.currency');
      if (amount === null || !num || !cur) continue;
      num.textContent = amount;
      cur.textContent = SYMBOLS[l][current];
      // EN reads "SAR 299" (symbol first); AR reads "299 ر.س" (amount
      // first), which RTL flow lays out with the symbol on the left.
      var wantNumFirst = l === 'ar';
      var numIsFirst = !!(num.compareDocumentPosition(cur) & Node.DOCUMENT_POSITION_FOLLOWING);
      if (wantNumFirst !== numIsFirst) {
        if (wantNumFirst) el.insertBefore(num, cur);
        else el.insertBefore(cur, num);
      }
    }

    var inline = document.querySelectorAll('[data-price-text]');
    for (var j = 0; j < inline.length; j++) {
      var t = priceText(inline[j].getAttribute('data-price-text'), current, l);
      if (t) inline[j].textContent = t;
    }

    renderSwitchers(l);
    document.documentElement.setAttribute('data-currency', current);
  }

  function renderSwitchers(l) {
    var boxes = document.querySelectorAll('[data-currency-switcher]');
    var options = ORDER.filter(supported);
    for (var i = 0; i < boxes.length; i++) {
      var box = boxes[i];
      if (options.length < 2) { box.hidden = true; continue; }
      box.hidden = false;
      box.setAttribute('role', 'group');
      box.setAttribute('aria-label', l === 'ar' ? 'العملة' : 'Currency');
      box.innerHTML = '';
      for (var k = 0; k < options.length; k++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('data-currency', options[k]);
        b.setAttribute('aria-pressed', options[k] === current ? 'true' : 'false');
        b.textContent = CHIP_LABELS[l][options[k]];
        box.appendChild(b);
      }
    }
  }

  function choose(c, persist) {
    if (!supported(c)) return;
    current = c;
    if (persist) { try { localStorage.setItem(STORE_KEY, c); } catch (e) {} }
    render();
  }

  function initialCurrency() {
    try {
      var fromUrl = new URLSearchParams(location.search).get('currency');
      if (fromUrl && supported(fromUrl.toLowerCase())) return fromUrl.toLowerCase();
    } catch (e) {}
    try {
      var stored = localStorage.getItem(STORE_KEY);
      if (stored && supported(stored)) return stored;
    } catch (e) {}
    return supported(data.currency) ? data.currency : 'usd';
  }

  /** Validate the payload shape before trusting it for rendering. */
  function valid(d) {
    return !!(d && d.prices && d.decimals && Object.prototype.toString.call(d.currencies) === '[object Array]');
  }

  function apply(d) {
    if (!valid(d)) return;
    data = d;
    current = initialCurrency();
    render();
  }

  function injectStyles() {
    if (document.getElementById('mawid-pricing-css')) return;
    var css =
      '.' + PENDING_CLASS + ' [data-plan] .num,.' + PENDING_CLASS + ' [data-plan] .currency,' +
      '.' + PENDING_CLASS + ' [data-price-text]{visibility:hidden}' +
      '.currency-switch{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin:0 auto 28px;' +
      'font-family:var(--mono,ui-monospace,monospace);font-size:12px}' +
      '.currency-switch[hidden]{display:none}' +
      '.currency-switch button{padding:7px 14px;border-radius:999px;border:1px solid var(--line,#e6e2dc);' +
      'background:var(--bg,#fff);color:var(--muted,#7a746c);cursor:pointer;letter-spacing:.04em;font:inherit;' +
      'transition:color .15s,background .15s,border-color .15s}' +
      '.currency-switch button:hover{color:var(--ink,#111);border-color:var(--ink,#111)}' +
      '.currency-switch button[aria-pressed="true"]{background:var(--ink,#111);color:var(--bg,#fff);border-color:var(--ink,#111)}' +
      'html[lang^="ar"] .currency-switch{font-family:var(--body-ar,inherit);font-size:13px}';
    var s = document.createElement('style');
    s.id = 'mawid-pricing-css';
    s.textContent = css;
    document.head.appendChild(s);
  }

  function init() {
    if (!document.querySelector('[data-plan],[data-price-text]')) return;
    injectStyles();

    document.addEventListener('click', function (e) {
      var btn = e.target && e.target.closest && e.target.closest('[data-currency-switcher] button[data-currency]');
      if (btn) choose(btn.getAttribute('data-currency'), true);
    });

    // The home page swaps EN/AR in place; re-render symbol order + chip labels.
    if ('MutationObserver' in window) {
      new MutationObserver(render).observe(document.documentElement, {
        attributes: true, attributeFilter: ['lang']
      });
    }

    // Hide amounts briefly so Gulf visitors don't see "$80" flip to
    // "SAR 299". Never longer than 1.2s — the USD HTML is a valid fallback.
    var root = document.documentElement;
    root.classList.add(PENDING_CLASS);
    var reveal = function () { root.classList.remove(PENDING_CLASS); };
    var timer = setTimeout(reveal, 1200);

    if (!window.fetch) { reveal(); return; }
    var controller = 'AbortController' in window ? new AbortController() : null;
    if (controller) setTimeout(function () { controller.abort(); }, 4000);

    fetch(ENDPOINT, { credentials: 'omit', signal: controller ? controller.signal : undefined })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(apply)
      .catch(function () { /* keep the USD HTML */ })
      .then(function () { clearTimeout(timer); reveal(); });
  }

  window.MawidPricing = { apply: apply, choose: choose };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
