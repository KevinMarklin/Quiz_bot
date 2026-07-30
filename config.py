from dataclasses import dataclass
import toml
import os
from dotenv import load_dotenv


@dataclass
class Telegram:
    bot_token: str


@dataclass
class Database:
    dsn: str


@dataclass
class Config:
    telegram: Telegram
    database: Database

    @classmethod
    def from_file(cls, path: str) -> "Config":
        # Загружаем .env (если есть)
        load_dotenv()

        # Загружаем config.toml (если файл существует)
        config_data = {}
        if os.path.exists(path):
            config_data = toml.load(path)

        # --- Получаем bot_token ---
        env_token = os.getenv("BOT_TOKEN")
        if env_token:
            if "telegram" not in config_data:
                config_data["telegram"] = {}
            config_data["telegram"]["bot_token"] = env_token

        bot_token = config_data.get("telegram", {}).get("bot_token")
        if not bot_token:
            raise RuntimeError("BOT_TOKEN не найден ни в .env, ни в config.toml")

        # --- Получаем DATABASE_URL ---
        # 1. Проверяем переменные окружения (.env)
        dsn = os.getenv("DATABASE_URL")

        # 2. Если в .env пусто, берем из config.toml
        if not dsn or dsn.strip() == "":
            dsn = config_data.get("database", {}).get("dsn", "")

        # 3. Если и там пусто, используем дефолтный хост 'db' для Docker Compose
        if not dsn or dsn.strip() == "":
            dsn = "postgresql+asyncpg://bot:bot@db:5432/bot"

        # Преобразуем префиксы в асинхронный asyncpg драйвер
        if dsn.startswith("postgres://"):
            dsn = dsn.replace("postgres://", "postgresql+asyncpg://", 1)
        elif dsn.startswith("postgresql://"):
            dsn = dsn.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif "psycopg2" in dsn:
            dsn = dsn.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

        return cls(
            telegram=Telegram(bot_token=bot_token),
            database=Database(dsn=dsn),
        )




