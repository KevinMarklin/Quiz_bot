from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from core.database.orm_query import delete_user_quiz
from core.keyboards.start import main_menu


router = Router()



@router.callback_query(F.data == "del_quiz")
async def del_quizez(call: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    data = await state.get_data()
    del_message_opros_id = data.get("del_message_id")
    user_id = call.from_user.id
    if await delete_user_quiz(session, user_id):
        await call.bot.edit_message_text(
            chat_id=user_id,
            message_id=del_message_opros_id,
            text=f"😉Ваш тест на дружбу удалён\n\n"
                 f"Нажмите /start чтобы продолжить работу бота",
        )
    else:
        await call.message.answer("Опрос не найден или произошла ошибка.")


