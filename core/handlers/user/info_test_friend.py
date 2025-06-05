from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.orm_query import look_user_quiz, result_user_passed

from core.keyboards.reverse_messages import creat_test_friend, reverse

router = Router()


@router.message(F.text == 'ℹ️Информация о тесте')
@router.message(Command("info_test_friend"))
async def info(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    user_id = message.from_user.id

    user_quiz_exists = await look_user_quiz(session, user_id)

    if user_quiz_exists == False:
        await message.answer("🌟У вас нету, созданного теста на дружбу,\n чтобы получить о нём информацию!",
                             reply_markup=reverse())

    else:
        user_result = await result_user_passed(session, user_id)

        if user_result == False:
            await message.answer("🌟Твои друзья ещё не прошли твой тест!")

        else:

            result_text = "<b>🌟Друзья, прошедшие твой тест:</b>\n\n"


            for idx, (name, score) in enumerate(user_result, start=1):
                name_display = name.strip() if isinstance(name, str) and name.strip() else "Имя не найдено"
                result_text += f"{idx}. @{name_display} - {score}/11\n"

            await message.answer(result_text)





@router.callback_query(F.data == "info_test")
async def info(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    user_id = call.from_user.id

    data = await state.get_data()
    del_message_opros_id = data.get("del_message_id")

    user_quiz_exists = await look_user_quiz(session, user_id)

    if user_quiz_exists == False:

        await call.bot.delete_message(
            chat_id=user_id,
            message_id=del_message_opros_id
        )

        await call.message.answer("🌟У вас нету, созданного теста на дружбу,\n"
                                  "чтобы получить о нём информацию!",
                                  reply_markup=reverse())

    else:
        user_result = await result_user_passed(session, user_id)

        if user_result == False:

            await call.bot.delete_message(
                chat_id=user_id,
                message_id=del_message_opros_id
            )

            await call.message.answer("🌟Твои друзья ещё не прошли твой тест!")

        else:

            await call.bot.delete_message(
                chat_id=user_id,
                message_id=del_message_opros_id
            )

            result_text = "<b>🌟Друзья, прошедшие твой тест:</b>\n\n"


            for idx, (name, score) in enumerate(user_result, start=1):
                name_display = name.strip() if isinstance(name, str) and name.strip() else "Имя не найдено"
                result_text += f"{idx}. @{name_display} - {score}/11\n"

            await call.message.answer(result_text)

    await call.answer()