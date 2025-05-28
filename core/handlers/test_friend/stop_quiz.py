from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.keyboards.start import main_menu
from core.states.quiz import FriendTest

router = Router()




@router.callback_query(F.data == "stop_opros", FriendTest.QUIZ)
async def stop_test(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Удаляем сообщение с вопросом
    try:
        await call.message.delete()
    except Exception:
        pass

    # Удаляем вступительное сообщение
    intro_id = data.get("intro_message_id")
    if intro_id:
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=intro_id)
        except Exception:
            pass

    await state.clear()
    await call.answer()
    await call.message.answer("🚫 Опрос был остановлен.",
                              reply_markup=main_menu())