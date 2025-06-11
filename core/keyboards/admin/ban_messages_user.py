from aiogram.utils.keyboard import InlineKeyboardBuilder
from lock_state import is_locked

def admin_lock_kb():
    locked = is_locked()
    text = "🔓 Открыть доступ" if locked else "🔒 Ограничить доступ"
    kb = InlineKeyboardBuilder()
    kb.button(text=text, callback_data="admin_lock_toggle")
    return kb.as_markup()