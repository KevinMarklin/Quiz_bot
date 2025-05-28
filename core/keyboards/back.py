from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def back_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🔙Вернуться к меню"))
    return builder.as_markup(resize_keyboard=True)

def back_menu_in():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙Вернуться к меню", callback_data="menu")
    return kb.as_markup()


