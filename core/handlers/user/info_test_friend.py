from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.orm_query import result_user_passed, look_quiz
from core.keyboards.test_friend.reverse_messages import reverse

router = Router()


@router.message(F.text == 'ℹ️Информация о тесте')
@router.message(Command("info_test_friend"))
async def info(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    user_id = message.from_user.id

    user_quiz_exists = await look_quiz(session, user_id)

    if user_quiz_exists == False:
        await message.answer("Информация о тесте на дружбу,\n"
                             "появится здесь, как только вы его создадите.\n"
                             "Начните прямо сейчас – это увлекательно! ✨",
                             reply_markup=reverse())

    else:
        user_result = await result_user_passed(session, user_id)

        if user_result == False:
            await message.answer("🌟 Твои друзья ещё не прошли твой тест!")

        else:

            result_text = "<b>🌟 Друзья, прошедшие твой тест:</b>\n\n"

            for idx, (name, score, len_quiz) in enumerate(user_result, start=1):
                name_display = name.strip() if isinstance(name, str) and name.strip() else "Имя не найдено"

                # Добавляем "(Ты сам)", если это имя пользователя, вызвавшего коллбэк
                if name_display.lower() == message.from_user.username.lower():
                    name_display += " (Ты сам)"

                result_text += f"{idx}. @{name_display} - {score}/{len_quiz}\n"

            await message.answer(result_text)




@router.callback_query(F.data == "info_test")
async def info(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()

    user_quiz_exists = await look_quiz(session, call.from_user.id)

    if user_quiz_exists == False:

        await call.message.delete()

        await call.message.answer("Информация о тесте на дружбу,\n"
                                  "появится здесь, как только вы его создадите.\n"
                                  "Начните прямо сейчас – это увлекательно! ✨",
                                  reply_markup=reverse())

    else:
        user_result = await result_user_passed(session, call.from_user.id)

        if user_result == False:

            await call.message.delete()

            await call.message.answer("🌟 Твои друзья ещё не прошли твой тест!")

        else:

            await call.message.delete()

            result_text = "<b>🌟 Друзья, прошедшие твой тест:</b>\n\n"

            for idx, (name, score, len_quiz) in enumerate(user_result, start=1):
                name_display = name.strip() if isinstance(name, str) and name.strip() else "Имя не найдено"

                # Добавляем "(Ты сам)", если это имя пользователя, вызвавшего коллбэк
                if name_display.lower() == call.from_user.username.lower():
                    name_display += " (Ты сам)"

                result_text += f"{idx}. @{name_display} - {score}/{len_quiz}\n"

            await call.message.answer(result_text)

    await call.answer()