
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def choice_test() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🎯Классический тест"))
    builder.row(KeyboardButton(text="⚒️Индивидуальный тест"))
    return builder.as_markup(resize_keyboard=True)
