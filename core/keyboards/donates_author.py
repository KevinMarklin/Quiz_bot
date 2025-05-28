import l10n
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


def choice_donate():
    kb = InlineKeyboardBuilder()
    kb.button(text="⭐️ Поддержать звёздами", callback_data="stars")
    kb.button(text="💎 Поддержать рублями", callback_data="ruble")
    kb.adjust(2)
    return kb.as_markup()








def donate_rubl() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for amount in [50, 100, 200, 300]:
        kb.button(text=f"{amount}₽", callback_data=f"ruble_{amount}")
    kb.row(InlineKeyboardButton(text="🔙Назад", callback_data="back_choice_donate"))
    kb.adjust(2)
    return kb.as_markup()


def payment_rubl():
    kb = InlineKeyboardBuilder()
    kb.button(text=f"💳 Оплатить", pay=True),
    kb.button(text=f"🔙Назад ", callback_data="back_ruble_choice")
    kb.adjust(1)
    return kb.as_markup()



def payment_receipt_kb(receipt_url):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧾 Чек", url=receipt_url)]
    ])
    return kb







def payment_stars():
    kb = InlineKeyboardBuilder()
    kb.button(text=f"💳 Оплатить", pay=True)
    kb.button(text=f"🔙Назад ", callback_data="back_stars_donate")
    kb.adjust(1)
    return kb.as_markup()












def back():
    kb = InlineKeyboardBuilder()
    kb.button(text=f"🔙Назад ", callback_data="back_choice")
    return kb.as_markup()







