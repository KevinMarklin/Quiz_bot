from aiogram.utils.keyboard import InlineKeyboardBuilder


def del_q_p():
    kb = InlineKeyboardBuilder()
    kb.button(text="Таблицу с тестами", callback_data="del_quizs")
    kb.button(text="Таблицу с passed", callback_data="del_passed")
    kb.adjust(2)
    return kb.as_markup()