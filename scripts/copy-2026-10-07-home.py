"""One-off copy revision for the homepage dictionary (i18n/home.json).

Why (2026-10-07):
  1. Truth pass — the site described features Mawid doesn't have (an AI
     dialect assistant, no-show prediction, automated WhatsApp confirmations
     and reminders, auto-detected holidays, colour-formula templates, source
     analytics) plus unbacked stats ("vs pre-Mawid", "beta salons").
     Unverifiable claims are a Google Ads misrepresentation risk.
  2. Gender-neutral Arabic — the AR copy was feminine singular throughout.
     Style: masdar / noun phrases for buttons and labels; 2nd-person PLURAL
     (كم) for the business owner; generic nouns (العملاء، الفريق).

Each entry: key -> (en, ar). None keeps that language unchanged.
Kept as a script (not just the JSON diff) so the reasoning is reviewable.
"""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / 'i18n' / 'home.json'
d = json.loads(P.read_text())
en, ar = d['en'], d['ar']

S = {
    # ---- header / hero ----
    'cta.header': (None, 'بدء التجربة المجانية'),
    'hero.lede': (
        'Customers book from your Instagram or WhatsApp link in under a minute — in Arabic or English, on the Hijri or Gregorian calendar. You see every booking the moment it lands. Built for salons, clinics and restaurants in Saudi Arabia, the UAE, Qatar and Kuwait.',
        'عملاؤكم يحجزون من رابطكم في إنستغرام أو واتساب في أقل من دقيقة — بالعربية أو الإنجليزية، وبالتقويم الهجري أو الميلادي. وكل حجز يصلكم لحظة تأكيده. مصمَّم للصالونات والعيادات والمطاعم في السعودية والإمارات وقطر والكويت.',
    ),
    'hero.cta': (None, 'بدء التجربة المجانية'),
    'hero.cta2': (None, 'مشاهدة العرض'),
    'hero.cta_meta': ('7-day free trial · set up in minutes', 'تجربة مجانية ٧ أيام · إعداد في دقائق'),
    'hero.trust1': (None, 'تجربة مجانية — الإلغاء قبل نهايتها بدون أي رسوم'),
    'hero.s4.l': ('Booking link', 'رابط الحجز'),
    'hero.s4.v': ('Instagram · WhatsApp', 'إنستغرام · واتساب'),

    # ---- dashboard mockups (hero + preview) ----
    'hp.cust': (None, 'العملاء'),
    'hp.staff': ('Team', 'الفريق'),
    'hp.pay': ('Settings', 'الإعدادات'),
    'prev.cust': (None, 'العملاء'),
    'prev.staff': ('Team', 'الفريق'),
    'prev.pay': ('Settings', 'الإعدادات'),
    'prev.org_sub': ('Riyadh · Studio plan', 'الرياض · خطة الاستوديو'),
    'prev.bcrumb': ('27 Muharram – 3 Safar 1448 · 14 services · 6 team members', '٢٧ محرّم – ٣ صفر ١٤٤٨ · ١٤ خدمة · ٦ أعضاء في الفريق'),
    'prev.lede': (
        'Every screen of the admin console works in Arabic and English, right-to-left and left-to-right, and dates show in Gregorian and Hijri together. Figures below are illustrative.',
        'كل شاشة في لوحة الإدارة تعمل بالعربية والإنجليزية، من اليمين ومن اليسار، والتواريخ تظهر بالميلادي والهجري معاً. الأرقام المعروضة للتوضيح.',
    ),
    'prev.k2d': ('2 of 42 bookings', '٢ من ٤٢ حجزاً'),
    'prev.k3': (None, 'العملاء العائدون'),
    'prev.k3d': ("of this week's bookings", 'من حجوزات الأسبوع'),
    'prev.k4': ('Booked online', 'حجوزات أونلاين'),
    'prev.k4d': ('of 42 this week', 'من ٤٢ هذا الأسبوع'),

    # ---- proof strip + marquee ----
    'proof.label': ('Built for businesses in', 'مصمَّم للأعمال في'),
    'm.1': ('Salons', 'صالونات'),
    'm.2': ('Barbershops', 'صالونات حلاقة'),
    'm.3': ('Aesthetic clinics', 'عيادات تجميل'),
    'm.4': ('Dental clinics', 'عيادات أسنان'),
    'm.5': ('Spas', 'مراكز سبا'),
    'm.6': ('Restaurants', 'مطاعم'),
    'm.7': ('Fitness studios', 'استوديوهات لياقة'),
    'm.8': ('Dermatology', 'عيادات جلدية'),

    # ---- channels ----
    'ch.lede': (
        None,
        'ضعوا رابط الحجز في إنستغرام أو تيك توك أو سناب شات أو فيسبوك أو ملف نشاطكم على جوجل — أو أرسلوه على واتساب. الرابط نفسه يعمل أينما يجدكم عملاؤكم.',
    ),
    'ch.foot': (
        "<strong>You're not locked into one funnel.</strong> Use one link everywhere, or a separate tagged link for each channel from your Share tab.",
        '<strong>لستم مقيّدين بقناة واحدة.</strong> رابط واحد لكل مكان، أو رابط مخصص لكل قناة من تبويب المشاركة.',
    ),

    # ---- features ----
    'feat.title': (
        'Six things <span class="it">built for</span> how the Gulf books.',
        'ست خصائص <span class="it">مبنية</span> لطريقة الحجز في الخليج.',
    ),
    'feat.1.title': ("Your customers don't download an app. They tap your link.", 'عملاؤكم لا يحمّلون تطبيقاً. يضغطون على رابطكم.'),
    'feat.1.body': (
        'Your booking page lives where they already are — your Instagram bio, WhatsApp chats, your Google profile. They pick a service and a time and book in under a minute, in their language. No accounts, no passwords. Questions? One tap opens a WhatsApp chat with you. Automated WhatsApp confirmations and reminders are coming next.',
        'صفحة الحجز موجودة حيث يتواجد عملاؤكم أصلاً — في سيرة إنستغرام، ومحادثات واتساب، وملفكم على جوجل. يختارون الخدمة والوقت ويحجزون في أقل من دقيقة، بلغتهم. بدون حسابات أو كلمات مرور. ولأي استفسار، ضغطة واحدة تفتح محادثة واتساب معكم. التأكيدات والتذكيرات التلقائية عبر واتساب قادمة قريباً.',
    ),
    'feat.1.wa2': ('Friday 10:00 is free ✓ Book it here — takes 30 seconds 👇', 'الجمعة ١٠:٠٠ متاح ✓ الحجز من الرابط يأخذ ٣٠ ثانية 👇'),
    'feat.1.paytitle': ('Book at Salon Rasha', 'الحجز في صالون رشا'),
    'feat.1.wa3': ('Done — booked for Friday 🌸', 'تم — حجزت للجمعة 🌸'),
    'feat.2.body': (
        'Your booking page shows every date in Hijri and Gregorian side by side. Friday mornings are closed by default for Saudi businesses, and Eid, National Day or Ramadan hours go in as closures in seconds.',
        'صفحة الحجز تعرض كل تاريخ بالهجري والميلادي جنباً إلى جنب. صباح الجمعة مغلق افتراضياً للأعمال في السعودية، وإضافة إجازات العيد واليوم الوطني ودوام رمضان تتم في ثوانٍ.',
    ),
    'feat.3.label': ('03 — Team', '٠٣ — الفريق'),
    'feat.3.title': ("Every team member's day on one screen.", 'يوم كل عضو في الفريق على شاشة واحدة.'),
    'feat.3.body': (
        'Working hours, days off and holidays for each person. Prayer breaks and Friday mornings are blocked automatically, so customers only ever see times you can actually take.',
        'ساعات العمل والإجازات لكل موظف. أوقات الصلاة وصباح الجمعة محجوبة تلقائياً، فلا يرى العملاء إلا الأوقات المتاحة فعلاً.',
    ),
    'feat.3.head': ('Today · Thursday', 'اليوم · الخميس'),
    'feat.3.r1n': ('Maysa', 'ميساء'),
    'feat.3.r1s': ('10:00 – 18:00 · 5 bookings', '١٠:٠٠ – ١٨:٠٠ · ٥ حجوزات'),
    'feat.3.r2n': ('Hessa', 'حصة'),
    'feat.3.r2s': ('Day off', 'إجازة'),
    'feat.3.r3n': ('Dhuhr prayer', 'صلاة الظهر'),
    'feat.3.r3s': ('12:05 – 12:35 · nobody can book', '١٢:٠٥ – ١٢:٣٥ · لا يمكن الحجز'),
    'feat.3.r4n': ('Noura', 'نورة'),
    'feat.3.r4s': ('14:00 – 22:00 · 3 bookings', '١٤:٠٠ – ٢٢:٠٠ · ٣ حجوزات'),
    'feat.3.tagOn': ('On shift', 'دوام'),
    'feat.3.tagOff': ('Off', 'إجازة'),
    'feat.3.tagAuto': ('Auto', 'تلقائي'),
    'feat.4.body': (
        'Every service and staff profile is written in Arabic and English side by side. Each person picks their own interface language, and layouts flip direction cleanly. RTL is built in, not bolted on.',
        'كل خدمة وملف موظف يُكتب بالعربية والإنجليزية معاً. كل مستخدم يختار لغة واجهته، والاتجاه ينعكس بسلاسة. دعم RTL مبني من الأساس.',
    ),
    'feat.5.label': (None, '٠٥ — العملاء'),
    'feat.5.title': ("Every customer who's ever booked, on one screen.", 'كل عميل حجز لديكم يوماً، في شاشة واحدة.'),
    'feat.5.body': (
        'Mawid keeps a searchable record of everyone who books with you — visit history, no-show count, last visit and notes. Your team greets returning customers like regulars, because the system remembers.',
        'موعد يحتفظ بسجل قابل للبحث لكل من يحجز لديكم — الزيارات، وعدد مرات الغياب، وآخر زيارة، والملاحظات. فريقكم يستقبل العملاء العائدين كأنهم يعرفونهم، لأن النظام يتذكر.',
    ),
    'feat.5.head': (None, 'العملاء'),
    'feat.5.tagReg': (None, 'منتظم'),
    'feat.5.tagLapsed': (None, 'متوقف'),
    'feat.5.more': (None, '+ ٢٬٨٣٦ آخرون'),
    'feat.6.label': ('06 — Business types', '٠٦ — أنواع الأعمال'),
    'feat.6.title': (
        'Salons book a stylist. Restaurants book a table. Clinics book a slot.',
        'في الصالون يُحجز المختص، وفي المطعم الطاولة، وفي العيادة الموعد.',
    ),
    'feat.6.body': (
        'Pick your business type at signup and Mawid sets the booking flow to match: salons and spas get a service menu and team picker, restaurants get party size and table capacity, clinics get simple appointment slots. Set up in minutes, not days.',
        'اختاروا نوع نشاطكم عند التسجيل، وموعد يضبط طريقة الحجز تلقائياً: الصالونات والسبا تحصل على قائمة خدمات واختيار المختص، والمطاعم على عدد الأشخاص وسعة الطاولات، والعيادات على مواعيد بسيطة. إعداد في دقائق لا أيام.',
    ),
    'feat.6.t1': ('Salon · service + stylist', 'صالون · خدمة + مختص'),
    'feat.6.t1a': ('Service', 'الخدمة'),
    'feat.6.t1b': ('Stylist', 'المختص'),
    'feat.6.t1c': ('When', 'الموعد'),
    'feat.6.t1av': ('Color + cut', 'صبغة + قص'),
    'feat.6.t1bv': ('Maysa', 'ميساء'),
    'feat.6.t1cv': ('Fri 10:00', 'الجمعة ١٠:٠٠'),
    'feat.6.t2': ('Restaurant · reservation', 'مطعم · حجز طاولة'),
    'feat.6.t2a': ('Party of 4', '٤ أشخاص'),
    'feat.6.t2b': ('Table capacity checked', 'سعة الطاولات متاحة'),
    'feat.6.t2c': ('Note: patio, birthday', 'ملاحظة: الجلسة الخارجية، عيد ميلاد'),

    # ---- customer experience ----
    'exp.kicker': (None, 'تجربة العميل'),
    'exp.lede': (
        'Your customers go from Instagram link to confirmed appointment in under a minute. Mawid runs the booking page and the customer history — payment happens at your business, the way it always has. One flat monthly subscription: no transaction fees, no commission, no surprises.',
        'عملاؤكم ينتقلون من رابط إنستغرام إلى موعد مؤكد في أقل من دقيقة. موعد يدير صفحة الحجز وسجل العملاء — والدفع يتم لديكم كما اعتدتم. اشتراك شهري ثابت: بدون رسوم على المعاملات، بدون عمولة، بدون مفاجآت.',
    ),
    'exp.s1.h': (None, 'يجدونكم على إنستغرام.'),
    'exp.s1.b': (None, 'رابط الحجز الخاص بكم في سيرة حسابكم، وفي الستوريز، وفي رسائلكم. ضغطة واحدة ويصلون إلى صفحتكم — بدون تحميل أو تسجيل.'),
    'exp.s3.h': ('You see it instantly.', 'يصلكم الحجز فوراً.'),
    'exp.s3.b': (
        "The booking drops into your calendar and you get an email the moment it's made — with the customer's name, service, time and phone number.",
        'يظهر الحجز في تقويمكم وتصلكم رسالة بريد لحظة تأكيده — باسم العميل والخدمة والوقت ورقم الجوال.',
    ),
    'exp.s4.h': ('Questions? One tap to WhatsApp.', 'استفسار؟ ضغطة واحدة إلى واتساب.'),
    'exp.s4.b': (
        'Every booking page has a WhatsApp button that opens a chat with you, so customers ask on the channel they use every day. Automated WhatsApp confirmations and reminders are coming next.',
        'كل صفحة حجز فيها زر واتساب يفتح محادثة معكم مباشرة، فيسأل العملاء عبر القناة التي يستخدمونها يومياً. التأكيدات والتذكيرات التلقائية عبر واتساب قادمة قريباً.',
    ),
    'exp.bp.h': (None, 'حجز موعد.'),
    'exp.bp.svcs': (None, 'اختيار الخدمة'),
    'exp.bp.s2m': (None, '١٢٠ دقيقة · أي مختص'),
    'exp.bp.confirm': ('Questions? Chat on', 'للاستفسار:'),

    # ---- pricing ----
    'price.title': (None, 'سعرٌ بسيط. <span class="it">ينمو معكم.</span>'),
    'price.lede': (
        "Every plan includes unlimited bookings, email booking alerts, a WhatsApp chat button, full Arabic and English, and prayer-time aware scheduling. Start with a 7-day free trial — cancel before it ends and you're not charged.",
        'كل الخطط تشمل حجوزات غير محدودة، وتنبيهات الحجز بالبريد، وزر محادثة واتساب، والعربية والإنجليزية بالكامل، وجدولة تراعي أوقات الصلاة. تجربة مجانية ٧ أيام — والإلغاء قبل نهايتها بدون أي رسوم.',
    ),
    'price.featured': ('Recommended', 'الخيار المقترح'),
    'price.t1.tag': ('Solo professionals and small businesses, up to 3 staff. Single location.', 'للمختصين المستقلين والأعمال الصغيرة حتى ٣ موظفين. فرع واحد.'),
    'price.t1.f1': (None, 'حتى ٣ موظفين'),
    'price.t1.f3': ('Email booking alerts + WhatsApp chat button', 'تنبيهات الحجز بالبريد وزر واتساب'),
    'price.t1.f4': (None, 'قاعدة بيانات العملاء'),
    'price.t1.cta': (None, 'بدء تجربة ٧ أيام'),
    'price.t2.tag': ('Growing businesses, up to 10 staff. Single location.', 'للأعمال النامية حتى ١٠ موظفين. فرع واحد.'),
    'price.t2.f2': (None, 'حتى ١٠ موظفين وجداولهم'),
    'price.t2.f3': ('Multi-staff scheduling', 'جدولة لعدة موظفين'),
    'price.t2.cta': (None, 'بدء تجربة ٧ أيام'),
    'price.t3.tag': ('Larger businesses with unlimited staff. Hands-on onboarding.', 'للأعمال الكبيرة بعدد موظفين غير محدود. إعداد مخصَّص.'),
    'price.t3.f2': (None, 'عدد موظفين غير محدود'),
    'price.t3.cta': (None, 'بدء تجربة ٧ أيام'),
    'price.t4.tag': ('Several locations · Volume pricing · Talk to us', 'عدة فروع · تسعير حسب الحجم · تواصلوا معنا'),
    'price.t4.body': (
        'For chains, franchises and multi-brand operators. Multi-location support is on our roadmap — talk to us about early access, custom onboarding and volume pricing.',
        'للسلاسل والامتيازات والمشغّلين متعددي العلامات. دعم الفروع المتعددة ضمن خطتنا القادمة — تواصلوا معنا للوصول المبكر والإعداد المخصص والتسعير حسب الحجم.',
    ),
    'price.t4.cta': (None, 'التواصل مع المبيعات'),

    # ---- setup-call form (was "beta") ----
    'beta.kicker': ('Setup help', 'المساعدة في الإعداد'),
    'beta.title': ('Prefer we set it up with you?', 'تفضّلون أن نجهّزه معكم؟'),
    'beta.body': (
        "Tell us about your business and we'll get you live with your services, team and hours — usually in one short call. The founders answer every message.",
        'أخبرونا عن نشاطكم وسنجهّز معكم الخدمات والفريق وساعات العمل — غالباً في مكالمة قصيرة واحدة. المؤسسون يردّون على كل رسالة.',
    ),
    'beta.p2': (None, 'ننقل خدماتكم وفريقكم وسجلاتكم بأنفسنا.'),
    'beta.p3': (None, 'دعم مباشر — من الفريق الذي بنى موعد نفسه.'),
    'beta.p4': (None, 'تدريب بالعربية والإنجليزية لكم ولفريقكم.'),
    'beta.p5': ('Custom features prioritized for active customers.', 'ميزات مخصصة بناءً على احتياجات العملاء النشطين.'),
    'beta.f.biz': ('Business name', 'اسم النشاط'),
    'beta.f.name': (None, 'الاسم'),
    'beta.f.country_ph': (None, 'اختيار الدولة'),
    'beta.f.vert_ph': (None, 'اختيار القطاع'),
    'beta.v.barber': ('Barbershop', 'صالون حلاقة'),
    'beta.v.restaurant': ('Restaurant', 'مطعم'),
    'beta.f.submit': ('Request a setup call', 'طلب مكالمة إعداد'),
    'beta.f.submitting': ('Sending…', 'جارٍ الإرسال…'),
    'beta.f.error': (
        'Something went wrong. Please try again, or email hello@mawid.ai.',
        'حدث خطأ. يرجى المحاولة مجدداً، أو مراسلتنا على hello@mawid.ai.',
    ),
    'beta.t3': ('Founder-led onboarding', 'إعداد بإشراف المؤسسين'),
    'beta.f.foot': ("We'll get back to you on WhatsApp.", 'سنتواصل معكم عبر واتساب.'),
    'beta.s.title': ("Thanks — we've got it.", 'وصلنا طلبكم، شكراً.'),
    'beta.s.body': ("We'll message you on WhatsApp to set up a short call.", 'سنراسلكم عبر واتساب لترتيب مكالمة قصيرة.'),

    # ---- footer ----
    'footer.about': (
        'The booking platform built for the Gulf. Arabic-first, Hijri-aware, and built around how your customers actually book — on Instagram and WhatsApp.',
        'منصة الحجوزات المصمَّمة للخليج. عربية أولاً، تدعم التقويم الهجري، ومبنية على طريقة حجز عملائكم الفعلية — عبر إنستغرام وواتساب.',
    ),
    'footer.beta': (None, 'بدء التجربة المجانية'),
    'footer.sales': (None, 'التواصل مع المبيعات'),
    'footer.forRestaurants': ('For restaurants', 'للمطاعم'),
    'footer.forClinics': ('For clinics', 'للعيادات'),
}

DELETE_PREFIXES = ('roadmap.',)
DELETE_KEYS = {'feat.3.who1', 'feat.3.who2', 'feat.3.d1', 'feat.3.d2', 'feat.3.d3', 'feat.3.d4',
               'feat.6.t2a_old'}

changed = 0
for k, (e, a) in S.items():
    for lang, v in (('en', e), ('ar', a)):
        if v is not None and d[lang].get(k) != v:
            d[lang][k] = v
            changed += 1
for lang in ('en', 'ar'):
    for k in list(d[lang]):
        if k.startswith(DELETE_PREFIXES) or k in DELETE_KEYS:
            del d[lang][k]
# Every key must exist in both languages.
for k in set(d['en']) ^ set(d['ar']):
    src = 'en' if k in d['en'] else 'ar'
    print('only in', src, ':', k)

P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('values changed:', changed, '| en keys:', len(d['en']), '| ar keys:', len(d['ar']))
