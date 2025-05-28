
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def reverse() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="📚Создать тест на дружбу"))
    return builder.as_markup(resize_keyboard=True)


def creat_test_friend():
    kb = InlineKeyboardBuilder()
    kb.button(text="📚Создать тест на дружбу", switch_inline_query_current_chat="/create_quiz")
    return kb.as_markup()

