
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="📚Создать тест на дружбу"))
    # builder.row(KeyboardButton(text="🤑Купить vip"), KeyboardButton(text="🧍Реферальная программа"))
    # builder.row(KeyboardButton(text="ℹ️ Информация"), KeyboardButton(text="🆘 Поддержка"))
    builder.row(KeyboardButton(text="🤑Поддержать автора"), (KeyboardButton(text="🆘 Поддержка")))
    builder.row(KeyboardButton(text="ℹ️Информация о тесте"))
    return builder.as_markup(resize_keyboard=True)