txt_choose_lang = "Tilni tanlang / Выберите язык"

txt_greeting = {
    'uz': "Assalomu alaykum!😃\n\n<b>'Forward school'</b>ning virtual yordamchi botiga xush kelibsiz.",
    'ru': 'Здравствуйте!😃\n\nДобро пожаловать в виртуальный бот-помощник <b>Forward school.</b>'
}

txt_phone_request = {
    'uz': "📱 Sizning telefon raqamingiz? Raqamingizni <b>+998 ** *** ****</b> shaklida <b>kiriting</b> yoki "
          "<b>yuboring</b>",
    'ru': "📱 Ваш номер телефона? Отправьте или введите <b>ваш номер</b> телефона в виде: <b>+998 ** *** ****</b>"
}

sms_text = {
    'uz': 'Forward School Sizga maxsus kod yubordi! - {}. Uni hech kimga bermang!',
    'ru': 'Forward School отправил вам секретный код - {}. Никому его не сообщайте!'
}

code_sent = {
    'uz': "Siz tergan raqamga kod yuborildi. O'sha raqamni tering",
    'ru': 'На данный номер был отправлен код. Пожалуйста введите его сюда'
}

phone_country_error = {
    'uz': "❗️ Hozir biz faqat O'zbekiston raqamlarini qabul qilamiz",
    'ru': "❗️ Сейчас мы принимаем только номера в Узбекистане"
}

code_resent = {
    'uz': "Kod qaytadan yuborildi.",
    'ru': 'Код переотправлен.'
}

txt_name_request = {
    'uz': "Ism va familiyangizni kiritng",
    'ru': "Введите имя и фамилию"
}

name_error_1 = {
    'uz': "Ism va Familiyani to'liq kiriting",
    'ru': "Введите имя и фамилию полностью"
}
name_error_2 = {
    'uz': "Ism yoki Familiya katta xarf bilan boshlanishi kerak",
    'ru': "Ошибка при написании имени. Имя и Фамилия начинаются с заглавной буквы"
}

code_error = {
    'uz': "Kod noto'g'ri. Qaytadan tering yoki telefon raqamni o'zgartiring",
    'ru': "Код неверный. Попробуйте ввести код заново или измените номер телефона"
}

name_accepted = {
    'uz': 'Qabul qilindi!',
    'ru': 'Принято!'
}

main_menu_markup = {
    'uz': "Asosiy sahifa:",
    'ru': "Главная страница:"
}

# Ask Me Markup Text
amm_text = {
    'uz': 'Kimga savol beramiz?',
    'ru': 'Кому зададим вопрос?'
}

# Get Info Markup text
gim_text = {
    'uz': "Qaysi kurs haqida ma'lumot olishni hohlaysiz?",
    'ru': 'Какой курс вас интересует?'
}

# Watch Video Markup text
wvm_text = {
    'uz': "Videolardan birini tanlang",
    'ru': "Выберите один из видеороликов"
}

# Test Knowledge Markup text
ptm_text = {
    'uz': """🤓 Siz FORWARD SCHOOL test sinov bo'limidasiz!
    
🧠 Bu bo'limda ingiliz tili darajangizni sinab ko'rishingiz mumkin

🔑 Testni boshlash uchun sizga maxsus <code>kod</code> kerak bo'ladi, uni maktabimiz administratorlaridan olishingiz mumkin""",
    'ru': """🤓 Сейчас вы в разделе тестирования!

🧠 Здесь вы можете проверить уровень своего английского языка

🔑 Получите специальный <code>код</code> от администратора школы и проходите тест"""
}

settings_markup_text = {
    'uz': "Sizga qanday yordam berishim mumkin?",
    'ru': "Чем могу вам помочь?"
}

quiz_password_txt = {
    'request': {
        'uz': "🔒 Administrator tomonidan berilgan maxsus kodni tering",
        'ru': "🔒 Введите специальный код, предоставленный администратором школы"
    },
    'confirm': {
        'uz': "🔓 Muvaffaqiyatli!",
        'ru': "🔓 Успешно!"
    },
    'reject': {
        'uz': "❌ Noto'g'ri kod terildi! Qayta urinib ko'ring yoki administrator bilan bog'laning",
        'ru': "❌ Неправильный код! Повторите попытку или свяжитесь с администратором"
    }
}

