"""One-off structural edits to product/index.html and ar/product/index.html.

- Drops the AI-insights and Multi-location tabs + panels (not in the app)
  and renumbers the Bilingual tab to 04.
- Fixes the calendar visual: May 2026 is Dhu al-Qadah -> Dhu al-Hijjah
  1447 (Umm al-Qura: 1 Dhu al-Hijjah = 18 May, Eid al-Adha = 27 May), so
  the Hijri day numbers from 17 May on, the month line and the holiday
  cells were wrong. Legend localized on the Arabic page.
- Replaces the WhatsApp visual (automated confirmation, reschedule link,
  scheduled reminder - none of which ship yet) with the real flow: a
  customer asks in chat, the business replies with its booking link.
- Footer "Payments" link (no such tab) -> Customers; tab hash list fixed
  ('payments' -> 'customers', removed tabs dropped).
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

CAL_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/>'
            '<line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>'
            '<line x1="3" y1="10" x2="21" y2="10"/></svg>')

WA = {
    'en': dict(
        q='Hi! Any time Friday morning for colour + cut?', t1='10:42 AM',
        a='Hi! Pick any free slot here 👇', t2='10:42 AM ✓✓',
        label='BOOK ONLINE', title='Salon Rasha · pick a time',
        done='Done, booked Friday 10:00 🌸', t3='10:44 AM',
    ),
    'ar': dict(
        q='هلا، فيه موعد الجمعة الصبح لصبغة وقص؟', t1='١٠:٤٢ ص',
        a='أهلاً! تقدرون تختارون الوقت المناسب من هنا 👇', t2='١٠:٤٢ ص ✓✓',
        label='الحجز أونلاين', title='صالون رشا · اختيار الموعد',
        done='تم، حجزت الجمعة ١٠:٠٠ 🌸', t3='١٠:٤٤ ص',
    ),
}

LEGEND = {
    'en': ('Today', 'Friday AM closed', 'Eid closure'),
    'ar': ('اليوم', 'صباح الجمعة مغلق', 'إغلاق العيد'),
}

# Gregorian day (May 2026 + leading/trailing days) -> Umm al-Qura day.
# Verified with @umalqura/core: 17 May = 30 Dhu al-Qadah, 18 May = 1 Dhu al-Hijjah.
def hijri_for(row_index):
    # Grid starts Sun 26 Apr = 9 Dhu al-Qadah; Dhu al-Qadah 1447 has 30 days.
    n = 9 + row_index
    return n if n <= 30 else n - 30

EID_DAYS = {27, 28}  # 10-11 Dhu al-Hijjah


def sub_once(s, old, new, label):
    if s.count(old) != 1:
        raise SystemExit(f'{label}: expected 1 match, found {s.count(old)}')
    return s.replace(old, new)


def process(rel, lang):
    p = ROOT / rel
    s = p.read_text()

    # --- tabs ---
    s = re.sub(r'\s*<button type="button" class="pp-tab" data-tab="(ai|locations)" role="tab">.*?</button>',
               '', s, flags=re.S)
    s = sub_once(s, '<span class="pp-tab-num">06</span>', '<span class="pp-tab-num">04</span>', 'tab num')

    # --- panels ---
    start = s.index('    <!-- Panel 04: AI insights -->')
    end = s.index('    <!-- Panel 06: Localization -->')
    s = s[:start] + s[end:]
    s = sub_once(s, '<!-- Panel 06: Localization -->', '<!-- Panel 04: Localization -->', 'panel comment')

    # --- calendar ---
    s = sub_once(s, '<div class="pp-cal-month-h">شوال — ذو القعدة ١٤٤٧</div>',
                 '<div class="pp-cal-month-h">ذو القعدة — ذو الحجة ١٤٤٧</div>', 'hijri month')
    grid_start = s.index('<div class="pp-cal-grid">')
    grid_end = s.index('</div>\n            <div class="pp-cal-legend">', grid_start)
    grid = s[grid_start:grid_end]
    cells = list(re.finditer(r'<div class="pp-cal-day([^"]*)">(\d+)<div class="pp-cal-hijri">\d+</div></div>', grid))
    if len(cells) != 42:
        raise SystemExit(f'{rel}: expected 42 calendar cells, found {len(cells)}')
    out, last = [], 0
    for i, m in enumerate(cells):
        classes = m.group(1).replace(' holiday', '')
        day = int(m.group(2))
        in_may = 5 <= i <= 35
        if in_may and day in EID_DAYS:
            classes += ' holiday'
        out.append(grid[last:m.start()])
        out.append(f'<div class="pp-cal-day{classes}">{day}<div class="pp-cal-hijri">{hijri_for(i)}</div></div>')
        last = m.end()
    out.append(grid[last:])
    s = s[:grid_start] + ''.join(out) + s[grid_end:]

    today, fri, hol = LEGEND[lang]
    s = sub_once(s, 'var(--ink);"></span> Today</div>', f'var(--ink);"></span> {today}</div>', 'legend today')
    s = sub_once(s, '#C49B5C;"></span> Friday AM blocked</div>', f'#C49B5C;"></span> {fri}</div>', 'legend fri')
    s = sub_once(s, '0.4);"></span> Holiday</div>', f'0.4);"></span> {hol}</div>', 'legend hol')

    # --- WhatsApp visual ---
    w = WA[lang]
    wa_start = s.index('<div class="pp-wa">')
    wa_end = s.index('</div>\n        </div>\n      </div>\n    </div>', wa_start)
    new_wa = (
        '<div class="pp-wa">\n'
        f'            <div class="pp-wa-msg">{w["q"]}<span class="pp-wa-time">{w["t1"]}</span></div>\n'
        f'            <div class="pp-wa-msg out">{w["a"]}<span class="pp-wa-time">{w["t2"]}</span></div>\n'
        '            <div class="pp-wa-pay">\n'
        f'              <div style="font-size: 11px; color: var(--muted); font-family: var(--mono);">{w["label"]}</div>\n'
        f'              <div style="font-weight: 600; font-size: 14px; margin-block-start: 4px;">{w["title"]}</div>\n'
        '              <div class="pp-wa-pay-bar" dir="ltr">\n'
        f'                {CAL_ICON}\n'
        '                mawid.ai/book/salon-rasha\n'
        '              </div>\n'
        '            </div>\n'
        f'            <div class="pp-wa-msg">{w["done"]}<span class="pp-wa-time">{w["t3"]}</span></div>\n'
        '          '
    )
    s = s[:wa_start] + new_wa + s[wa_end:]

    # --- footer + tab routing ---
    prefix = '/ar' if lang == 'ar' else ''
    s = sub_once(s, f'href="{prefix}/product/#payments" data-i18n="foot.product.payments"',
                 f'href="{prefix}/product/#customers" data-i18n="foot.product.customers"', 'footer link')
    s = sub_once(s, "const validTabs = ['bookings', 'payments', 'whatsapp', 'ai', 'locations', 'localization'];",
                 "const validTabs = ['bookings', 'customers', 'whatsapp', 'localization'];", 'validTabs')

    p.write_text(s)
    print(rel, 'ok')


process('product/index.html', 'en')
process('ar/product/index.html', 'ar')
