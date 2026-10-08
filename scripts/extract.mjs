// Extract the current inner HTML of every data-i18n element on a page into
// {key: html}. Used once to seed i18n/product.json from the hand-written pages.
import { readFileSync } from 'node:fs';
import { parse } from 'parse5';
export function extract(file) {
  const src = readFileSync(file, 'utf8');
  const doc = parse(src, { sourceCodeLocationInfo: true });
  const out = {};
  (function walk(n) {
    const key = n.attrs?.find((a) => a.name === 'data-i18n')?.value;
    const loc = n.sourceCodeLocation;
    if (key && loc?.startTag && loc?.endTag) { out[key] = src.slice(loc.startTag.endOffset, loc.endTag.startOffset).trim(); return; }
    for (const c of n.childNodes ?? []) walk(c);
  })(doc);
  return out;
}
if (process.argv[2]) console.log(JSON.stringify(extract(process.argv[2]), null, 2));
