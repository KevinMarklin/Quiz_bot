import re

from aiogram import F, Router, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from config import FRIEND_TEST
from sqlalchemy.ext.asyncio import AsyncSession


from core.database.orm_query import look_user_quiz, look_user_answers, add_passed_id_name

from core.keyboards.begin_opros import send_question_for_user
from core.keyboards.start import main_menu
from core.states.quiz import BeginFriendTest
from core.keyboards.reverse_messages import reverse


router = Router()


@router.message(F.text == '▶️Начать прохождение опроса')
async def creat_quiz(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    data = await state.get_data()
    friends_id = data.get("id_friends")
    one_message = data.get('one_message')
    print(friends_id)

    await bot.delete_message(chat_id=message.chat.id, message_id=one_message)

    user_quiz_exists = await look_user_quiz(session, friends_id)

    if user_quiz_exists == False:
        await message.answer("Ой, кажется, тест друга исчез... 🥹\n"
                             "Не беда! Попроси его создать новый — будет ещё интереснее! 💫",
                             reply_markup=ReplyKeyboardRemove())

    else:
        message_intro = await message.answer("Отвечай спокойно, не торопись",
                                             reply_markup=ReplyKeyboardRemove())
        await state.update_data(
            current_question=0,
            user_answers=[],
            intro_message_id=message_intro.message_id
        )

        await state.set_state(BeginFriendTest.OPROS)
        await send_question_for_user(message.chat.id, 0, message.message_id, state, bot)




@router.callback_query(F.data.startswith("answers_"), BeginFriendTest.OPROS)
async def process_answer(call: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    user_id = call.from_user.id

    _, q_idx, a_idx = call.data.split("_")
    question_index = int(q_idx)
    answer_index = int(a_idx)

    data = await state.get_data()
    user_answers = data.get("user_answers", [])
    message_intro = data.get("message_intro")
    friends_id = data.get("id_friends")

    # Сохраняем ответ
    selected = FRIEND_TEST[question_index]["answers"][answer_index]["text"]
    while len(user_answers) <= question_index:
        user_answers.append(None)
    user_answers[question_index] = selected

    await state.update_data(user_answers=user_answers)

    next_index = question_index + 1

    if next_index < len(FRIEND_TEST):
        await state.update_data(current_question=next_index)
        await call.answer()
        await send_question_for_user(call.message.chat.id, next_index, call.message.message_id, state, bot)
    else:
        await call.answer()

        # Удаляем сообщение с фото и кнопками
        try:
            await call.message.delete()
        except Exception:
            pass

        intro_id = data.get("intro_message_id")
        if intro_id:
            try:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=intro_id)
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=message_intro)
            except Exception:
                pass


        original_data = await look_user_answers(session, friends_id)

        original_data_str = original_data[0]  # Получаем строку из списка
        original_data_list = re.findall(r'[^\s]+\S*', original_data_str)

        await state.clear()


        correct_count = 0
        total_questions = len(FRIEND_TEST)

        result_text = f"<b>🎉 Ваш друг {call.from_user.username} прошёл тест!</b>\n\n<b>📋 Результаты:</b>\n\n"

        for i in range(total_questions):
            question = FRIEND_TEST[i]["question_for_user"]
            correct = original_data_list[i]
            friend = user_answers[i]

            is_correct = (correct == friend)
            if is_correct:
                result_text += f"✅ <b>{question}</b>\n<b>Правильный ответ:</b> {correct}\n<b>Ответ друга:</b> {friend}\n\n"
                correct_count += 1
            else:
                result_text += f"❌ <b>{question}</b>\n<b>Правильный ответ:</b> {correct}\n<b>Ответ друга:</b> {friend}\n\n"

        result_text += f"<b>🏁 Итог:</b> {correct_count} из {total_questions} правильных!"

        await bot.send_message(chat_id=call.message.chat.id,
                               text="Результаты отправлены другу 🎯")

        await bot.send_message(chat_id=call.message.chat.id,
                               text="<b>🌟Теперь твоя очередь устроить дружеский экзамен!🌟</b>\n\n"
                                    "Почему бы не предложить ему ответный тест на дружбу?\n"
                                    "Пусть проверит, насколько хорошо он знает тебя.",
                               reply_markup=reverse())

        await state.update_data(reverse_test_friend=True)


        await bot.send_message(chat_id=friends_id,
                               text=result_text,
                               reply_markup=main_menu())

        await state.update_data(
            friend_id=friends_id,
            user_id_passed=user_id,
            user_name_passed=call.from_user.username,
            total_questions=correct_count

        )

        info_user_passed = await state.get_data()

        await add_passed_id_name(session, info_user_passed)


