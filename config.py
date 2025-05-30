from dataclasses import dataclass
import toml


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
        config = toml.load(path)
        return cls(
            telegram=Telegram(
                **config["telegram"],
            ),
            database=Database(
                **config["database"]
            )
        )




FRIEND_TEST = [
    {
        "question": "В каком месяце у тебя день рождения?",
        "question_for_user": "В каком месяце у него/неё день рождения",
        "answer_back": "День рождения в ",
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
        "question": "Твой любимый напиток?",
        "image_url": "https://versiya.info/uploads/posts/2020-03/1584239824_photo_2020-03-15_11-36-16.jpg",
        "question_for_user": "Его/ её любимый напиток",
        "answer_back": "Любимый напиток ",
        "answers": [
            {"text": "🍺Алкоголь"},
            {"text": "☕️Кофе"},
            {"text": "🍋Газировка"},
            {"text": "🧃Сок"},
            {"text": "🍵Чай"},
        ]
    },
    {
        "question": "Твой любимый время года?",
        "image_url": "https://trikky.ru/wp-content/blogs.dir/1/files/2022/12/01/2022-12-01-12-21-11.jpg",
        "question_for_user": "Его/её любимый время года",
        "answers": [
            {"text": "❄️Зима"},
            {"text": "💐Весна"},
            {"text": "☀️Лето"},
            {"text": "🍂Осень"},
        ]
    },

{
        "question": "Твой размер ноги?",
        "image_url": "https://cs12.pikabu.ru/post_img/2021/09/10/10/og_og_1631290171258795964.jpg",
        "question_for_user": "Его/её размер ноги",
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
        "question": "Твой любимый школьный предмет?",
        "image_url": "https://kartinki.pics/uploads/posts/2022-03/1646955831_66-kartinkin-net-p-uchebnie-prinadlezhnosti-kartinki-74.jpg",
        "question_for_user": "Его/её любимый школьный предмет?",
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
        "question": "Твоё любимое хобби?",
        "image_url": "https://kartinki.pics/uploads/posts/2022-12/thumbs/1671729543_kartinkin-net-p-khobbi-kartinki-dlya-detei-instagram-11.jpg",
        "question_for_user": "Его/её любимое хобби",
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
        "question": "Твой любимый цвет?",
        "image_url": "https://www.mindful.org/content/uploads/How-the-Arts-Can-Bring-Healing-to-Healthcare-1024x640.png",
        "question_for_user": "Его/её любимый цвет",
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
        "question": "Твой цвет глаз?",
        "image_url": "https://i.pinimg.com/originals/56/8c/2c/568c2c50ea205d701c8115499cf14e3a.jpg",
        "question_for_user": "Его/её цвет глаз",
        "answers": [
            {"text": "🟢Зелёные"},
            {"text": "🟦Голубые"},
            {"text": "⚪Серые"},
            {"text": "🟤Карие"},
        ]
    },

{
        "question": "Твой любимый фрукт?",
        "image_url": "https://avatars.dzeninfra.ru/get-zen_doc/1708669/pub_5ddd8239a29ee0330b851fd6_5ddd853c3112ab60c7359559/scale_1200",
        "question_for_user": "Его/её любимый фрукт",
        "answers": [
            {"text": "🍎Яблоко"},
            {"text": "🍌Банан"},
            {"text": "🥭Манго"},
            {"text": "🍊Апельсин"},
            {"text": "🍊Мандарин"},
            ]
    },

{
        "question": "Твой любимый вид спорта?",
        "image_url": "https://mmkids.ru/wp-content/uploads/4/8/0/4805ee8e4f6ec25a166306b98205857e.jpeg",
        "question_for_user": "Его/её любимый вид спорта",
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
        "question": "Что тебе больше всего нравится смотреть?",
        "image_url": "https://static.mk.ru/upload/entities/2022/12/14/11/articles/facebookPicture/8e/55/ce/99/68b8a22b6052c0b5dcf70f85347ce007.jpg",
        "question_for_user": "Его/её нравится смотреть",
        "answers": [
            {"text": "🎞️Сериал"},
            {"text": "🎬Фильм"},
            {"text": "▷Мультик"},
        ]
    },

]