FRIEND_TEST = [
    {
        "question": "🌙 В каком месяце у тебя день рождения?",
        "question_for_user": "В каком месяце у него/неё день рождения",
        "answer_back": "🌙 День рождения в ",
        "image_url": "https://static.foxnews.com/foxnews.com/content/uploads/2020/04/iStock-184332537.jpg",
        "answers": [
            {"text": "❄️Январь"},
            {"text": "💘Февраль"},
            {"text": "🌷Март"},
            {"text": "🌷Апрель"},
            {"text": "🌷Май"},
            {"text": "️☀️Июнь"},
            {"text": "🍉Июль"},
            {"text": "🌞Август"},
            {"text": "🍂Сентябрь"},
            {"text": "🍂Октябрь"},
            {"text": "🍁Ноябрь"},
            {"text": "❄️Декабрь"},

        ]
    },

    {
        "question": "🥛 Твой любимый напиток?",
        "image_url": "https://versiya.info/uploads/posts/2020-03/1584239824_photo_2020-03-15_11-36-16.jpg",
        "question_for_user": "🥛 Его/её любимый напиток",
        "answer_back": "🥛 Любимый напиток ",
        "answers": [
            {"text": "🍺Алкоголь"},
            {"text": "☕️Кофе"},
            {"text": "🍋Газировка"},
            {"text": "🧃Сок"},
            {"text": "🍵Чай"},
        ]
    },
    {
        "question": "🏞 Какое время года ты предпочитаешь?",
        "image_url": "https://trikky.ru/wp-content/blogs.dir/1/files/2022/12/01/2022-12-01-12-21-11.jpg",
        "question_for_user": "🏞 Его/её любимое время года",
        "answers": [
            {"text": "❄️Зима"},
            {"text": "💐Весна"},
            {"text": "☀️Лето"},
            {"text": "🍂Осень"},
        ]
    },

{
        "question": "🦶 Твой размер ноги?",
        "image_url": "https://cs12.pikabu.ru/post_img/2021/09/10/10/og_og_1631290171258795964.jpg",
        "question_for_user": "🦶 Его/её размер ноги",
        "answers": [
            {"text": "📏35-36"},
            {"text": "📐37-38"},
            {"text": "🤏39-40"},
            {"text": "↔40-41"},
            {"text": "📐42-43"},
            {"text": "↕44-45"},
        ]
    },

{
        "question": "📖 Твой любимый школьный предмет?",
        "image_url": "https://kartinki.pics/uploads/posts/2022-03/1646955831_66-kartinkin-net-p-uchebnie-prinadlezhnosti-kartinki-74.jpg",
        "question_for_user": "📖 Его/её любимый школьный предмет?",
        "answers": [
            {"text": "🖩Математика"},
            {"text": "⚛Физика"},
            {"text": "🇷🇺Русский язык"},
            {"text": "💂Английский язык"},
            {"text": "💻Информатика"},
            {"text": "🌎География"},
            {"text": "⚽Физкультура"},
            {"text": "￼ОБЖ"},
            {"text": "🖌️ИЗО"},
            {"text": "♪Музыка"},
            {"text": "📚Литература"},
            {"text": "🧪Химия"},
            {"text": "📜История"},
            {"text": "🎓Обществознание"},
            {"text": "🛠️Технология"},
            {"text": "🇪🇸Испанский язык"},
        ]
    },

{
        "question": "🤤 Твоё любимое хобби?",
        "image_url": "https://kartinki.pics/uploads/posts/2022-12/thumbs/1671729543_kartinkin-net-p-khobbi-kartinki-dlya-detei-instagram-11.jpg",
        "question_for_user": "🤤 Его/её любимое хобби",
        "answers": [
            {"text": "💃Танцы"},
            {"text": "📖Чтение"},
            {"text": "️‍♀️Спорт"},
            {"text": "🎨Рисование"},
            {"text": "🎥Съёмка"},
            {"text": "➰Бисероплетение"},
        ]
    },

{
        "question": "🌼 Твой любимый цвет?",
        "image_url": "https://www.mindful.org/content/uploads/How-the-Arts-Can-Bring-Healing-to-Healthcare-1024x640.png",
        "question_for_user": "🌼 Его/её любимый цвет",
        "answers": [
            {"text": "🔴Красный"},
            {"text": "🟠Оранжевый"},
            {"text": "🟡Жёлтый"},
            {"text": "🟢Зелёный"},
            {"text": "🟦Голубой"},
            {"text": "🔵Синий"},
            {"text": "🟣Фиолетовый"},

        ]
    },

{
        "question": "👀 Твой цвет глаз?",
        "image_url": "https://i.pinimg.com/originals/56/8c/2c/568c2c50ea205d701c8115499cf14e3a.jpg",
        "question_for_user": "👀 Его/её цвет глаз",
        "answers": [
            {"text": "🟢Зелёные"},
            {"text": "🟦Голубые"},
            {"text": "⚪Серые"},
            {"text": "🟤Карие"},
        ]
    },

{
        "question": "😝 Твой любимый фрукт?",
        "image_url": "https://avatars.dzeninfra.ru/get-zen_doc/1708669/pub_5ddd8239a29ee0330b851fd6_5ddd853c3112ab60c7359559/scale_1200",
        "question_for_user": "😝 Его/её любимый фрукт",
        "answers": [
            {"text": "🍎Яблоко"},
            {"text": "🍌Банан"},
            {"text": "🥭Манго"},
            {"text": "🍊Апельсин"},
            {"text": "🍊Мандарин"},
            ]
    },

{
        "question": "💪 Твой любимый вид спорта?",
        "image_url": "https://mmkids.ru/wp-content/uploads/4/8/0/4805ee8e4f6ec25a166306b98205857e.jpeg",
        "question_for_user": "💪 Его/её любимый вид спорта",
        "answers": [
            {"text": "🏐Волейбол"},
            {"text": "⚽Футбол"},
            {"text": "🏀Баскетбол"},
            {"text": "🏊Плаванье"},
            {"text": "🏃Бег"},
            {"text": "🏒Хоккей"},
            {"text": "🌎Другое"},
        ]
    },

{
        "question": "🎥 Что тебе больше всего нравится смотреть?",
        "image_url": "https://static.mk.ru/upload/entities/2022/12/14/11/articles/facebookPicture/8e/55/ce/99/68b8a22b6052c0b5dcf70f85347ce007.jpg",
        "question_for_user": "🎥 Ему/ей нравится смотреть",
        "answers": [
            {"text": "🎞️Сериал"},
            {"text": "🎬Фильм"},
            {"text": "▷Мультик"},
        ]
    },

]












