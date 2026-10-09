"""Arabic privacy/terms pages: Arabic head, a governing-language note, noindex.

The section bodies are still English (legal text needs a proper legal
translation). Until then the Arabic URLs exist for navigation but stay out
of Google's index, and say clearly that the English version governs.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
site = json.loads((ROOT / 'i18n/site.json').read_text())
NOTE = site['ar']['legal.ar_note']

PAGES = {
    'ar/privacy/index.html': (
        'Privacy Policy · Mawid', 'سياسة الخصوصية · موعد',
        'How Mawid handles personal information for our customers, their staff, and people who book through their booking pages. KSA PDPL, UAE PDP Law, and GDPR-aligned.',
        'كيف تتعامل موعد مع المعلومات الشخصية لعملائنا وموظفيهم ومن يحجز عبر صفحات الحجز. النسخة الإنجليزية هي المعتمدة.',
        'privacy.updated',
    ),
    'ar/terms/index.html': (
        'Terms of Service · Mawid', 'شروط الخدمة · موعد',
        'The agreement between you and Diyar Holdings LLC governing use of Mawid. Wyoming governing law.',
        'الاتفاقية بينكم وبين شركة ديار القابضة التي تحكم استخدام موعد. النسخة الإنجليزية هي المعتمدة.',
        'terms.updated',
    ),
}


def once(s, old, new, label):
    if s.count(old) != 1:
        raise SystemExit(f'{label}: expected 1, found {s.count(old)}')
    return s.replace(old, new)


for rel, (t_en, t_ar, d_en, d_ar, updated_key) in PAGES.items():
    p = ROOT / rel
    s = p.read_text()
    s = once(s, f'<title>{t_en}</title>', f'<title>{t_ar}</title>', rel + ' title')
    s = once(s, f'<meta name="description" content="{d_en}" />', f'<meta name="description" content="{d_ar}" />', rel + ' desc')
    s = once(s, '<meta name="robots" content="index, follow" />', '<meta name="robots" content="noindex, follow" />', rel + ' robots')
    for prop in ('og:title', 'twitter:title'):
        s = s.replace(f'<meta property="{prop}" content="{t_en}" />', f'<meta property="{prop}" content="{t_ar}" />')
        s = s.replace(f'<meta name="{prop}" content="{t_en}" />', f'<meta name="{prop}" content="{t_ar}" />')
    marker = f'data-i18n="{updated_key}">'
    i = s.index(marker)
    end = s.index('</p>', i) + len('</p>')
    s = s[:end] + f'\n    <p class="legal-ar-note" data-i18n="legal.ar_note" style="margin: 16px auto 0; max-width: 60ch; font-size: 14px; color: var(--ink-mid); text-align: center;">{NOTE}</p>' + s[end:]
    p.write_text(s)
    print(rel, 'ok')
