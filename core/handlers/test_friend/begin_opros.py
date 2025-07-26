

from aiogram import F, Router, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from config import FRIEND_TEST
from sqlalchemy.ext.asyncio import AsyncSession


from core.database.orm_query import look_user_answers, add_passed_id_name


from core.keyboards.admin.start import main_menu
from core.keyboards.test_friend.begin_opros import send_question_for_user
from core.keyboards.test_friend.reverse_messages import reverse
from core.keyboards.test_friend.stop_opros import stop_begin_quiz
from core.states.quiz import BeginFriendTest


router = Router()


@router.message(F.text == '▶️Приступить к прохождению теста')
async def creat_quiz(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    friends_id = data.get("id_friends")
    one_message = data.get('one_message')
    print(friends_id)

    await bot.delete_message(chat_id=message.chat.id, message_id=one_message)


    message_intro = await message.answer("<b>Не спеши! Отвечай внимательно!</b>",
                                         reply_markup=stop_begin_quiz())
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
        original_data_str = original_data[0]  # '💂Английский язык|||📖Чтение|||...'
        correct_answers = original_data_str.split("|||")  # список

        await state.clear()


        correct_count = 0
        total_questions = len(FRIEND_TEST)

        if call.from_user.id == friends_id:
            header = f"<b>🎉 Вы прошли свой тест!</b>\n\n<b>📋 Результаты:</b>\n\n"
        else:
            header = f"<b>🎉 Ваш друг @{call.from_user.username} прошёл тест!</b>\n\n<b>📋 Результаты:</b>\n\n"

        result_text = header

        for i in range(total_questions):
            question = FRIEND_TEST[i]["question_for_user"]
            correct = correct_answers[i]
            friend = user_answers[i]

            is_correct = (correct == friend)
            if is_correct:
                result_text += f"✅ <b>{question}</b>\n<b>Правильный ответ:</b> {correct}\n<b>Ответ друга:</b> {friend}\n\n"
                correct_count += 1
            else:
                result_text += f"❌ <b>{question}</b>\n<b>Правильный ответ:</b> {correct}\n<b>Ответ друга:</b> {friend}\n\n"

        result_text += f"<b>🏁 Итог:</b> {correct_count} из {total_questions} правильных!"

        if call.from_user.id == friends_id:
            await call.answer()
        else:
            await bot.send_message(chat_id=call.message.chat.id,
                                   text="Результаты отправлены другу 🎯")

            msg = await bot.send_message(chat_id=call.message.chat.id,
                                   text="<b>🌟Теперь твоя очередь устроить дружеский экзамен!🌟</b>\n\n"
                                        "Почему бы не предложить ему ответный тест на дружбу?\n"
                                        "Пусть проверит, насколько хорошо он знает тебя.",
                                   reply_markup=reverse())

            await state.update_data(reverse_msg=msg.message_id)

        await state.update_data(reverse_test_friend=True)

        await bot.send_message(chat_id=friends_id,
                               text=result_text,
                               reply_markup=main_menu())

        await state.update_data(
            friend_id=friends_id,
            user_id_passed=user_id,
            user_name_passed=call.from_user.username,
            total_questions=correct_count,
            len_quiz=11

        )

        info_user_passed = await state.get_data()

        await add_passed_id_name(session, info_user_passed)


