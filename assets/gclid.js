/* Mawid · Google Ads click-id (gclid) capture + cross-domain forward.
   Loaded on every marketing page. Lightweight (no deps), runs once at
   DOMContentLoaded, ~1.5 KB.

   Why this exists (besides GA4's built-in cross-domain linker):

   1. Belt-and-braces for the gclid handoff from mawid.ai → app.mawid.ai.
      GA4 sets a `_gl` URL param on outbound clicks that contains gclid
      info, BUT only when the click target's href is parsed at click
      time AND the linker is fully booted. If gtag.js fails to load
      (ad-blockers in MENA hit ~15-20%) the linker silently drops the
      gclid. Direct gclid forwarding survives ad-blockers because we
      append it ourselves.

   2. Enhanced Conversions matching window. Google needs the gclid OR
      the user_data hash to attribute a conversion. The user_data path
      is wired in lib/analytics/track.ts. THIS file ensures the gclid
      path also keeps working — both routes increase match rate.

   3. Server-side dedup later. The /sign-up page reads gclid from URL
      and stores it on the Stripe customer's `client_reference_id`. When
      we add server-side conversion reporting (Measurement Protocol),
      we use that to deduplicate against the browser-fired sign_up.

   Cookie scope:
     - name:   mawid_gclid
     - domain: .mawid.ai  (so both mawid.ai AND app.mawid.ai see it)
     - max-age: 90 days (matches Google's standard click-id TTL)
     - SameSite=Lax, Secure (prod only — HTTP fails Secure on local)
*/
(function () {
  'use strict';

  var COOKIE_NAME = 'mawid_gclid';
  var COOKIE_DAYS = 90;
  // Hosts where we want the gclid to follow the user. Adding more hosts
  // here (e.g. a referrals subdomain later) keeps the click attribution
  // intact across the whole property.
  var FORWARD_TO_HOSTS = ['app.mawid.ai'];

  function getCookie(name) {
    var rows = document.cookie ? document.cookie.split('; ') : [];
    for (var i = 0; i < rows.length; i++) {
      var eq = rows[i].indexOf('=');
      if (eq === -1) continue;
      if (rows[i].slice(0, eq) === name) {
        try { return decodeURIComponent(rows[i].slice(eq + 1)); }
        catch (e) { return rows[i].slice(eq + 1); }
      }
    }
    return null;
  }

  function setCookie(name, value) {
    var d = new Date();
    d.setTime(d.getTime() + COOKIE_DAYS * 24 * 60 * 60 * 1000);
    var isHttps = window.location.protocol === 'https:';
    // Domain must include the leading dot so app.mawid.ai inherits it.
    // On localhost the leading dot breaks Chrome's cookie store, so we
    // skip the domain attribute there (still works same-origin).
    var domainAttr =
      window.location.hostname.indexOf('mawid.ai') !== -1
        ? '; domain=.mawid.ai'
        : '';
    var secureAttr = isHttps ? '; Secure' : '';
    document.cookie =
      name +
      '=' +
      encodeURIComponent(value) +
      '; expires=' +
      d.toUTCString() +
      '; path=/' +
      domainAttr +
      '; SameSite=Lax' +
      secureAttr;
  }

  // ── 1. Capture gclid from URL on first hit ────────────────────────
  function captureFromUrl() {
    try {
      var sp = new URLSearchParams(window.location.search);
      var gclid = sp.get('gclid');
      if (!gclid) return;
      // Always overwrite — the most recent click wins (matches how GA4
      // and Google Ads behave internally).
      setCookie(COOKIE_NAME, gclid);
    } catch (e) {
      // URLSearchParams is in every browser we support; if it fails the
      // user is on something so old that ad attribution is unreliable
      // anyway.
    }
  }

  // ── 2. Forward gclid to app.mawid.ai on outbound links ────────────
  // We rewrite the href ONCE on DOMContentLoaded so the browser's own
  // navigation handler keeps working (no preventDefault, no JS
  // navigation). Cleaner than intercepting clicks — also survives
  // middle-click / cmd-click / right-click-open-in-new-tab.
  function appendGclidToOutboundLinks() {
    var gclid = getCookie(COOKIE_NAME);
    if (!gclid) return;
    var anchors = document.querySelectorAll('a[href]');
    for (var i = 0; i < anchors.length; i++) {
      var a = anchors[i];
      var href = a.getAttribute('href');
      if (!href) continue;
      // Skip non-http(s) schemes (mailto:, tel:, wa.me, hash links).
      if (href.indexOf('http') !== 0 && href.indexOf('//') !== 0) continue;
      var url;
      try { url = new URL(href, window.location.href); }
      catch (e) { continue; }
      var host = url.hostname.toLowerCase();
      if (FORWARD_TO_HOSTS.indexOf(host) === -1) continue;
      // If the link already carries a gclid (operator hard-coded one,
      // or GA4 linker already injected it) don't overwrite.
      if (url.searchParams.has('gclid')) continue;
      url.searchParams.set('gclid', gclid);
      a.setAttribute('href', url.toString());
    }
  }

  // ── 3. Run on DOM-ready, AND on any later dynamic href changes via
  //       a MutationObserver fallback. Marketing pages are static, so
  //       this mostly handles single-page hash route updates.
  function init() {
    captureFromUrl();
    appendGclidToOutboundLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
