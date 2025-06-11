import toml

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from core.keyboards.admin.ban_messages_user import admin_lock_kb
from lock_state import is_locked, set_locked
router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]



@router.message(Command("ban_message"))
async def ban(message: Message):
    await message.answer('Выберите действие:', reply_markup=admin_lock_kb())




@router.callback_query(F.data == "admin_lock_toggle")
async def toggle_lock(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in ADMIN_IDS:
        return

    locked_now = is_locked()
    set_locked(not locked_now)

    await call.message.edit_reply_markup(reply_markup=admin_lock_kb())
    await call.answer(
        "🔒 Доступ ограничен" if not locked_now else "🔓 Доступ открыт", show_alert=True
    )