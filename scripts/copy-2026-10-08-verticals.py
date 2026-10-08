"""One-off truth + gender pass for the restaurants and clinics pages (EN + AR).

These pages are hand-written HTML (no data-i18n), so edits are exact-text
replacements that must each match. What changes:

- WhatsApp: no automated confirmations / reminders / reschedule links yet.
  Copy now describes what ships (WhatsApp chat button on the booking page
  and confirmation, email alert per booking) and says automation is coming.
- Hero mocks: the WhatsApp bubble shows the real click-to-chat message;
  Hijri dates corrected (May 2026 = Dhu al-Qadah 1447); no "Waitlist" or
  "Walk-in" (neither exists); plan names match the app (Professional /
  Studio).
- Unverifiable stats and competitor claims removed (20% no-shows, $500/mo
  EHR, "Calendly doesn't speak Arabic", Eat App pricing/Arabic).
- Arabic addresses the business in the plural, never the feminine singular.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALL = None  # replace every occurrence (at least one)


def wa_block(lang, venue, outgoing, reply):
    t1, t2 = ('2:14 PM', '2:16 PM') if lang == 'en' else ('٢:١٤ م', '٢:١٦ م')
    return (
        '          <div class="float-wa">\n'
        f'            <span>{outgoing}</span>\n'
        f'            <span class="float-wa-time">{t1} <span class="check">✓✓</span></span>\n'
        '          </div>\n'
        '          <div class="float-wa in">\n'
        f'            <span>{reply}</span>\n'
        f'            <span class="float-wa-time">{t2}</span>\n'
        '          </div>\n'
    )


WA_OLD = re.compile(r'          <div class="float-wa in">\n.*?</div>\n          <div class="float-wa">\n.*?</div>\n', re.S)

EDITS = {
    'clinics/index.html': [
        ('<meta name="description" content="Mawid for clinics. Arabic-first booking, WhatsApp confirmations, Hijri-aware reminders.',
         '<meta name="description" content="Mawid for clinics. Arabic-first online booking with Hijri and Gregorian dates and a one-tap WhatsApp button.', 1),
        ('<meta property="og:description" content="Arabic-first booking. WhatsApp confirmations. Hijri-aware reminders.',
         '<meta property="og:description" content="Arabic-first booking. Hijri + Gregorian dates. One tap to WhatsApp.', 1),
        ('Arabic-first. WhatsApp-native. Hijri-aware. Built for dermatology, dental, and aesthetic clinics across the Gulf — the front-desk software your EHR was never going to be.',
         'Arabic-first. Hijri-aware. One tap to WhatsApp. Built for dermatology, dental, and aesthetic clinics across the Gulf — the front-desk booking page your EHR was never going to be.', 1),
        ('Riyadh · Clinic plan', 'Riyadh · Professional plan', 1),
        ('3 Safar · Friday, May 16 · 18 patients', '29 Dhu al-Qadah · Saturday, May 16 · 18 patients', 1),
        ('WA', ('en', 'Clinic Derma', 'Hi Clinic Derma 🌸 This is Layan, I just booked.',
                'Welcome Layan! See you Monday at 11:30 with Dr. Hassan 💚'), 1),
        ('Mawid handles patient appointments, confirmations, and reminders.',
         'Mawid handles patient appointments: the booking page, the schedule and the front-desk view.', 1),
        ('Half the time something falls through. No-shows hit 20%.',
         'Something always falls through, and no-shows go untracked.', 1),
        ("You're a number on Vezeeta.", "You're one listing among many.", 1),
        ('Marketplace platforms compete you on price, take commission per booking, and own your patient relationship.',
         'Directory apps list you next to the clinic down the street, often charge per booking, and own the patient relationship.', 1),
        ("Calendly doesn't speak Arabic.", "Global tools weren't built for the Gulf.", 1),
        ('Global booking tools assume English-speaking patients on Western calendars. RTL is an afterthought. Hijri dates don\'t exist. Friday morning isn\'t a "weekend."',
         'Most booking tools assume English-speaking patients on a Western calendar. Arabic and RTL come second, Hijri dates are missing, and Friday is just another weekday.', 1),
        ('SevenRooms is overkill.', 'Hospital systems are overkill.', 1),
        ('Enterprise EHR + billing platforms start at $500/month and take three months to onboard.',
         'Enterprise EHR and billing suites are priced and paced for hospitals, with months of onboarding.', 1),
        ('WhatsApp confirmation arrives instantly with the date in Hijri and Gregorian. 24h before the appointment, a reminder. 2h before, a nudge with your clinic\'s location pin.',
         'The confirmation screen shows the date in Hijri and Gregorian, adds it to their calendar in one tap, and has a WhatsApp button if they have a question. Automated WhatsApp reminders are coming soon.', 1),
        ('Four things <span class="it">no other booking platform</span> in the Gulf gives you.', 'Four things <span class="it">built for</span> Gulf clinics.', 1),
        ('<h3>WhatsApp confirmations + reminders.</h3>', '<h3>WhatsApp, one tap away.</h3>', 1),
        ("The patient doesn't install anything, doesn't make an account. Confirmations land in WhatsApp with a tap-to-reschedule link. Reminders are timed to your clinic's no-show patterns.",
         "Patients don't install anything or make an account. Your booking page and every confirmation have a WhatsApp button that opens a chat with your clinic. Automated WhatsApp confirmations and reminders are coming soon; until then, your team gets an email for every new booking.", 1),
        ('Reminders carry both calendars. Friday morning prayer time is blocked by default for KSA clinics. Ramadan-shifted hours are respected. We built for the Gulf calendar, not against it.',
         'Your booking page shows both calendars. Friday mornings are closed by default for Saudi clinics, prayer breaks are blocked automatically, and Ramadan hours or Eid closures go in in seconds. Built for the Gulf calendar, not against it.', 1),
        ('Names, phones, visit count, last seen, preferred provider, optional free-text notes.',
         'Names, phones, visit count, no-shows, last visit, optional free-text notes.', 1),
        ('No surcharges for SMS or support.', 'No surcharges for support.', 1),
        ('<div class="vert-price-cap">Clinic plan</div>', '<div class="vert-price-cap">Professional plan</div>', 1),
        ('Unlimited appointments · WhatsApp + email confirmations · Hijri-aware reminders · Patient database (non-clinical) · Bilingual booking page · 7-day free trial',
         'Unlimited appointments · Email booking alerts · WhatsApp chat button · Hijri + Gregorian booking page · Patient database (non-clinical) · Bilingual booking page · 7-day free trial', 1),
        ('If you need an EHR + billing suite, talk to platforms like Cura, Medscope, or Yashfeen instead — that\'s not what Mawid does.',
         'If you need an EHR and billing suite, run a dedicated medical system alongside Mawid — that\'s not what Mawid does.', 1),
        ('Your team uses Mawid for appointments + reminders,', 'Your team uses Mawid for appointments,', 1),
        ('<summary>Can patients reschedule via WhatsApp?</summary>', '<summary>Can patients reschedule?</summary>', 1),
        ('Yes. Every confirmation includes a tap-to-reschedule link. The change reaches your dashboard in real time so the front desk always sees the truth.',
         'Yes. They tap the WhatsApp button on their confirmation to message your clinic; your team cancels the old slot and sends the booking link so they can pick a new time. One-tap self-serve rescheduling is on the roadmap.', 1),
        ('Mawid asks the patient an optional "insurance provider" free-text field at booking so your team has it before the visit.',
         'Patients can mention their insurance provider in the optional note at booking, so your team has it before the visit.', 1),
    ],
    'restaurants/index.html': [
        ('<meta name="description" content="Mawid for restaurants. Arabic-first reservations, WhatsApp confirmations, Hijri-aware reminders.',
         '<meta name="description" content="Mawid for restaurants. Arabic-first online reservations with party size, table capacity, Hijri and Gregorian dates and a one-tap WhatsApp button.', 1),
        ('<meta property="og:description" content="Arabic-first reservations. WhatsApp confirmations. Hijri-aware reminders.',
         '<meta property="og:description" content="Arabic-first reservations. Hijri + Gregorian dates. One tap to WhatsApp.', 1),
        ('Riyadh · Restaurant plan', 'Riyadh · Studio plan', 1),
        ('<span>Waitlist</span>', '<span>Calendar</span>', 1),
        ('3 Safar · Friday, May 16 · 42 covers', '28 Dhu al-Qadah · Friday, May 15 · 42 covers', 1),
        ('Party of 4 · prefers patio', 'Party of 4 · patio please', 1),
        ('<span class="hp-res-tag tag-walkin">Walk-in</span>', '<span class="hp-res-tag tag-walkin">New</span>', 1),
        ('WA', ('en', 'Cafe Lateef', 'Hi Cafe Lateef 🌸 This is Layan, I just booked.',
                'Welcome Layan! Table for 4 on Friday at 9:30 — see you then 🌿'), 1),
        ('The hostess holds the whole night in her head. She moves to a different shift and tomorrow\'s reservations get half-forgotten.',
         'Your host holds the whole night in their head. When they change shifts, tomorrow\'s reservations get half-forgotten.', 1),
        ("OpenTable doesn't know Riyadh. Eat App charges enterprise prices for SMB features. Neither speaks Arabic the way your guests do.",
         'Global reservation platforms are built and priced for big restaurant groups, and Arabic usually comes second.', 1),
        ('WhatsApp confirmation arrives instantly with the date in both Hijri and Gregorian. Thursday morning gets a reminder. Friday morning, a "see you tonight" nudge.',
         'The confirmation screen shows the date in Hijri and Gregorian, adds it to their calendar in one tap, and has a WhatsApp button if plans change. Automated WhatsApp reminders are coming soon.', 1),
        ("<h3>Sees who's coming.</h3>", "<h3>See who's coming.</h3>", 1),
        ('Four things <span class="it">no other platform</span> in the Gulf gives you.', 'Four things <span class="it">built for</span> Gulf restaurants.', 1),
        ('<h3>WhatsApp confirmations.</h3>', '<h3>WhatsApp, one tap away.</h3>', 1),
        ("The guest doesn't install anything, doesn't make an account. The confirmation lands in WhatsApp — the app they already check forty times a day — with a tap-to-reschedule link.",
         "Guests don't install anything or make an account. Your booking page and every confirmation have a WhatsApp button that opens a chat with you. Automated WhatsApp confirmations and reminders are coming soon; until then, you get an email for every new reservation.", 1),
        ('Reminders carry both calendars. Ramadan iftar reservations work. Eid bookings work. Friday morning prayer time is blocked by default for Saudi venues.',
         'Your booking page shows both calendars. Ramadan iftar and Eid reservations work like any other night, Friday mornings are closed by default for Saudi venues, and holiday closures go in in seconds.', 1),
        ('Mawid remembers their name, their preferred table, the food allergy you noted last time.',
         'Mawid keeps their name, number, visit count and the food allergy you noted last time.', 1),
        ('No surcharges for SMS or support.', 'No surcharges for support.', 1),
        ('<div class="vert-price-cap">Restaurant plan</div>', '<div class="vert-price-cap">Studio plan</div>', 1),
        ('Unlimited reservations · WhatsApp + email confirmations · Hijri-aware reminders · Searchable guest database · Bilingual booking page · 7-day free trial',
         'Unlimited reservations · Email booking alerts · WhatsApp chat button · Hijri + Gregorian booking page · Searchable guest database · Bilingual booking page · 7-day free trial', 1),
        ('The confirmation lands in WhatsApp. They never sign up for anything.',
         'They see their confirmation right away and never sign up for anything.', 1),
        ('/month for restaurants.', '/month on the Studio plan.', 1),
        ('Your hostess marks walk-ins on the dashboard so you have one source of truth for who\'s in the building.',
         'The dashboard shows tonight\'s reservations by hour, so your host knows exactly what\'s booked.', 1),
        ('Yes. Every confirmation includes a tap-to-reschedule link. The change reaches your dashboard in real time so the hostess always sees the truth.',
         'Yes. They tap the WhatsApp button on their confirmation to message you; your team cancels the old reservation and sends the booking link for a new time. One-tap self-serve changes are on the roadmap.', 1),
        ('Yes, by default for guests with Arabic phones.', 'Yes, automatically for guests whose phone is set to Arabic.', 1),
        ('Free 7-day trial. No credit card required to see the demo. Cancel anytime.', 'Free 7-day trial. Cancel anytime.', 1),
    ],
    'ar/clinics/index.html': [
        ('حجوزات عربية أولاً، تأكيدات واتساب، تذكيرات تراعي التقويم الهجري. الاستقبال فقط — السجلات الطبية تبقى في النظام الموجود عندك.',
         'حجز أونلاين عربي أولاً، بالتاريخ الهجري والميلادي، مع زر واتساب بضغطة. الاستقبال فقط — السجلات الطبية تبقى في نظامكم الحالي.', 1),
        ('حجوزات عربية أولاً. تأكيدات واتساب. تذكيرات تراعي التقويم الهجري. الاستقبال فقط — السجلات الطبية تبقى عندك.',
         'حجز عربي أولاً. هجري وميلادي. واتساب بضغطة. الاستقبال فقط — السجلات الطبية تبقى عندكم.', 1),
        ('يستحقها مرضاكِ', 'يستحقها مرضاكم', 1),
        ('عربية أولاً. تعمل على واتساب. تراعي التقويم الهجري. مصمَّمة لعيادات الجلدية والأسنان والتجميل في الخليج — برنامج الاستقبال الذي لم يكن نظامكِ الطبي ليكونه أبداً.',
         'عربية أولاً. تراعي التقويم الهجري. وواتساب على بُعد ضغطة. مصمَّمة لعيادات الجلدية والأسنان والتجميل في الخليج — صفحة الحجز التي لم يكن نظامكم الطبي ليوفّرها أبداً.', 1),
        ('الرياض · باقة العيادات', 'الرياض · الباقة الاحترافية', 1),
        ('٣ صفر · الجمعة ١٦ مايو · ١٨ مريض', '٢٩ ذو القعدة · السبت ١٦ مايو · ١٨ مريضاً', 1),
        ('>جديدة<', '>جديد<', 1),
        ('WA', ('ar', 'عيادة ديرما', 'هلا عيادة ديرما 🌸 أنا ليان حجزت توّي.',
                'أهلاً ليان! بانتظاركم الاثنين ١١:٣٠ مع د. حسن 💚'), 1),
        ('موعد يدير حجوزات المرضى، التأكيدات، والتذكيرات. يحفظ الأسماء، الجوالات، تاريخ الزيارات، وأي ملاحظات يضيفها فريقكِ',
         'موعد يدير حجوزات المرضى: صفحة الحجز، والجدول، وشاشة الاستقبال. يحفظ الأسماء، والجوالات، وسجل الزيارات، وأي ملاحظات يضيفها فريقكم', 1),
        ('نظامكِ الطبي الحالي (أو فريقكِ) يتولى ذلك', 'نظامكم الطبي الحالي (أو فريقكم) يتولى ذلك', 1),
        ('نصف الوقت شيء يضيع. حالات عدم الحضور تصل ٢٠٪.', 'دائماً هناك شيء يضيع، وحالات عدم الحضور لا يتابعها أحد.', 1),
        ('أنتِ مجرد رقم على Vezeeta.', 'عيادتكم مجرد اسم في قائمة طويلة.', 1),
        ('منصات السوق تنافسكِ على السعر، تأخذ عمولة على كل حجز، وتمتلك علاقتكِ بالمريض. علامتكِ التجارية تختفي.',
         'تطبيقات الأدلة تعرضكم بجانب العيادة المجاورة، وغالباً تأخذ رسوماً على كل حجز، وتمتلك علاقتكم بالمريض. علامتكم التجارية تختفي.', 1),
        ('Calendly ما يتحدث العربية.', 'الأدوات العالمية لم تُصمَّم للخليج.', 1),
        ('أدوات الحجز العالمية تفترض مرضى يتحدثون الإنجليزية وتقويمات غربية. الـ RTL يأتي لاحقاً. التقويم الهجري غير موجود.',
         'معظم أدوات الحجز تفترض مرضى يتحدثون الإنجليزية وتقويماً غربياً. العربية والـ RTL تأتي لاحقاً، والتقويم الهجري غائب.', 1),
        ('SevenRooms مبالَغ.', 'أنظمة المستشفيات مبالَغ فيها.', 1),
        ('أنظمة EHR + فوترة المؤسسات تبدأ من ٥٠٠ دولار شهرياً وتستغرق ثلاثة أشهر للإعداد. أنتِ تريدين صفحة حجز، لا نظام مستشفى.',
         'أنظمة السجلات الطبية والفوترة للمؤسسات مسعّرة ومصممة للمستشفيات، وإعدادها يستغرق شهوراً. أنتم تحتاجون صفحة حجز، لا نظام مستشفى.', 1),
        ('تجربة مرضاكِ بسيطة كحجز كوب قهوة. تجربة فريقكِ شاشة واحدة',
         'تجربة مرضاكم بسيطة كطلب كوب قهوة. وتجربة فريقكم شاشة واحدة', 1),
        ('تشاركين رابط الحجز', 'تشاركون رابط الحجز', 1),
        ('تأكيد واتساب يصل فوراً بالتقويمين. قبل الموعد بـ٢٤ ساعة، تذكير. قبل الموعد بساعتين، رسالة مع موقع العيادة.',
         'شاشة التأكيد تعرض الموعد بالتقويمين، وتضيفه لتقويم الجوال بضغطة، وفيها زر واتساب لأي استفسار. التذكيرات التلقائية عبر واتساب قادمة قريباً.', 1),
        ('اضغطي لتأكدي وصوله، اكتماله، أو عدم حضوره.', 'بضغطة تسجّلون وصوله، أو اكتمال الموعد، أو عدم حضوره.', 1),
        ('ما تحصلين عليه', 'ما تحصلون عليه', 1),
        ('أربع خصائص <span class="it">لا توفّرها</span> أي منصة حجوزات في الخليج.', 'أربع خصائص <span class="it">مصممة</span> لعيادات الخليج.', 1),
        ('تأكيدات وتذكيرات واتساب.', 'واتساب على بُعد ضغطة.', 1),
        ('المريض ما يحمّل شيء، ولا يسجّل في حساب. التأكيدات تصل في واتساب مع رابط تعديل. التذكيرات موقوتة حسب أنماط عدم الحضور في عيادتكِ.',
         'المريض لا يحمّل شيئاً ولا يسجّل في حساب. صفحة الحجز وكل تأكيد فيهما زر واتساب يفتح محادثة مع عيادتكم. التأكيدات والتذكيرات التلقائية عبر واتساب قادمة قريباً، وحتى ذلك الحين يصل فريقكم بريد مع كل حجز جديد.', 1),
        ('التذكيرات تحمل التقويمين. صباح الجمعة وقت الصلاة محجوز افتراضياً لعيادات السعودية. ساعات رمضان المعدَّلة محترمة.',
         'صفحة الحجز تعرض التقويمين. صباح الجمعة مغلق افتراضياً لعيادات السعودية، وأوقات الصلاة محجوبة تلقائياً، ودوام رمضان وإجازات العيد تُضاف في ثوانٍ.', 1),
        ('الأسماء، الجوالات، عدد الزيارات، آخر زيارة، الطبيب المفضل، ملاحظات حرة اختيارية. نظامكِ الطبي الحالي يحفظ السجل الطبي.',
         'الأسماء، والجوالات، وعدد الزيارات، ومرات الغياب، وآخر زيارة، وملاحظات حرة اختيارية. نظامكم الطبي الحالي يحفظ السجل الطبي.', 1),
        ('لا رسوم إضافية للرسائل أو الدعم.', 'لا رسوم إضافية على الدعم.', 1),
        ('خطة العيادات', 'الباقة الاحترافية', 1),
        ('مواعيد غير محدودة · تأكيدات واتساب وبريد · تذكيرات تراعي التقويم الهجري · سجل مرضى (غير طبي) · صفحة حجز ثنائية اللغة · تجربة مجانية ٧ أيام',
         'مواعيد غير محدودة · تنبيهات الحجز بالبريد · زر محادثة واتساب · صفحة حجز بالهجري والميلادي · سجل مرضى (غير طبي) · صفحة حجز ثنائية اللغة · تجربة مجانية ٧ أيام', 1),
        ('نظامكِ الطبي الحالي يحفظ السجل الطبي. إذا احتجتِ نظام EHR + فوترة، تكلّمي مع منصات مثل Cura أو Medscope أو يَشفِين — هذا ليس ما يفعله موعد.',
         'نظامكم الطبي الحالي يحفظ السجل الطبي. وإذا احتجتم نظام سجلات طبية وفوترة، فاستخدموا نظاماً طبياً مخصصاً بجانب موعد — هذا ليس ما يفعله موعد.', 1),
        ('فريقكِ يستخدم موعد للحجوزات والتذكيرات، ويواصل', 'فريقكم يستخدم موعد للحجوزات، ويواصل', 1),
        ('هل يستطيع المرضى إعادة الجدولة عبر واتساب؟', 'هل يستطيع المرضى تغيير الموعد؟', 1),
        ('نعم. كل تأكيد يحتوي رابط تعديل. التغيير يصل لوحتكِ فوراً، فالاستقبال دائماً يشوف الحقيقة الكاملة.',
         'نعم. يضغط المريض زر واتساب في صفحة التأكيد ليراسل عيادتكم، ويلغي فريقكم الموعد القديم ويرسل له رابط الحجز ليختار وقتاً جديداً. تغيير الموعد بضغطة من المريض نفسه ضمن خطتنا القادمة.', 1),
        ('الصقيه في بايو إنستغرام، أرسليه عبر واتساب، أو ضعيه كـ QR كود على لوحة في الاستقبال. هو صفحة حجز كاملة، ليس ودجت تضعينها في موقع.',
         'ضعوه في بايو إنستغرام، أو أرسلوه عبر واتساب، أو اطبعوه كرمز QR على لوحة في الاستقبال. هو صفحة حجز كاملة، ليس أداة تحتاج تركيبها في موقع.', 1),
        (re.compile(r'موعد يسأل المريض عن .{1,3}شركة التأمين.{1,3} كحقل نصي اختياري عند الحجز ليكون لدى فريقكِ هذه المعلومة قبل الزيارة\.'),
         'يمكن للمريض ذكر شركة التأمين في الملاحظة الاختيارية عند الحجز، ليكون لدى فريقكم هذه المعلومة قبل الزيارة.', 1),
        ('تستقبل عيادتكِ', 'تستقبل عيادتكم', 1),
        ('نعطيكِ رابط حجز.', 'ونعطيكم رابط حجز.', 1),
        ('توقّفي عن إدارة المواعيد على <span class="it">جلسات واتساب.</span>', 'كفى إدارة المواعيد في <span class="it">محادثات واتساب.</span>', 1),
        ('نظامكِ الطبي يواصل ما يفعله', 'نظامكم الطبي يواصل ما يفعله', 1),
    ],
    'ar/restaurants/index.html': [
        ('حجوزات عربية أولاً، تأكيدات واتساب، تذكيرات تراعي التقويم الهجري.',
         'حجوزات أونلاين عربية أولاً، مع عدد الضيوف وسعة الطاولات والتاريخ الهجري والميلادي وزر واتساب بضغطة.', 1),
        ('حجوزات عربية أولاً. تأكيدات واتساب. تذكيرات تراعي التقويم الهجري.',
         'حجوزات عربية أولاً. هجري وميلادي. واتساب بضغطة.', 1),
        ('ضيوفكم يختارون الوقت ويأكدون.', 'ضيوفكم يختارون الوقت ويؤكدون.', 1),
        ('الرياض · باقة المطاعم', 'الرياض · باقة الاستوديو', 1),
        ('قائمة الانتظار', 'التقويم', 1),
        ('٣ صفر · الجمعة ١٦ مايو · ٤٢ ضيف', '٢٨ ذو القعدة · الجمعة ١٥ مايو · ٤٢ ضيفاً', 1),
        ('مجموعة من ٤ · تفضّل التراس', 'مجموعة من ٤ · طلب التراس', 1),
        ('>واقف<', '>جديد<', 1),
        ('WA', ('ar', 'مقهى لطيف', 'هلا مقهى لطيف 🌸 أنا ليان حجزت توّي.',
                'أهلاً ليان! طاولتكم لأربعة الجمعة ٩:٣٠ م — بانتظاركم 🌿'), 1),
        ('المضيفة تحفظ الليلة كاملة في رأسها. تنتقل لوردية ثانية، نصف حجوزات بكرة تُنسى.',
         'المسؤول عن الحجوزات يحفظ الليلة كاملة في رأسه. ينتقل لوردية ثانية، فتُنسى نصف حجوزات بكرة.', 1),
        ('OpenTable ما يعرف الرياض. Eat App بأسعار مؤسسات لمطاعم صغيرة. ولا واحدة تتحدث العربية كما يتكلم ضيوفكم.',
         'منصات الحجز العالمية مصممة ومسعّرة لمجموعات المطاعم الكبيرة، والعربية غالباً تأتي في المرتبة الثانية.', 1),
        ('تأكيد واتساب يصل فوراً مع التاريخ بالهجري والميلادي. صباح الخميس يصله تذكير. صباح الجمعة، رسالة «أشوفك الليلة».',
         'شاشة التأكيد تعرض التاريخ بالهجري والميلادي، وتضيفه لتقويم الجوال بضغطة، وفيها زر واتساب لو تغيّرت الخطط. التذكيرات التلقائية عبر واتساب قادمة قريباً.', 1),
        ('اضغطي على الحجز لتأكدي وصولهم.', 'اضغطوا على الحجز لتسجيل وصولهم.', 1),
        ('أربع خصائص <span class="it">لا توفّرها</span> أي منصة في الخليج.', 'أربع خصائص <span class="it">مصممة</span> لمطاعم الخليج.', 1),
        ('تأكيدات واتساب.<', 'واتساب على بُعد ضغطة.<', 1),
        ('الضيف ما يحمّل شيء، ولا يسجّل في حساب. التأكيد يصله في واتساب — التطبيق اللي يفتحه ٤٠ مرة في اليوم — مع رابط لتعديل الحجز.',
         'الضيف لا يحمّل شيئاً ولا يسجّل في حساب. صفحة الحجز وكل تأكيد فيهما زر واتساب يفتح محادثة معكم. التأكيدات والتذكيرات التلقائية عبر واتساب قادمة قريباً، وحتى ذلك الحين يصلكم بريد مع كل حجز جديد.', 1),
        ('التذكيرات تحمل التقويمين. حجوزات إفطار رمضان تعمل. حجوزات العيد تعمل. صباح الجمعة وقت الصلاة محجوز افتراضياً للسعودية.',
         'صفحة الحجز تعرض التقويمين. حجوزات إفطار رمضان والعيد تعمل مثل أي ليلة، وصباح الجمعة مغلق افتراضياً في السعودية، وإغلاقات الإجازات تُضاف في ثوانٍ.', 1),
        ('موعد يتذكر أسمائهم، طاولتهم المفضلة، الحساسية اللي دوّنتموها آخر مرة.',
         'موعد يحفظ الاسم والرقم وعدد الزيارات والحساسية التي دوّنتموها آخر مرة.', 1),
        ('لا رسوم إضافية للرسائل أو الدعم.', 'لا رسوم إضافية على الدعم.', 1),
        ('خطة المطاعم', 'باقة الاستوديو', 1),
        ('حجوزات غير محدودة · تأكيدات واتساب وبريد · تذكيرات تراعي التقويم الهجري · سجل ضيوف قابل للبحث · صفحة حجز ثنائية اللغة · تجربة مجانية ٧ أيام',
         'حجوزات غير محدودة · تنبيهات الحجز بالبريد · زر محادثة واتساب · صفحة حجز بالهجري والميلادي · سجل ضيوف قابل للبحث · صفحة حجز ثنائية اللغة · تجربة مجانية ٧ أيام', 1),
        ('التأكيد يصل في واتساب. هم ما يسجّلون في أي حساب.', 'يرون التأكيد مباشرة، ولا يسجّلون في أي حساب.', 1),
        ('شهرياً للمطاعم.', 'شهرياً في باقة الاستوديو.', 1),
        ('المضيفة تسجّل الواقفين على اللوحة عشان يبقى عندكم مصدر واحد لمن في المطعم.',
         'واللوحة تعرض حجوزات الليلة بالساعة، فيعرف فريقكم بالضبط ما هو محجوز.', 1),
        ('نعم. كل تأكيد يحتوي رابط تعديل أو إلغاء. التغيير يصل لوحتكم فوراً، فالمضيفة دائماً تشوف الحقيقة الكاملة.',
         'نعم. يضغط الضيف زر واتساب في صفحة التأكيد ليراسلكم، ويلغي فريقكم الحجز القديم ويرسل له رابط الحجز ليختار وقتاً جديداً. التعديل والإلغاء بضغطة من الضيف نفسه ضمن خطتنا القادمة.', 1),
        ('نعم، افتراضياً للضيوف اللي جوالاتهم بالعربية.', 'نعم، تلقائياً للضيوف الذين لغة جوالاتهم العربية.', 1),
        ('توقّفي عن إدارة الحجوزات على <span class="it">الورق.</span>', 'كفى إدارة الحجوزات على <span class="it">الورق.</span>', 1),
        ('تجربة مجانية ٧ أيام. لا حاجة لبطاقة لمشاهدة العرض التوضيحي. ألغي وقتما شئتِ.',
         'تجربة مجانية ٧ أيام. يمكنكم الإلغاء في أي وقت.', 1),
    ],
}

# Shared Arabic CTA / trial wording on both vertical pages (order matters:
# longer phrases first).
AR_COMMON = [
    ('ابدئي التجربة المجانية', 'بدء التجربة المجانية'),
    ('ابدئي تجربة مجانية', 'بدء التجربة المجانية'),
    ('ابدئي التجربة', 'بدء التجربة'),
    ('جرّبي مجاناً ٧ أيام', 'جرّبوا مجاناً ٧ أيام'),
    ('تكلّمي مع المبيعات', 'تواصلوا مع المبيعات'),
    ('تكلّمي معنا', 'تواصلوا معنا'),
    ('قارني الباقات', 'مقارنة الباقات'),
    ('ألغي قبل اليوم الثامن ولن يُخصم منكِ شيء.', 'ألغوا قبل اليوم الثامن ولن يُخصم منكم شيء.'),
    ('ألغي وقتما شئتِ.', 'يمكنكم الإلغاء في أي وقت.'),
]


def apply(s, old, new, count, label):
    if isinstance(old, re.Pattern):
        n = len(old.findall(s))
        if n != count:
            raise SystemExit(f'{label}: regex matched {n}, expected {count}: {old.pattern[:60]}')
        return old.sub(new, s)
    n = s.count(old)
    if (count is ALL and n == 0) or (count is not ALL and n != count):
        raise SystemExit(f'{label}: found {n}, expected {count}: {old[:80]}')
    return s.replace(old, new)


import sys
ONLY = set(sys.argv[1:])  # optional: limit to specific pages
for rel, edits in EDITS.items():
    if ONLY and rel not in ONLY:
        continue
    p = ROOT / rel
    s = p.read_text()
    for old, new, count in edits:
        if old == 'WA':
            lang, venue, outgoing, reply = new
            if len(WA_OLD.findall(s)) != 1:
                raise SystemExit(f'{rel}: WhatsApp bubble block not found exactly once')
            s = WA_OLD.sub(lambda _m: wa_block(lang, venue, outgoing, reply), s)
            continue
        s = apply(s, old, new, count, rel)
    if rel.startswith('ar/'):
        for old, new in AR_COMMON:
            if old in s:
                s = s.replace(old, new)
    p.write_text(s)
    print(rel, 'ok')
