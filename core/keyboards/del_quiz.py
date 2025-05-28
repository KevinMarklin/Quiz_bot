from aiogram.utils.keyboard import InlineKeyboardBuilder


def del_quiz():
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑Удалить тест на дружбу", callback_data="del_quiz")
    return kb.as_markup()
