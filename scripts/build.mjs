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
// Usage:  node scripts/build.mjs            (write)
//         node scripts/build.mjs --check    (exit 1 if any page is stale)
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
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

let stale = 0;
const report = [];

for (const file of htmlFiles(ROOT).sort()) {
  const rel = relative(ROOT, file).split(sep).join('/');
  const locale = rel.startsWith('ar/') ? 'ar' : 'en';
  const dict = dicts[DICT_FOR[rel] ?? 'site'];
  const strings = dict[locale] ?? {};
  const src = readFileSync(file, 'utf8');
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

  function walk(node) {
    const attrs = Object.fromEntries((node.attrs ?? []).map((a) => [a.name, a.value]));

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

  edits.sort((a, b) => b[0] - a[0]);
  let out = src;
  for (const [s, e, text] of edits) out = out.slice(0, s) + text + out.slice(e);

  if (out !== src) {
    stale++;
    if (!CHECK) writeFileSync(file, out);
  }
  if (unclosed.size) stale++;
  if (applied || missing.size || unclosed.size) {
    report.push(
      `${rel.padEnd(28)} ${locale}  applied ${String(applied).padStart(3)}` +
        (missing.size ? `  missing: ${[...missing].join(', ')}` : '') +
        (unclosed.size ? `  UNCLOSED: ${[...unclosed].join(', ')}` : '') +
        (out !== src ? (CHECK ? '  STALE' : '  updated') : ''),
    );
  }
}

console.log(report.join('\n'));
if (CHECK && stale) {
  console.error(`\n${stale} page(s) out of date — run: node scripts/build.mjs`);
  process.exit(1);
}
console.log(`\n${CHECK ? 'check' : 'build'} done; ${stale} page(s) ${CHECK ? 'stale' : 'written'}.`);
