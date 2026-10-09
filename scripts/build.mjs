// Mawid site build: bakes translated text into every page's HTML.
//
// Why: the site used to ship English in the HTML and swap to Arabic with
// JavaScript after load. Google (and WhatsApp/LinkedIn previews, Bing, AI
// search) saw a mostly-English /ar/ page, and the swap delayed the main
// content by seconds on phones. Now each page's text is in its HTML.
//
// Source of truth for copy:
//   i18n/home.json     →  index.html, ar/index.html
//   i18n/product.json  →  product/index.html, ar/product/index.html
//                         (merged over site.json for shared header/footer)
//   i18n/site.json     →  every other page
// Pages under ar/ get the "ar" strings, everything else "en".
//
// Elements opt in with data-i18n="key" (replaces inner HTML),
// data-i18n-placeholder="key" and data-i18n-attr="attr:key" (attributes).
// Text is spliced in at exact source offsets, so nothing else in the file
// changes — no reformatting, no reordering. Re-running is idempotent.
//
// Also generated here, so they can't drift from the pages:
//   - FAQPage JSON-LD in <script type="application/ld+json" data-faq="prefix">,
//     rebuilt from the page's own <prefix>.qN / <prefix>.aN strings
//   - each page's <title>, description, canonical, hreflang and Open Graph /
//     Twitter tags, from i18n/meta.json (one entry per page, EN + AR)
//   - sitemap.xml, from each indexable page's canonical + hreflang links
//
// Usage:  node scripts/build.mjs            (write)
//         node scripts/build.mjs --check    (exit 1 if any page is stale)
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'parse5';

const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const CHECK = process.argv.includes('--check');
const SKIP_DIRS = new Set(['node_modules', '.git', '.vercel', 'scripts', 'i18n']);

const dicts = {
  home: JSON.parse(readFileSync(join(ROOT, 'i18n/home.json'), 'utf8')),
  site: JSON.parse(readFileSync(join(ROOT, 'i18n/site.json'), 'utf8')),
};
const product = JSON.parse(readFileSync(join(ROOT, 'i18n/product.json'), 'utf8'));
dicts.product = {
  en: { ...dicts.site.en, ...product.en },
  ar: { ...dicts.site.ar, ...product.ar },
};
const DICT_FOR = {
  'index.html': 'home',
  'ar/index.html': 'home',
  'product/index.html': 'product',
  'ar/product/index.html': 'product',
};

function htmlFiles(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) {
      if (!SKIP_DIRS.has(name)) out.push(...htmlFiles(p));
    } else if (name.endsWith('.html')) out.push(p);
  }
  return out;
}

const escAttr = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
const escText = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ---------- <head>: title, description, canonical, hreflang, social ----------
const meta = JSON.parse(readFileSync(join(ROOT, 'i18n/meta.json'), 'utf8'));
const SITE = 'https://mawid.ai';
// Arabic legal pages keep English bodies for now; they're noindex, so no
// hreflang pairs point at them (or from their English twins).
const NO_HREFLANG = new Set(['/privacy/', '/terms/']);

