from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.keyboards.start import main_menu
from core.states.quiz import FriendTest

router = Router()




@router.message(F.text == 'Прекратить создание теста❌')
async def stop_test(message: Message, state: FSMContext):

    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass

    data = await state.get_data()
    intro_id = data.get("intro_message_id")
    if intro_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=intro_id)
        except Exception:
            pass

    await state.clear()
    await message.answer("🚫 Создание теста было остановлено",
                         reply_markup=main_menu())


@router.message(F.text == '❌Прекратить прохождение опроса')
async def stop_test(message: Message, state: FSMContext):

    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass

    data = await state.get_data()
    intro_id = data.get("intro_message_id")
    if intro_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=intro_id)
        except Exception:
            pass

    await state.clear()
    await message.answer("🚫 Опрос был остановлен",
                         reply_markup=main_menu())
