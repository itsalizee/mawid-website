"""Make every EN/ع toggle a pair of real links to the counterpart page.

Several pages had two <button>s that swapped text in place with JS
(assets/i18n.js), so /pricing/ never linked to /ar/pricing/ and the URL
stayed English. Text is now baked per URL, so the toggle must navigate.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOGGLE = re.compile(r'(<div class="lang-toggle" role="tablist">)(.*?)(</div>)', re.S)

for p in sorted(ROOT.rglob('*.html')):
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith(('scripts/', '.git/')) or 'node_modules' in rel:
        continue
    s = p.read_text()
    if not TOGGLE.search(s):
        continue
    is_ar = rel.startswith('ar/')
    base = rel[3:] if is_ar else rel
    path = '/' if base == 'index.html' else '/' + base[: -len('index.html')]
    en, ar = path, '/ar' + path
    m = TOGGLE.search(s)
    indent = re.search(r'\n([ \t]*)<div class="lang-toggle"', s).group(1) + '  '
    inner = (
        f'\n{indent}<span class="pill"></span>'
        f'\n{indent}<a href="{en}" data-lang="en" aria-pressed="{"false" if is_ar else "true"}">EN</a>'
        f'\n{indent}<a href="{ar}" data-lang="ar" aria-pressed="{"true" if is_ar else "false"}">ع</a>'
        f'\n{indent[:-2]}'
    )
    s = s[: m.start(2)] + inner + s[m.end(2):]
    if len(TOGGLE.findall(s)) != 1:
        raise SystemExit(f'{rel}: expected one toggle')
    p.write_text(s)
    print(f'{rel:28} {en} | {ar}')
