from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from core.database.orm_query import delete_user_quiz
from core.keyboards.admin.start import main_menu


router = Router()



@router.callback_query(F.data == "del_quiz")
async def del_quizez(call: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):

    await state.clear()
    await call.message.delete()


    if await delete_user_quiz(session, call.from_user.id):

        await call.message.answer(f"😉Ваш тест на дружбу удалён",
                                  reply_markup=main_menu())

    else:
        await call.message.answer("Опрос не найден или произошла ошибка.")


