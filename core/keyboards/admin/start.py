
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="📚Создать тест на дружбу"))
    # builder.row(KeyboardButton(text="🤑Купить vip"), KeyboardButton(text="🧍Реферальная программа"))
    # builder.row(KeyboardButton(text="ℹ️ Информация"), KeyboardButton(text="🆘 Поддержка"))
    builder.row(KeyboardButton(text="🤑Поддержать автора"), (KeyboardButton(text="🆘 Поддержка")))
    builder.row(KeyboardButton(text="ℹ️Информация о тесте"))
    return builder.as_markup(resize_keyboard=True)



def reverse_link_friend_delete_info_bk(encrypted_link):
    kb = InlineKeyboardBuilder()
    kb.button(text="📤 Отправить друзьям",
    url=f"https://t.me/share/url?url={encrypted_link}&text=🔥СЕРЬЁЗНЫЙ ВЫЗОВ!🔥\n"
        f"Ты уверен, что знаешь меня на 11/11?")
    kb.button(text="📊Результаты", callback_data="info_test")
    kb.button(text="🗑Удалить тест на дружбу", callback_data="del_quiz")
    kb.adjust(1)

    return kb.as_markup()
