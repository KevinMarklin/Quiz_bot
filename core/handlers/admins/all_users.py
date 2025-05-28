import toml
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.orm_query import all_users
from core.states.admin import Admin
from core.keyboards.ban_messages_user import admin_lock_kb
from lock_state import is_locked, set_locked
router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]



@router.message(Command("look_users"))
async def all_user(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    lines = []
    if user_id not in ADMIN_IDS:
        return

    users = await all_users(session)

    for i, (user_id, user_name) in enumerate(users, start=1):
        display_name = user_name if user_name else "имени нет"
        lines.append(f"{i}. 👤 {user_id} — {display_name}")

    total = len(users)
    lines.append(f"\n📊 Всего пользователей: {total}")

    result = "\n".join(lines)

    await message.answer(f"{result}")