ALL_QUESTIONS_LIST = [
    {
        "question": "🌙 В каком месяце у тебя день рождения?",
        "question_for_user": "В каком месяце у него/неё день рождения",
        "answer_back": "🌙 День рождения в ",
        "image_url": "https://static.foxnews.com/foxnews.com/content/uploads/2020/04/iStock-184332537.jpg",
        "answers": [
            {"text": "❄️Январь"},
            {"text": "💘Февраль"},
            {"text": "🌷Март"},
            {"text": "🌷Апрель"},
            {"text": "🌷Май"},
            {"text": "️☀️Июнь"},
            {"text": "🍉Июль"},
            {"text": "🌞Август"},
            {"text": "🍂Сентябрь"},
            {"text": "🍂Октябрь"},
            {"text": "🍁Ноябрь"},
            {"text": "❄️Декабрь"},
        ],
        "id": "1"
    },

    {
        "question": "🥛 Твой любимый напиток?",
        "image_url": "https://versiya.info/uploads/posts/2020-03/1584239824_photo_2020-03-15_11-36-16.jpg",
        "question_for_user": "🥛  Его/ её любимый напиток",
        "answer_back": "🥛 Любимый напиток ",
        "answers": [
            {"text": "🍺Алкоголь"},
            {"text": "☕️Кофе"},
            {"text": "🍋Газировка"},
            {"text": "🧃Сок"},
            {"text": "🍵Чай"},
        ],
        "id": "2"
    },
    {
        "question": "🏞 Какое время года ты предпочитаешь?",
        "image_url": "https://trikky.ru/wp-content/blogs.dir/1/files/2022/12/01/2022-12-01-12-21-11.jpg",
        "question_for_user": "🏞 Его/её любимое время года",
        "answers": [
            {"text": "❄️Зима"},
            {"text": "💐Весна"},
            {"text": "☀️Лето"},
            {"text": "🍂Осень"},
        ],
        "id": "3"
    },


    {
        "question": "🦶 Твой размер ноги?",
        "image_url": "https://cs12.pikabu.ru/post_img/2021/09/10/10/og_og_1631290171258795964.jpg",
        "question_for_user": "🦶 Его/её размер ноги",
        "answers": [
            {"text": "📏35-36"},
            {"text": "📐37-38"},
            {"text": "🤏39-40"},
            {"text": "↔40-41"},
            {"text": "📐42-43"},
            {"text": "↕44-45"},
        ],
        "id": "4"
    },


    {
        "question": "🤤 Твоё любимое хобби?",
        "image_url": "https://kartinki.pics/uploads/posts/2022-12/thumbs/1671729543_kartinkin-net-p-khobbi-kartinki-dlya-detei-instagram-11.jpg",
        "question_for_user": "🤤 Его/её любимое хобби",
        "answers": [
            {"text": "💃Танцы"},
            {"text": "📖Чтение"},
            {"text": "️‍♀️Спорт"},
            {"text": "🎨Рисование"},
            {"text": "🎥Съёмка"},
            {"text": "➰Бисероплетение"},
        ],
        "id": "5"
    },

    {
        "question": "🌼 Твой любимый цвет?",
        "image_url": "https://www.mindful.org/content/uploads/How-the-Arts-Can-Bring-Healing-to-Healthcare-1024x640.png",
        "question_for_user": "🌼 Его/её любимый цвет",
        "answers": [
            {"text": "🔴Красный"},
            {"text": "🟠Оранжевый"},
            {"text": "🟡Жёлтый"},
            {"text": "🟢Зелёный"},
            {"text": "🟦Голубой"},
            {"text": "🔵Синий"},
            {"text": "🟣Фиолетовый"},

        ],
        "id": "6"
    },

    {
        "question": "👀 Твой цвет глаз?",
        "image_url": "https://i.pinimg.com/originals/56/8c/2c/568c2c50ea205d701c8115499cf14e3a.jpg",
        "question_for_user": "👀 Его/её цвет глаз",
        "answers": [
            {"text": "🟢Зелёные"},
            {"text": "🟦Голубые"},
            {"text": "⚪Серые"},
            {"text": "🟤Карие"},
        ],
        "id": "7"
    },

    {
        "question": "😝 Твой любимый фрукт?",
        "image_url": "https://avatars.dzeninfra.ru/get-zen_doc/1708669/pub_5ddd8239a29ee0330b851fd6_5ddd853c3112ab60c7359559/scale_1200",
        "question_for_user": "😝 Его/её любимый фрукт",
        "answers": [
            {"text": "🍎Яблоко"},
            {"text": "🍌Банан"},
            {"text": "🥭Манго"},
            {"text": "🍊Апельсин"},
            {"text": "🍊Мандарин"},
            ],
        "id": "8"

    },

    {
        "question": "💪 Твой любимый вид спорта?",
        "image_url": "https://mmkids.ru/wp-content/uploads/4/8/0/4805ee8e4f6ec25a166306b98205857e.jpeg",
        "question_for_user": "💪 Его/её любимый вид спорта",
        "answers": [
            {"text": "🏐Волейбол"},
            {"text": "⚽Футбол"},
            {"text": "🏀Баскетбол"},
            {"text": "🏊Плаванье"},
            {"text": "🏃Бег"},
            {"text": "🏒Хоккей"},
            {"text": "🌎Другое"},
        ],
        "id": "9"
    },

    {
        "question": "🎥 Что тебе больше всего нравится смотреть?",
        "image_url": "https://static.mk.ru/upload/entities/2022/12/14/11/articles/facebookPicture/8e/55/ce/99/68b8a22b6052c0b5dcf70f85347ce007.jpg",
        "question_for_user": "🎥 Ему/ей нравится смотреть",
        "answers": [
            {"text": "🎞️Сериал"},
            {"text": "🎬Фильм"},
            {"text": "▷Мультик"},
        ],
        "id": "10"
    },


    {
        "question": "🗓 Какой день недели твой любимый?",
        "image_url": "https://mur-mur.top/uploads/posts/2023-04/1682371715_mur-mur-top-p-otkritki-kalendar-na-kazhdii-den-krasivo-13.jpg",
        "question_for_user": "🗓 Какой день недели его/её любимый?",
        "answers": [
            {"text": "📅Понедельник"},
            {"text": "🔟Вторник"},
            {"text": "⌛️Среда"},
            {"text": "🏙Четверг"},
            {"text": "📆Пятница"},
            {"text": "🌌Суббота"},
            {"text": "🗓Воскресенье"},
        ],
        "id": "11"
    },

    {
        "question": "📱 Какое развлекательное приложение ты предпочитаешь?",
        "image_url": "https://avatars.mds.yandex.net/i?id=71bcc23c6f81adfaea00cf389f3f2a5d_l-5146789-images-thumbs&n=13",
        "question_for_user": "📱 Какое развлекательное приложение он/она предпочитает?",
        "answers": [
            {"text": "▶️YoTube"},
            {"text": "💌Instagram"},
            {"text": "🌐TikTok"},
            {"text": "🤳Likee"},
            {"text": "💻VK"},
            {"text": "🔗Telegram"},
        ],
        "id": "12"
    },

    {
        "question": "❓ Кто ты?",
        "image_url": "https://avatars.dzeninfra.ru/get-zen_doc/5283265"
                     "/pub_63352a15a8b88a163ae44c7b_6335333d0140f345a2c42f70/scale_1200",
        "question_for_user": "❓ Кто она/он?",
        "answers": [
            {"text": "🧑‍🤝‍🧑Экстраверт"},
            {"text": "🧍Интроверт?"},
        ],
        "id": "13"
    },

    {
        "question": "💬 Какое общение ты предпочитаешь?",
        "image_url": "https://t4.ftcdn.net/jpg/01/41/38/11/360_F_141381130_uS0EJ5cFlfASuWSYuCOAuivWDnLBEGoz.jpg",
        "question_for_user": "💬 Какое общение он/она предпочитает?",
        "answers": [
            {"text": "👫Живое"},
            {"text": "🌐Соц.сети"},
            {"text": "📱По телефону"},
            {"text": "🗣Не люблю общаться"},

        ],
        "id": "14"
    },

    {
        "question": "🌎 В жизни ты бы не смог/-ла обойтись без...",
        "image_url": "https://cerenas.club/uploads/posts/2022-12/1671112372_cerenas-club-p-semya-za-stolom-instagram-82.jpg",
        "question_for_user": "🌎 В жизни он/она не смог/-ла бы обойтись без...",
        "answers": [
            {"text": "🎮Игр"},
            {"text": "🧑‍🤝‍🧑Друзей"},
            {"text": "🍔Еды"},

        ],
        "id": "15"
    },

    {
        "question": "🗣 Как ты разговариваешь?",
        "image_url": "https://dz2cdn1.dzone.com/storage/article-thumb/6280713-thumb.jpg",
        "question_for_user": "🗣 Как он/она разговаривает?",
        "answers": [
            {"text": "🔊Громко"},
            {"text": "🔕Шёпотом"},
            {"text": "😃Нормально"},

        ],
        "id": "16"
    },

    {
        "question": "⭐️ Какой ты знак зодиака?",
        "image_url": "https://www.proprofs.com/quiz-school/topic_images/p18mk4soe36qmf40t0v1acs1rus3.jpg",
        "question_for_user": "️⭐ Какой он/она знак зодиака?",
        "answers": [
            {"text": "♈️Овен"},
            {"text": "♉️Телец"},
            {"text": "♊️Близнецу"},
            {"text": "♋️Рак"},
            {"text": "♌️Лев"},
            {"text": "♍️Дева"},
            {"text": "♎️Весы"},
            {"text": "♏️Скорпион"},
            {"text": "♐️Стрелец"},
            {"text": "♑️Козерог"},
            {"text": "♒️Водолей"},
            {"text": "♓️Рыбы"},

        ],
        "id": "17"
    },

    {
        "question": "🎂 Любимый твой десерт?",
        "image_url": "https://avatars.mds.yandex.net/i?id=e453d60a94fa42750b828037b2e123b817d198db-9153855-images-thumbs&n=13",
        "question_for_user": "🎂 Любимый его/её десерт",
        "answers": [
            {"text": "🍦Мороженое"},
            {"text": "🍬Мармелад"},
            {"text": "🎂Торт"},
            {"text": "🍫Шоколад"},
            {"text": "🍨Суфле"},
            {"text": "🥧Пирог"},
            {"text": "🍬Конфеты"},

        ],
        "id": "18"
    },

    {
        "question": "☀️ Любимая погода",
        "image_url": "https://wallpapers.com/images/hd/marvelous-window-raindrops-love-background-z1g44rat6dhmzc2t.jpg",
        "question_for_user": "☀️ Любимая его/её погода",
        "answers": [
            {"text": "🌧Дождливая"},
            {"text": "☀️Солнечная"},
            {"text": "😶‍🌫️Туманная"},
            {"text": "⛅️Пасмурная"},
            {"text": "🌨Снегопад"},
        ],
        "id": "19"
    },




]

