import toml

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from core.keyboards.ban_messages_user import admin_lock_kb
from lock_state import is_locked, set_locked
router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]




@router.message(Command("help"))
async def sending_mes(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        return

    await message.answer('/look_users - Посмотреть всех пользователей\n'
                         '/sending_mes - Отправить рассылку\n'
                         '/ban_message - Заблокировать отпраку сообщений\n'
                         '')

