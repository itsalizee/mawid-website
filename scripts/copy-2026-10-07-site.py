"""One-off copy revision for i18n/site.json (pricing, about, contact, legal,
404, shared header/footer). Same rules as copy-2026-10-07-home.py:
truthful claims only, gender-neutral Arabic (masdar for buttons, plural for
the business owner, generic nouns). key -> (en, ar); None keeps that side.
"""
import json, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / 'i18n' / 'site.json'
d = json.loads(P.read_text())

START_AR = 'بدء التجربة المجانية'
S = {
    # ---- shared ----
    'cta.header': ('Start free trial', START_AR),
    'cta.beta': (None, START_AR),
    'cta.start': (None, START_AR),
    'foot.tagline': (
        'Booking, built for the Gulf. Arabic-first and Hijri-aware — designed for how Saudi, Emirati, Qatari and Kuwaiti businesses actually run.',
        'الحجوزات، مصمَّمة للخليج. عربية أولاً وتدعم التقويم الهجري — مبنية لطريقة عمل المنشآت في السعودية والإمارات وقطر والكويت.',
    ),
    'foot.product.beta': ('Start free trial', START_AR),

    # ---- about ----
    'about.lede': (
        None,
        'كل منصات الحجوزات التي تخدم الخليج بُنيت في مكان آخر ثم تُرجمت. بعضها أدوات عالمية بزر للعربية، وبعضها حاول التعريب لاحقاً. لم تُصمَّم أيٌّ منها من الأساس لطريقة عمل المنشآت في السعودية والإمارات وقطر والكويت. موعد صُمِّم لذلك.',
    ),
    'about.story.p1': (
        None,
        'أي شخص حاول حجز موعد في صالون أو عيادة أو نادٍ رياضي في الرياض أو دبي أو الدوحة أو الكويت يعرف السيناريو: رسالة على إنستغرام، ثم طلب رقم الجوال، ثم انتظار تأكيد على واتساب قد يصل وقد لا يصل، ثم الذهاب للموعد على أمل أنه ما زال محجوزاً.',
    ),
    'about.story.p2': (
        None,
        'على الجهة الأخرى من المحادثة، صاحب الصالون يدير أربع عشرة محادثة واتساب، وتقويماً في Google Sheets وآخر في ذاكرته، وكومة أوراق لتركيبات الصبغات وتفضيلات العملاء. حالات عدم الحضور تصل إلى ٢٠–٣٠٪، وحملات استعادة العملاء معدومة، وكل حجز يُعاد بناؤه يدوياً.',
    ),
    'about.story.p3': (
        None,
        'المنصات العالمية لا تستطيع حلّ هذا — لا تتحدث اللهجات الخليجية، ولا تعرض التواريخ الهجرية، ولا تتحدث لغة العميل الخليجي، ولا تفهم أن صباح الجمعة للصلاة. والمنصات المحلية لا تستطيع حلّه أيضاً — ضعيفة المنتج، وغير مستثمَر فيها.',
    ),
    'about.story.p4': (
        "Mawid is the platform we wished existed. Native to four GCC markets from day one. Built around Instagram and WhatsApp, because that's where bookings actually start. Arabic-first, with Hijri and Gregorian dates side by side. A searchable customer database that remembers every visit, every preference, every name.",
        'موعد هي المنصة التي تمنّينا وجودها. أصلية لأربعة أسواق خليجية من اليوم الأول. مبنية حول إنستغرام وواتساب، لأن الحجوزات تبدأ هناك فعلاً. عربية أولاً، والتاريخ الهجري بجانب الميلادي. وسجل عملاء قابل للبحث يتذكر كل زيارة وكل تفضيل وكل اسم.',
    ),
    'about.v1.b': (
        "We don't ship a global product with Arabic strings glued on. Every service, staff profile and booking page is bilingual at the data level, and the booking page shows Hijri dates because that's how much of the Gulf plans its week.",
        'لا نشحن منتجاً عالمياً ونلصق عليه نصوصاً عربية. كل خدمة وملف موظف وصفحة حجز ثنائية اللغة في صميم البيانات، وصفحة الحجز تعرض التاريخ الهجري لأن هكذا يخطط كثيرون في الخليج لأسبوعهم.',
    ),
    'about.v2.b': (
        "Gulf customers live on WhatsApp and Instagram. They won't download your app or remember another password. So every customer-facing flow we build starts with one question: does this work from a chat? If not, we redesign it.",
        'العملاء في الخليج يعيشون على واتساب وإنستغرام. لن يحمّلوا تطبيقاً، ولن يتذكروا كلمة مرور جديدة. لذلك كل تجربة تلامس العميل نبدأها بسؤال: هل تعمل من داخل محادثة؟ إن لم تعمل، نعيد تصميمها.',
    ),
    'about.v3.b': (
        'One flat monthly subscription, published on the pricing page. No commission on bookings, no surcharges, no extra fees for support. You see exactly what you pay.',
        'اشتراك شهري ثابت منشور على صفحة الأسعار. بدون عمولة على الحجوزات، وبدون رسوم إضافية، وبدون رسوم على الدعم. تعرفون بالضبط ما تدفعون.',
    ),
    'about.v4.h': ('Ship, then improve, with real customers.', 'نطلق، ثم نطوّر، مع عملاء حقيقيين.'),
    'about.v4.b': (
        "We'd rather put Mawid in front of real salons, clinics and restaurants, watch what breaks and fix it fast, than polish slides. Every customer gets a direct line to the people building it.",
        'نفضّل أن نضع موعد بين أيدي صالونات وعيادات ومطاعم حقيقية، ونراقب ما يتعطل ونصلحه بسرعة، على أن نصقل العروض التقديمية. كل عميل لديه خط مباشر مع من يبنون المنتج.',
    ),
    'about.cta.title': (None, 'تريدون رؤيته <span class="it">مباشرة؟</span>'),
    'about.cta.body': (
        "Start a 7-day free trial and take your first booking today — or talk to us and we'll set it up with you.",
        'ابدؤوا تجربة مجانية ٧ أيام واستقبلوا أول حجز اليوم — أو تواصلوا معنا وسنجهّزه معكم.',
    ),
    'about.cta.btn': ('Start free trial', START_AR),
    'about.team.kicker': ('The company', 'الشركة'),
    'about.team.title': ('Diyar Holdings.', 'ديار القابضة.'),
    'about.team.p1': (
        'Mawid is operated by Diyar Holdings LLC, a Wyoming-registered company purpose-built to scale technology products into Gulf markets. We chose Wyoming for the legal infrastructure — clean US incorporation, banking, and payment processing — while operating natively in the GCC where our customers are.',
        'تُدار موعد من قِبل شركة ديار القابضة ذ.م.م، وهي شركة مسجَّلة في ولاية وايومنغ أُسِّست لتوسيع المنتجات التقنية في أسواق الخليج. اخترنا وايومنغ لبنيتها القانونية — تأسيس أمريكي واضح، وخدمات مصرفية، ومعالجة مدفوعات — بينما نعمل في الخليج حيث يتواجد عملاؤنا.',
    ),
    'about.team.p2': (
        None,
        'فريقنا أطلق منتجات للمستهلكين وللشركات في الخليج وأمريكا الشمالية وأستراليا: مساكن جاهزة في الإمارات والسعودية، وأجهزة عافية في خمسين ولاية أمريكية، وبنية تسويق رقمي لأعمال الخدمات. موعد هو ما يحدث حين تتركّز هذه الخبرة التشغيلية والتقنية على مشكلة واحدة واضحة: كيف تدير أعمال الخدمات في الخليج يومها.',
    ),

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
    'price.faq.a1': (None, 'التجربة المجانية ٧ أيام. البطاقة مسجَّلة لكن لا يتم الخصم حتى اليوم الثامن. الإلغاء متاح في أي وقت خلال الأيام السبعة بدون أي رسوم.'),
    'price.faq.q2': (None, 'هل تمرّ مدفوعات العملاء عبر موعد؟'),
    'price.faq.a2': (
        'No. Your customers book online and pay you in person, the same as today. Online deposits are on our roadmap.',
        'لا. عملاؤكم يحجزون أونلاين ويدفعون لكم شخصياً كما هو الحال اليوم. تحصيل العربون أونلاين ضمن خطتنا القادمة.',
    ),
    'price.faq.a4': (
        'No. Booking alerts are included on every plan. When automated WhatsApp confirmations and reminders launch, standard usage will be included too.',
        'لا. تنبيهات الحجز مشمولة في كل الخطط. وعند إطلاق التأكيدات والتذكيرات التلقائية عبر واتساب، سيكون الاستخدام الاعتيادي مشمولاً أيضاً.',
    ),
    'price.faq.a5': (None, 'الإلغاء متاح في أي وقت من حسابكم في موعد. يستمر الاشتراك حتى نهاية دورة الفوترة الحالية، ونُصدِّر لكم قاعدة بيانات العملاء وسجل الحجوزات بصيغة CSV عند الطلب.'),

    # ---- legal ----
    'privacy.lede': (None, 'كيف تتعامل موعد مع المعلومات الشخصية لعملائنا وفرق عملهم، والأشخاص الذين يحجزون عبر صفحات الحجز الخاصة بهم.'),
    'privacy.s7.t': (None, 'حقوقكم'),
    'terms.lede': (None, 'الاتفاقية بينكم (المنشأة المستخدمة لـ موعد) وبين شركة ديار القابضة. يرجى القراءة بعناية — بالتسجيل توافقون على هذه الشروط.'),
    'legal.ar_note': (
        '',
        'هذه الوثيقة متاحة حالياً باللغة الإنجليزية، والنسخة الإنجليزية هي النسخة المعتمدة. لأي استفسار باللغة العربية: hello@mawid.ai',
    ),

    # ---- contact ----
    'contact.title': (None, 'تواصلوا <span class="it">معنا.</span>'),
    'contact.lede': (
        "Whether you're a business owner with a question, a chain weighing the Enterprise tier, or a partner looking to integrate — pick the channel that fits and we'll respond within one business day.",
        'سواء كنتم أصحاب نشاط لديكم استفسار، أو سلسلة تدرس الخطة المؤسسية، أو شريكاً يبحث عن التكامل — اختاروا القناة المناسبة وسنردّ خلال يوم عمل واحد.',
    ),
    'contact.c2.body': ('Demos, setup help, multi-location chains, Enterprise quotes.', 'العروض، المساعدة في الإعداد، السلاسل، عروض الأسعار المؤسسية.'),
    'contact.c3.body': (None, 'للعملاء الحاليين — الأخطاء، الفوترة، تغييرات الحساب، التكاملات.'),
    'contact.form.title': (None, 'أو أرسلوا رسالة'),
    'contact.form.success.body': (None, 'استلمنا رسالتكم وسنردّ عبر البريد الإلكتروني خلال يوم عمل واحد.'),
    'contact.form.error': (
        'Something went wrong. Please try again, or email hello@mawid.ai.',
        'حدث خطأ. يرجى المحاولة مجدداً، أو مراسلتنا على hello@mawid.ai.',
    ),
    'contact.subj.beta': ('Setup help', 'المساعدة في الإعداد'),
    'contact.office.note': (None, 'موعد تعمل عبر السعودية والإمارات وقطر والكويت. لا نملك حالياً مكاتب فعلية في الخليج. كل دعم العملاء والمبيعات يتم عن بُعد عبر واتساب والبريد الإلكتروني والمكالمات المرئية.'),

    # ---- 404 ----
    'err.sub': (None, 'الصفحة المطلوبة غير موجودة، أو نُقِلَت، أو في الرابط خطأ. يمكنكم العودة للصفحة الرئيسية.'),
}

changed = 0
for k, (e, a) in S.items():
    for lang, v in (('en', e), ('ar', a)):
        if v is not None and d[lang].get(k) != v:
            d[lang][k] = v
            changed += 1
    # Keys new to the dictionary need a value on both sides.
    for lang in ('en', 'ar'):
        d[lang].setdefault(k, d['en' if lang == 'ar' else 'ar'][k])
for k in set(d['en']) ^ set(d['ar']):
    print('only in one language:', k)
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('values changed:', changed, '| en keys:', len(d['en']), '| ar keys:', len(d['ar']))
