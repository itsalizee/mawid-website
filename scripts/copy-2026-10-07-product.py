"""One-off revision for i18n/product.json (product page, EN + AR).

Removes the AI-insights and Multi-location tabs (neither exists), rewrites
the WhatsApp tab to what ships today (one-tap chat + shareable links;
automated messages are "coming"), corrects the Customers tab (VIP is a
manual flag + tags, not automatic segmentation; no stylist-preference
ranking) and the calendar claims (Umm al-Qura everywhere; holidays are
closures you add). Arabic is gender-neutral throughout.
"""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / 'i18n' / 'product.json'
d = json.loads(P.read_text())

S = {
    'prod.title': (
        'Built for how Gulf businesses actually work.',
        'مبني لطريقة عمل الأعمال في الخليج فعلاً.',
    ),
    'prod.lede': (
        'Four product surfaces, built for the GCC from day one. Not retrofitted. Not translated. Pick one to see what\'s inside.',
        'أربعة أجزاء أساسية مبنية للخليج من اليوم الأول. لم تُكيَّف ولم تُترجم. اختاروا أحدها لمعرفة ما فيه.',
    ),
    'prod.stat3': (
        'Salon · restaurant · clinic booking modes',
        'أنماط حجز للصالون والمطعم والعيادة',
    ),
    # ---- bookings ----
    'prod.bookings.lede': (
        'Hijri and Gregorian dates side by side on your booking page. Friday mornings closed by default for KSA, prayer breaks blocked automatically, and Eid or Ramadan hours added as closures in seconds.',
        'التاريخ الهجري والميلادي جنباً إلى جنب في صفحة الحجز. صباح الجمعة مغلق افتراضياً في السعودية، وأوقات الصلاة محجوبة تلقائياً، وإجازات العيد ودوام رمضان تُضاف في ثوانٍ.',
    ),
    'prod.bookings.s1.t': ('Hijri + Gregorian dates', 'التاريخ الهجري والميلادي'),
    'prod.bookings.s1.b': (
        'Every date on the booking page shows in both calendars (Umm al-Qura for Hijri), so customers read whichever they\'re used to.',
        'كل تاريخ في صفحة الحجز يظهر بالتقويمين (أم القرى للهجري)، فيقرأ كل عميل التقويم الذي اعتاد عليه.',
    ),
    'prod.bookings.s2.b': (
        'Mawid checks staff schedules, prayer times, closures, buffer times and existing bookings, so customers only ever see slots that are actually free.',
        'موعد يراجع جداول الموظفين وأوقات الصلاة والإغلاقات وأوقات التجهيز والحجوزات القائمة، فلا يرى العملاء إلا الأوقات المتاحة فعلاً.',
    ),
    'prod.bookings.s3.t': ('Pick a specialist, or anyone free', 'اختيار المختص أو أول متاح'),
    'prod.bookings.s3.b': (
        'Customers choose a specific team member or "any available". You decide who offers which service — colourists for colour, keratin specialists for keratin.',
        'يختار العملاء عضواً محدداً من الفريق أو "أي متاح". وأنتم تحددون من يقدّم كل خدمة — مختص الصبغة للصبغة، ومختص الكيراتين للكيراتين.',
    ),
    'prod.bookings.s4.b': (
        'Per-service buffer minutes. Colour and cut needs 15 minutes of clean-up, Brazilian keratin needs 20. Set it once and it applies automatically.',
        'دقائق تجهيز لكل خدمة. الصبغة والقص تحتاج ١٥ دقيقة، والكيراتين البرازيلي ٢٠. تُضبط مرة واحدة وتُطبَّق تلقائياً.',
    ),
    # ---- customers ----
    'prod.customers.lede': (
        'Visit history, no-show count, last visit and notes for everyone who books with you. Your team greets returning customers like regulars, because the system remembers.',
        'سجل الزيارات، وعدد مرات الغياب، وآخر زيارة، والملاحظات لكل من يحجز لديكم. فريقكم يستقبل العملاء العائدين كأنهم يعرفونهم، لأن النظام يتذكر.',
    ),
    'prod.customers.s1.b': (
        'Every appointment and service, searchable by name or phone number. New customers are added automatically the first time they book.',
        'كل موعد وخدمة، مع البحث بالاسم أو رقم الجوال. العملاء الجدد يُضافون تلقائياً عند أول حجز.',
    ),
    'prod.customers.s2.t': ('VIP flag and tags', 'علامة VIP والوسوم'),
    'prod.customers.s2.b': (
        'Mark your VIPs, add your own tags like "bridal" or "regular", and filter the list in one tap.',
        'ميّزوا عملاء VIP، وأضيفوا وسومكم الخاصة مثل "عروس" أو "منتظم"، وصفّوا القائمة بضغطة واحدة.',
    ),
    'prod.customers.s3.t': ('Visits and no-shows at a glance', 'الزيارات والغياب بنظرة واحدة'),
    'prod.customers.s3.b': (
        'See how often each customer comes, when they last visited, and how many times they didn\'t show — before you confirm their next booking.',
        'اعرفوا كم مرة يزوركم كل عميل، ومتى كانت آخر زيارة، وكم مرة لم يحضر — قبل تأكيد حجزه التالي.',
    ),
    'prod.customers.s4.t': ('Notes that outlast staff turnover', 'ملاحظات تبقى حتى لو تغيّر الفريق'),
    'prod.customers.s4.b': (
        'Free-form notes on every customer — colour formulas, allergies, preferences. They stay with the customer, not in someone\'s head.',
        'ملاحظات حرة لكل عميل — تركيبات الصبغة، والحساسيات، والتفضيلات. تبقى مع العميل، لا في ذاكرة أحد.',
    ),
    'prod.customers.c1s': ('12 visits · last visit 3 days ago', '١٢ زيارة · آخرها قبل ٣ أيام'),
    'prod.customers.tagReg': (None, 'منتظم'),
    'prod.customers.tagLapsed': ('Bridal', 'عروس'),
    'prod.customers.more': (None, '+ ٢٬٨٣٦ آخرون'),
    # ---- WhatsApp ----
    'prod.wa.title': (
        'Where bookings actually start — <span class="it">WhatsApp.</span>',
        'حيث تبدأ الحجوزات فعلاً — <span class="it">واتساب.</span>',
    ),
    'prod.wa.lede': (
        'Your booking link works inside any chat, and every booking page has a one-tap WhatsApp button. Automated confirmations and reminders are coming next.',
        'رابط الحجز يعمل داخل أي محادثة، وكل صفحة حجز فيها زر واتساب بضغطة واحدة. التأكيدات والتذكيرات التلقائية قادمة قريباً.',
    ),
    'prod.wa.s1.t': ('One-tap chat from your booking page', 'محادثة بضغطة من صفحة الحجز'),
    'prod.wa.s1.b': (
        'Add your WhatsApp number once. Customers with a question tap the button and land in a chat with you, with a message already typed.',
        'أضيفوا رقم الواتساب مرة واحدة. العميل الذي لديه استفسار يضغط الزر فتُفتح محادثة معكم ورسالته جاهزة.',
    ),
    'prod.wa.s2.t': ('Send your link in any chat', 'أرسلوا الرابط في أي محادثة'),
    'prod.wa.s2.b': (
        'When someone asks "any time Friday?", reply with your booking link. They pick the slot themselves in under a minute — no back-and-forth.',
        'عندما يسأل أحدهم "فيه موعد الجمعة؟"، ردّوا برابط الحجز. يختار الوقت بنفسه في أقل من دقيقة — بدون أخذ ورد.',
    ),
    'prod.wa.s3.t': ('A link for every channel', 'رابط لكل قناة'),
    'prod.wa.s3.b': (
        'Your Share tab has ready-made links for Instagram bio, stories and WhatsApp, a QR code for the counter, and a suggested caption.',
        'تبويب المشاركة فيه روابط جاهزة لسيرة إنستغرام والستوريز وواتساب، ورمز QR للاستقبال، ونص مقترح للنشر.',
    ),
    'prod.wa.s4.t': ('Automated confirmations — coming soon', 'تأكيدات تلقائية — قريباً'),
    'prod.wa.s4.b': (
        'WhatsApp confirmations and reminders sent from Mawid are in progress and will roll out to every plan. Until then, you get an email for every booking.',
        'التأكيدات والتذكيرات عبر واتساب من موعد قيد التطوير وستصل لكل الخطط. وحتى ذلك الحين، تصلكم رسالة بريد مع كل حجز.',
    ),
    # ---- bilingual ----
    'prod.l10n.lede': (
        'Each person on your team picks Arabic or English for their own screen. Customers see the booking page in their language, and Mawid remembers which one they used.',
        'كل عضو في الفريق يختار العربية أو الإنجليزية لشاشته. والعملاء يرون صفحة الحجز بلغتهم، وموعد يتذكر اللغة التي استخدموها.',
    ),
    'prod.l10n.s2.t': ('Each customer\'s language, remembered', 'لغة كل عميل محفوظة'),
    'prod.l10n.s2.b': (
        'Book in Arabic and Mawid saves Arabic on that customer\'s profile; book in English and it saves English. Same business, same booking flow.',
        'من يحجز بالعربية تُحفظ العربية في ملفه، ومن يحجز بالإنجليزية تُحفظ الإنجليزية. النشاط نفسه وطريقة الحجز نفسها.',
    ),
    'prod.l10n.s3.b': (
        'Numbers display as 1, 2, 3 even in the Arabic interface — matching how prices are written on receipts and screens across the Gulf.',
        'الأرقام تظهر 1، 2، 3 حتى في الواجهة العربية — كما تُكتب الأسعار على الإيصالات والشاشات في الخليج.',
    ),
    'prod.l10n.s4.b': (
        'IBM Plex Sans Arabic throughout, with spacing tuned for Arabic script. It reads like it was designed in Arabic, not translated into it.',
        'خط IBM Plex Sans Arabic في كل الشاشات، مع تباعد مضبوط للحرف العربي. تبدو مصممة بالعربية، لا مترجمة إليها.',
    ),
    # ---- gender-neutral leftovers ----
    'prod.tab.customers': (None, 'العملاء'),
    'prod.customers.head': (None, 'العملاء'),
    'prod.customers.title': (
        'Every customer who\'s ever walked in — <span class="it">searchable.</span>',
        'كل عميل زاركم يوماً — <span class="it">قابل للبحث.</span>',
    ),
    'prod.customers.s1.t': (None, 'سجل زيارات كامل لكل عميل'),
    'prod.cta.kicker': (None, 'شاهدوه يعمل'),
    'prod.cta.sample_post': (None, '— تماماً كما يراها عملاؤكم.'),
    # ---- CTA ----
    'prod.cta.title': (
        'Want to see Mawid running at your business?',
        'تريدون رؤية موعد يعمل في نشاطكم؟',
    ),
    'prod.cta.lede': (
        'Start a 7-day free trial and set up your services, team and hours in minutes — or talk to us and we\'ll do it with you.',
        'ابدؤوا تجربة مجانية ٧ أيام وجهّزوا خدماتكم وفريقكم وساعات العمل في دقائق — أو تواصلوا معنا وسنجهّزه معكم.',
    ),
    'prod.cta.btn': (None, 'بدء التجربة المجانية'),
    'prod.cta.sample': ('preview a live sample booking page', 'معاينة صفحة حجز نموذجية'),
    'foot.product.customers': ('Customers', 'العملاء'),
    'foot.company.beta': (None, 'بدء التجربة المجانية'),
}

DELETE = ('prod.ai.', 'prod.loc.', 'prod.tab.ai', 'prod.tab.locations', 'foot.product.payments')

changed = 0
for k, (e, a) in S.items():
    for lang, v in (('en', e), ('ar', a)):
        if v is not None and d[lang].get(k) != v:
            d[lang][k] = v
            changed += 1
for lang in ('en', 'ar'):
    for k in list(d[lang]):
        if k.startswith(DELETE):
            del d[lang][k]
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('values changed:', changed, '| keys:', len(d['en']), len(d['ar']))