text_quiz_instructions = {
    'uz': """Tayyorlaning! Placement test boshlanmoqda!
    
Batafsil ma'lumot: 
⁉️ Savollar Beginner darajasidan boshlanib, Vocabulary bilan tugaydi 

✍️ 50 ta test 
⏳ 25 daqiqa

<b>Natijalar shkalasi:</b> 
0 - 15: Beginner 
16 - 24: Elementary 
25 - 32: Pre-Intermediate 
33 - 39: Intermediate 
40 - 45: Upper Intermediate
46 - 50: Advanced 

Agar siz tayyor bo'lsangiz, tugmani bosing va biz boshlaymiz! 🚀""",
    'ru': """🧠 Готовьтесь! Placement Test начинается!
    
Инструкции к тестируемому:
⁉️ Вопросы начинаются с уровня Beginner и заканчиваются с Vocabulary

✍️ 50 тестов
⏳ 25 минут

<b>Шкала оценок уровней:</b>
0 - 15: Beginner
16 - 24: Elementary
25 - 32: Pre-Intermediate
33 - 39: Intermediate
40 - 45: Upper Intermediate
46 - 50: Advanced

Если готов, жми кнопку, и мы начнём! 🚀"""
}

quiz_finished_text = {
    'uz': """Tabriklaymiz! 🥳

Siz testni muvaffaqiyatli tugatdingiz

Sizning natijangiz: <b>{}/50</b>
Ingiliz tili darajasi: <b>{}</b>""",
    'ru': """Поздравляем! 🥳
    
Вы благополучно закончили тест

Ваш результат: <b>{}/50</b>
Уровень английского языка: <b>{}</b>"""
}
quiz_thank_you = {
    'uz': "Testda qatnashganingiz uchun rahmat!",
    'ru': "Спасибо за участие в тесте!"
}

intensive_6_txt = {
    'uz': """<b>Intensive 6+</b>

✅ Ingliz tilini endi boshlaganlar uchun. 

⏰ Bir hafta - 6 ta mashg‘ulot
⏳ Dars davomiyligi: 180 daqiqa
🎒 Kurs davomiyligi: 4 oy

🥳 Siz bemalol bizning tadbirlarda qatnashishingiz, professionallardan qo'shimcha bilim olishingiz mumkin😌

Batafsil ma'lumot uchun: 
📞 + 998 95 144 22 12 

🤩 Yangi imkoniyatlarni kashf etish vaqti keldi!

😌 60 dan ortiq o‘quvchilar bu imkoniyatlardan muntazam foydalanib kelmoqdalar""",
    'ru': """<b>Intensive 6+</b>

✅ Для тех, кто только начинает изучать английский язык.

⏰ Часота: 6 раз в неделю 
⏳ Длительность: 180 минут 
🎒 Продолжительность: 4 месяца

🥳 Сможете участвовать в наших мероприятиях, получить дополнительные знания от профессионалов 

Для подробной информации:
📞+998 95 144 22 12

🤩 Пора открывать новые возможности!

😌 Более 60 учеников полностью доверились нам"""
}
intensive_7_txt = {
    'uz': """<b>Intensive 7+</b>

✅ Kursga intermediate darajasiga ega bo‘lganlar qabul qilinadi. 

⏰ Bir hafta - 6 ta mashg‘ulot
⏳ Dars davomiyligi: 180 daqiqa
🎒 Kurs davomiyligi: 4 oy

 🤩 Qo'shimcha darslarda va  turli xil tadbirlarda qatnashishingiz, bilimingizni oshirishingiz mumkin.

 Batafsil ma'lumot uchun:
 📞 + 998 95 144 22 12 

😉 Vaqtingizni va pulingizni tejash imkoniyatini boy bermang.

😌 35 dan ortiq o‘quvchilar o‘z qarorlarini qabul qilib bo‘ldilar""",
    'ru': """<b>Intensive  7+</b>

✅ На курс принимаются ученики на уровне intermediate. 

⏰ Частота: 6 раз в неделю 
⏳ Длительность занятий: 180 минут
🎒 Продолжительность курса: 3 месяца

🤩 Также вы сможете принять участие в различных мероприятиях и улучшить свои знания на дополнительных занятиях.

Подробнее можете узнать по номеру:
📞 +998 95 144 22 12

😉 Не упустите свой шанс сэкономить свое время и деньги
😌 Свыше 35 учеников уже сделали правильный выбор"""
}
general_english_txt = {
    'uz': """<b>General English</b> 

✅ Darslar Amerika ta'lim tizimi (jahon standartiga) muvofiq olib boriladi. 

⏰ Bir hafta - 3ta mashg‘ulot
⏳ Darslar davomiyligi: 90 minut
🎒 Kurs davomiyligi: 3 oy

🥳 Shuningdek, sizni turli tadbirlar va qo'shimcha darslar kutmoqda (9-19 tizimi)

Batafsil ma'lumot uchun:
📞 + 998 95 144 22 12 

😌 Darslarning sifatini kafolatlaydigan maxsus bo'lim mavjud

🤝 100 dan ko‘proq inson bizga ishonishadi""",
    'ru': """<b>General English</b>

✅ Уроки проводятся по американской системе обучения (мировой стандарт изучения английского языка)

⏰ Частота: 3 раза в неделю
⏳ Длительность занятий: 90 минут
🎒 Продолжительность курса: 3 месяца

🥳 А еще вас ждут различные мероприятияб а также дополнительные занятия (система 9-19)

🙌 Более 100 человек уже доверяют нам

Подробнее можете узнать по номеру:
📞 +998 95 144 22 12"""
}
ielts_txt = {
    'uz': """<b>IELTS</b>

✅ Darslar Amerika o'qitish tizimi (jahon standarti) bo'yicha o‘tiladi.

😌 Ortiqcha mashaqqatsiz o'z ballarini oshirishni istaganlar uchun. 

 Kurs haqida qo'shimcha ma'lumotni quyidagi raqamga qo'ng'iroq qilib bilib olishingiz mumkin. 
📞 + 998 95 144 22 12 

📑 Shuningdek, siz uchun oyiga 2 marta mock exam o‘tkaziladi.""",
    'ru': """<b>IELTS</b> 

✅Уроки проводятся по американской системе обучения (мировой стандарт)

😌 Курс для тех, кто желает повысить свой балл без особой нагрузки. Удобный график работы. 

Подробно о курсе вы сможете узнать, позвонив по номеру:
📞+998 95 144 22 12

📑 Также 2 раза в месяц для вас будут проводиться Mock экзамены"""
}

