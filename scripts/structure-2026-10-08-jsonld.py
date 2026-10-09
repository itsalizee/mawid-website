"""Homepage JSON-LD (EN + AR): accurate Organization + SoftwareApplication.

Drops "AI-powered", "WhatsApp-native" and the iOS/Android claim (web app
only), names the real operating company, and lists prices in USD and SAR
(see lib/billing/pricing.ts in the app repo). Also removes the ignored
meta keywords tag.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRICES = {'Starter': (80, 299), 'Professional': (140, 529), 'Studio': (180, 679)}

DESC = {
    'en': 'Arabic-first online booking platform for salons, clinics, spas and restaurants in Saudi Arabia, UAE, Qatar and Kuwait.',
    'ar': 'منصة حجز مواعيد أونلاين عربية أولاً للصالونات والعيادات والسبا والمطاعم في السعودية والإمارات وقطر والكويت.',
}
FEATURES = {
    'en': ['Bilingual Arabic/English booking page', 'Hijri and Gregorian dates', 'Prayer-time-aware time slots',
           'Friday and holiday closures', 'Customer list with visit history, no-shows and notes',
           'WhatsApp chat button on every booking page', 'Email alert for every booking',
           'Restaurant mode with party size and table capacity', '7-day free trial'],
    'ar': ['صفحة حجز بالعربية والإنجليزية', 'التاريخ الهجري والميلادي', 'أوقات حجز تراعي أوقات الصلاة',
           'إغلاق الجمعة والإجازات', 'سجل عملاء بالزيارات ومرات الغياب والملاحظات',
           'زر واتساب في كل صفحة حجز', 'تنبيه بالبريد مع كل حجز',
           'نمط المطاعم مع عدد الضيوف وسعة الطاولات', 'تجربة مجانية ٧ أيام'],
}


def org(lang):
    return {
        '@context': 'https://schema.org', '@type': 'Organization', '@id': 'https://mawid.ai/#org',
        'name': 'Mawid', 'alternateName': 'موعد', 'url': 'https://mawid.ai/', 'logo': 'https://mawid.ai/logo.png',
        'description': DESC[lang],
        'areaServed': [{'@type': 'Country', 'name': n} for n in ('Saudi Arabia', 'United Arab Emirates', 'Qatar', 'Kuwait')],
        'parentOrganization': {
            '@type': 'Organization', 'name': 'Diyar Holdings LLC',
            'address': {'@type': 'PostalAddress', 'streetAddress': '30 N Gould Street, Suite R', 'addressLocality': 'Sheridan',
                        'addressRegion': 'WY', 'postalCode': '82801', 'addressCountry': 'US'},
        },
        'contactPoint': {'@type': 'ContactPoint', 'email': 'hello@mawid.ai', 'contactType': 'customer support',
                         'availableLanguage': ['English', 'Arabic']},
    }


def app(lang):
    offers = []
    for name, (usd, sar) in PRICES.items():
        for price, cur in ((usd, 'USD'), (sar, 'SAR')):
            offers.append({'@type': 'Offer', 'name': name, 'price': str(price), 'priceCurrency': cur,
                           'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': str(price),
                                                  'priceCurrency': cur, 'unitText': 'MONTH'}})
    return {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Mawid',
        'applicationCategory': 'BusinessApplication', 'applicationSubCategory': 'Booking & scheduling',
        'operatingSystem': 'Web', 'url': 'https://mawid.ai/' if lang == 'en' else 'https://mawid.ai/ar/',
        'inLanguage': lang, 'description': DESC[lang], 'publisher': {'@id': 'https://mawid.ai/#org'},
        'offers': offers, 'featureList': FEATURES[lang],
    }


def block(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'


for rel, lang in (('index.html', 'en'), ('ar/index.html', 'ar')):
    p = ROOT / rel
    s = p.read_text()
    scripts = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
    by_type = {}
    for m in scripts:
        t = re.search(r'"@type":\s*"([A-Za-z]+)"', m.group(0)).group(1)
        by_type[t] = m
    for t, build in (('SoftwareApplication', app), ('Organization', org)):  # later one first
        m = by_type[t]
        s = s[:m.start()] + block(build(lang)) + s[m.end():]
        by_type = {k: v for k, v in by_type.items()}
        # recompute offsets after the splice
        scripts = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
        by_type = {re.search(r'"@type":\s*"([A-Za-z]+)"', x.group(0)).group(1): x for x in scripts}
    s = re.sub(r'<meta name="keywords"[^>]*>\n', '', s)
    p.write_text(s)
    print(rel, 'ok')
