import toml

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.orm_query import all_users
from core.states.admin import Sending

router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]



@router.message(Command("sending_mes"))
async def sending_mes(message: Message, session: AsyncSession, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        return

    await message.answer('Напишите сообщение, которое хотите разослать')

    await state.set_state(Sending.SEND)


@router.message(Sending.SEND)
async def sending_mes_all(message: Message, session: AsyncSession, state: FSMContext, bot: Bot):

    mes = message.text

    users = await all_users(session)

    for user in users:
        await bot.send_message(chat_id=user, text=mes)

    await state.clear()
