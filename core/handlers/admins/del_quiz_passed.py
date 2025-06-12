from aiogram import Router, F, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
import toml

from core.database.orm_query import clear_quiz_user_table, clear_passed_user_table
from core.keyboards.admin.del_quiz_passed import del_q_p

router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]


@router.message(Command("del_quiz_passed"))
async def start(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()

    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        return

    await message.answer("Выбери, что удалить:",
                         reply_markup=del_q_p())


@router.callback_query(F.data == "del_quizs")
async def del_quizez(call: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):

    await state.clear()

    try:
        await clear_quiz_user_table(session)
    except Exception as e:
        await call.message.answer(f"Ошибка {e}")

    await call.message.answer("Успешно удалено")
    await call.answer()


@router.callback_query(F.data == "del_passed")
async def del_quizez(call: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):

    await state.clear()

    try:
        await clear_passed_user_table(session)
    except Exception as e:
        await call.message.answer(f"Ошибка {e}")

    await call.message.answer("Успешно удалено")
    await call.answer()