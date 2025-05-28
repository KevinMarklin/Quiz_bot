import toml

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.orm_query import all_users


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