function applyHead(src, rel, locale) {
  const base = rel.replace(/^ar\//, '');
  const path = base === 'index.html' ? '/' : '/' + base.replace(/index\.html$/, '');
  const m = meta[path]?.[locale];
  if (!m) return src;
  const bodyAt = src.indexOf('<body');
  let head = src.slice(0, bodyAt);
  const url = SITE + (locale === 'ar' ? '/ar' : '') + path;
  const enUrl = SITE + path;

  head = head.replace(/<title>[\s\S]*?<\/title>/, `<title>${escText(m.title)}</title>`);
  const desc = `<meta name="description" content="${escAttr(m.description)}" />`;
  head = /<meta name="description"[^>]*>/.test(head)
    ? head.replace(/<meta name="description"[^>]*>/, desc)
    : head.replace(/(<title>[\s\S]*?<\/title>)/, `$1\n${desc}`);

  head = head.replace(/[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*\/?>\n?/g, '');
  head = head.replace(/[ \t]*<meta (?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>\n?/g, '');
  const alts = NO_HREFLANG.has(path) ? [] : [['en', enUrl], ['ar', SITE + '/ar' + path], ['x-default', enUrl]];
  const img = SITE + (locale === 'ar' ? '/og-image-ar.png' : '/og-image.png');
  const alt = locale === 'ar' ? 'موعد · نظام حجز مواعيد للخليج' : 'Mawid · Booking, built for the Gulf';
  const tags = [
    ['property', 'og:type', 'website'],
    ['property', 'og:site_name', locale === 'ar' ? 'موعد' : 'Mawid'],
    ['property', 'og:title', m.title],
    ['property', 'og:description', m.description],
    ['property', 'og:url', url],
    ['property', 'og:image', img],
    ['property', 'og:image:width', '1200'],
    ['property', 'og:image:height', '630'],
    ['property', 'og:image:alt', alt],
    ['property', 'og:locale', locale === 'ar' ? 'ar_SA' : 'en_US'],
    ['property', 'og:locale:alternate', locale === 'ar' ? 'en_US' : 'ar_SA'],
    ['name', 'twitter:card', 'summary_large_image'],
    ['name', 'twitter:title', m.title],
    ['name', 'twitter:description', m.description],
    ['name', 'twitter:image', img],
    ['name', 'twitter:image:alt', alt],
  ];
  const block =
    `<link rel="canonical" href="${url}" />\n` +
    alts.map(([l, h]) => `<link rel="alternate" hreflang="${l}" href="${h}" />\n`).join('') +
    tags.map(([k, n, v]) => `<meta ${k}="${n}" content="${escAttr(v)}" />\n`).join('');
  head = /<link rel="canonical"[^>]*>\n?/.test(head)
    ? head.replace(/<link rel="canonical"[^>]*>\n?/, block)
    : head.replace(/(<meta name="description"[^>]*>\n?)/, `$1${block}`);
  return head + src.slice(bodyAt);
}

let stale = 0;
const report = [];

for (const file of htmlFiles(ROOT).sort()) {
  const rel = relative(ROOT, file).split(sep).join('/');
  const locale = rel.startsWith('ar/') ? 'ar' : 'en';
  const dict = dicts[DICT_FOR[rel] ?? 'site'];
  const strings = dict[locale] ?? {};
  const original = readFileSync(file, 'utf8');
  const src = applyHead(original, rel, locale);
  const doc = parse(src, { sourceCodeLocationInfo: true });
  const edits = [];
  const missing = new Set();
  const unclosed = new Set();
  let applied = 0;

  const attrLoc = (node, name) => node.sourceCodeLocation?.attrs?.[name];

  function setAttr(node, attr, value) {
    const loc = attrLoc(node, attr);
    if (!loc) return; // attribute absent on this element; don't invent it
    edits.push([loc.startOffset, loc.endOffset, `${attr}="${escAttr(value)}"`]);
    applied++;
  }

  const onPage = new Set();
  const faqScripts = [];

  function walk(node) {
    const attrs = Object.fromEntries((node.attrs ?? []).map((a) => [a.name, a.value]));
    if (node.nodeName === 'script' && attrs['data-faq']) faqScripts.push([node, attrs['data-faq']]);
    if (attrs['data-i18n']) onPage.add(attrs['data-i18n']);

    if (attrs['data-i18n-placeholder']) {
      const v = strings[attrs['data-i18n-placeholder']];
      if (v === undefined) missing.add(attrs['data-i18n-placeholder']);
      else setAttr(node, 'placeholder', v);
    }
    if (attrs['data-i18n-attr']) {
      for (const pair of attrs['data-i18n-attr'].split(',')) {
        const [a, k] = pair.split(':').map((x) => x.trim());
        if (!a || !k) continue;
        const v = strings[k];
        if (v === undefined) missing.add(k);
        else setAttr(node, a, v);
      }
    }
    if (attrs['data-i18n']) {
      const key = attrs['data-i18n'];
      const v = strings[key];
      const loc = node.sourceCodeLocation;
      if (v === undefined) missing.add(key);
      else if (loc?.startTag && loc?.endTag) {
        edits.push([loc.startTag.endOffset, loc.endTag.startOffset, String(v)]);
        applied++;
        return; // the value replaces the whole subtree
      } else unclosed.add(key); // malformed source (e.g. <a>…</div>) — fix the HTML
    }
    const kids = node.nodeName === 'template' ? node.content?.childNodes : node.childNodes;
    for (const c of kids ?? []) walk(c);
  }
  walk(doc);

  for (const [node, prefix] of faqScripts) {
    const loc = node.sourceCodeLocation;
    const plain = (h) => String(h).replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
    const mainEntity = [];
    for (let n = 1; onPage.has(`${prefix}.q${n}`); n++) {
      const q = strings[`${prefix}.q${n}`];
      const a = strings[`${prefix}.a${n}`];
      if (q === undefined || a === undefined) break;
      mainEntity.push({ '@type': 'Question', name: plain(q), acceptedAnswer: { '@type': 'Answer', text: plain(a) } });
    }
    const json = JSON.stringify({ '@context': 'https://schema.org', '@type': 'FAQPage', inLanguage: locale, mainEntity }, null, 2);
    edits.push([loc.startTag.endOffset, loc.endTag.startOffset, `\n${json}\n`]);
  }

  edits.sort((a, b) => b[0] - a[0]);
  let out = src;
  for (const [s, e, text] of edits) out = out.slice(0, s) + text + out.slice(e);

  if (out !== original) {
    stale++;
    if (!CHECK) writeFileSync(file, out);
  }
  if (unclosed.size) stale++;
  if (applied || missing.size || unclosed.size) {
    report.push(
      `${rel.padEnd(28)} ${locale}  applied ${String(applied).padStart(3)}` +
        (missing.size ? `  missing: ${[...missing].join(', ')}` : '') +
        (unclosed.size ? `  UNCLOSED: ${[...unclosed].join(', ')}` : '') +
        (out !== original ? (CHECK ? '  STALE' : '  updated') : ''),
    );
  }
}

// ---------- sitemap.xml ----------
// Every page with a canonical URL and no noindex, plus its hreflang
// alternates. lastmod = last commit touching the file (today if modified).
const today = new Date().toISOString().slice(0, 10);
function lastmod(file) {
  try {
    const dirty = execFileSync('git', ['status', '--porcelain', '--', file], { cwd: ROOT }).toString().trim();
    if (dirty) return today;
    return execFileSync('git', ['log', '-1', '--format=%cs', '--', file], { cwd: ROOT }).toString().trim() || today;
  } catch {
    return today;
  }
}
const entries = [];
for (const file of htmlFiles(ROOT).sort()) {
  const src = readFileSync(file, 'utf8');
  const head = src.slice(0, src.indexOf('<body'));
  const canonical = head.match(/<link rel="canonical" href="([^"]+)"/)?.[1];
  const robots = head.match(/<meta name="robots" content="([^"]+)"/)?.[1] ?? '';
  if (!canonical || /noindex/.test(robots)) continue;
  const alts = [...head.matchAll(/<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"/g)].map((m) => [m[1], m[2]]);
  entries.push({ loc: canonical, lastmod: lastmod(relative(ROOT, file)), alts });
}
const order = (u) => {
  const p = new URL(u).pathname.replace(/^\/ar/, '') || '/';
  const rank = ['/', '/product/', '/pricing/', '/restaurants/', '/clinics/', '/about/', '/contact/', '/refund/', '/privacy/', '/terms/'];
  const i = rank.indexOf(p);
  return (i === -1 ? 99 : i) * 2 + (u.includes('/ar/') ? 1 : 0);
};
entries.sort((a, b) => order(a.loc) - order(b.loc));
const sitemap =
  '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<!-- Generated by scripts/build.mjs — do not edit by hand. -->\n' +
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
  entries
    .map(
      (e) =>
        `  <url>\n    <loc>${e.loc}</loc>\n    <lastmod>${e.lastmod}</lastmod>\n` +
        e.alts.map(([l, h]) => `    <xhtml:link rel="alternate" hreflang="${l}" href="${h}" />\n`).join('') +
        '  </url>\n',
    )
    .join('') +
  '</urlset>\n';
const smPath = join(ROOT, 'sitemap.xml');
const smOld = existsSync(smPath) ? readFileSync(smPath, 'utf8') : '';
// lastmod dates alone shouldn't make --check fail on a clean tree
const smKey = (x) => x.replace(/<lastmod>[^<]*<\/lastmod>/g, '');
if (smKey(smOld) !== smKey(sitemap)) {
  stale++;
  report.push(`sitemap.xml                  ${entries.length} urls${CHECK ? '  STALE' : '  updated'}`);
}
if (!CHECK && smOld !== sitemap) writeFileSync(smPath, sitemap);

console.log(report.join('\n'));
if (CHECK && stale) {
  console.error(`\n${stale} page(s) out of date — run: node scripts/build.mjs`);
  process.exit(1);
}
console.log(`\n${CHECK ? 'check' : 'build'} done; ${stale} page(s) ${CHECK ? 'stale' : 'written'}.`);
