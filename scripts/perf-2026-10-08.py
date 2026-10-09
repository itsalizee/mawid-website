"""One-off page-speed pass over every page.

- GA4 + Meta Pixel: same tags and IDs, but the two vendor scripts load
  after the page has finished loading (idle callback). Calls made earlier
  (page_view, conversions) are queued by the standard stubs.
- Google Fonts: trimmed to the weights actually used (no 300; Instrument
  Serif italic only; Reem Kufi 600 only) and loaded without blocking
  render (preload + media swap, noscript fallback).
- Above-the-fold .reveal content on sub-pages is visible immediately
  (assets/mawid.css), instead of waiting for JS.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

ANALYTICS = """<script>
  /* GA4 + Meta Pixel. The vendor scripts load once the page is idle so
     they don't compete with first paint; earlier calls are queued. */
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  // Cross-domain linker so the user's journey stitches mawid.ai ↔ app.mawid.ai
  gtag('config', 'G-Y7V29X4R34', {
    linker: { domains: ['mawid.ai', 'app.mawid.ai'] }
  });
  !function(f){if(f.fbq)return;var n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];}(window);
  fbq('init', '1016451274045170');
  fbq('track', 'PageView');
  (function () {
    function load() {
      ['https://www.googletagmanager.com/gtag/js?id=G-Y7V29X4R34',
       'https://connect.facebook.net/en_US/fbevents.js'].forEach(function (src) {
        var s = document.createElement('script');
        s.async = true; s.src = src; document.head.appendChild(s);
      });
    }
    function later() {
      if ('requestIdleCallback' in window) requestIdleCallback(load, { timeout: 2500 });
      else setTimeout(load, 1200);
    }
    if (document.readyState === 'complete') later();
    else window.addEventListener('load', later);
  })();
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1016451274045170&ev=PageView&noscript=1"
/></noscript>
"""

FONTS_URL = ('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700'
             '&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@1'
             '&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Reem+Kufi:wght@600&display=swap')
FONTS = (f'<link rel="preload" as="style" href="{FONTS_URL}" />\n'
         f'<link rel="stylesheet" href="{FONTS_URL}" media="print" onload="this.media=\'all\'" />\n'
         f'<noscript><link rel="stylesheet" href="{FONTS_URL}" /></noscript>')

n = 0
for p in sorted(ROOT.rglob('*.html')):
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith(('scripts/', '.git/')):
        continue
    s = p.read_text()
    a = s.find('<script async src="https://www.googletagmanager.com/gtag/js')
    b = s.find('<!-- End Meta Pixel Code -->')
    if a < 0 or b < 0:
        raise SystemExit(f'{rel}: analytics block not found')
    s = s[:a] + ANALYTICS + s[b:]
    s, k = re.subn(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet"\s*/?>', FONTS.replace('\\', '\\\\'), s)
    if k != 1:
        raise SystemExit(f'{rel}: expected 1 Google Fonts link, found {k}')
    p.write_text(s)
    n += 1
print('pages', n)

css = ROOT / 'assets/mawid.css'
c = css.read_text()
rule = '.page-hero .reveal { opacity: 1; transform: none; transition: none; }'
if rule not in c:
    c = c.replace('.reveal.in { opacity: 1; transform: translateY(0); }',
                  '.reveal.in { opacity: 1; transform: translateY(0); }\n'
                  '/* First-screen content paints without waiting for JS (LCP). */\n' + rule, 1)
    css.write_text(c)
print('css ok' if rule in c else 'css FAIL')