ask_support_got = {
    'uz': "Qabul qildik! Academic Support siz bilan bog'lanadi",
    'ru': "Приняли! Academic Support с вами свяжется"
}
ask_teachers_got = {
    'uz': "Qabul qildik! O'qituvchilarimiz siz bilan bog'lanadi",
    'ru': 'Приняли! Учителя с вами свяжутся'
}
ask_administration_got = {
    'uz': "Qabul qildik! Administratsiya siz bilan bog'lanadi",
    'ru': 'Приняли! Администрация с вами свяжется'
}

ask_finance_got = {
    'uz': "Qabul qildik! Moliya bo'limi siz bilan bog'lanadi",
    'ru': 'Приняли! Финансовый отдел с вами свяжется'
}

asking_texts = {
    -1001361079718: {
        'uz': 'bla bla',
        'ru': 'russish bla bla'
    },
    -1001221591327: {
        'uz': "Academic Supportga o'z murojaatingizni yuboring😊",
        'ru': "Отправьте свой запрос нашему Academic Support😊"
    },
    -1001352926506: {
        'uz': "O'qituvchilarimizga o'z murojaatingizni yuboring😊",
        'ru': "Отправьте свой запрос нашим учителям😊"
    },
    -1001312359770: {
        'uz': "Administratorlarimizga o'z murojaatingizni yuboring😊",
        'ru': "Отправьте свой запрос нашим администраторам😊"
    },
    -1001393166508: {
        'uz': "Moliya bo'limi ma'sullarimizga o'z murojaatingizni yuboring😊",
        'ru': "Отправьте свой запрос нашим финансистам😊"
    }
}

gotcha_texts = {
    -1001361079718: {
        'uz': 'bla bla',
        'ru': 'russish bla bla'
    },
    -1001221591327: {
        'uz': "Qabul qildim. Academic Support guruhiga yubordim ;)",
        'ru': "Принял. Отправил в группу Academic Support ;)"
    },
    -1001352926506: {
        'uz': "Qabul qildim. O'qituvchilarimizga yubordim ;)",
        'ru': "Принял. Отправил в группу учителей ;)"
    },
    -1001312359770: {
        'uz': "Qabul qildim. Administratorlarimizga yubordim ;)",
        'ru': "Принял. Отправил в группу администраторов ;)"
    },
    -1001393166508: {
        'uz': "Qabul qildim. Moliyachilarimizga yubordim ;)",
        'ru': "Принял. Отправил в группу финансистов ;)"
    }
}

txt_reply = {
    'uz': "🔔 Yangi xabar!\n\n<b>{}</b>",
    'ru': "🔔 Новое уведомление!\n\n<b>{}</b>"
}

video_1_caption = {
    'uz': "",
    'ru': """🤩 FORWARD SCHOOL – одна большая семья, которая может достичь всего, работая вместе 
😉 Присоединяйтесь к нам и откройте для себя новые возможности"""
}
video_2_caption = {
    'uz': "",
    'ru': """📚 У нас проводятся различные мастер-классы, где повысить свои знания вам помогут сразу 5 специалистов
🥰 Присоединяйтесь к нашей семье и почувствуйте всю атмосферу️"""
}
video_3_caption = {
    'uz': "",
    'ru': """🎬 Благодаря нашим онлайн-урокам, вы сможете получить знания и не выходя из дома
👩‍🏫 Ну если вам не хватает этого, то можете смело приходить к нам в школу"""
}