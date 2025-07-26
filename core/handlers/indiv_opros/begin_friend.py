from aiogram import types, F, Router, Bot

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from config import ALL_QUESTIONS_LIST
from core.database.orm_query import select_quiz_id, look_user_answers, add_passed_id_name
from core.keyboards.admin.start import main_menu
from core.keyboards.indiv_test_friend.begin_indiv_opros import send_question_for_user
from core.keyboards.test_friend.reverse_messages import reverse
from core.keyboards.test_friend.stop_opros import stop_begin_quiz
from core.states.quiz import Indiv_quiz

router = Router()


QUESTION_DICT = {q["id"]: q for q in ALL_QUESTIONS_LIST}

@router.message(F.text == '◀️Приступить к прохождению теста')
async def begin_test(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):


    data = await state.get_data()
    friends_id = data.get("id_friends")
    one_message = data.get('one_message')

    original_id = await select_quiz_id(session, friends_id)
    original_str = original_id[0]  # '3|||6|||...'


    original_data = await look_user_answers(session, friends_id)
    original_data_str = original_data[0]  # '💂Английский язык|||📖Чтение|||...'


    correct_id = original_str.split("|||")
    correct_answers = original_data_str.split("|||")



    message_intro = await message.answer("<b>Не спеши! Отвечай внимательно!</b>", reply_markup=stop_begin_quiz())

    await state.update_data(
        current_question=0,
        user_answers=[],
        question_ids=correct_id,
        correct_answers=correct_answers,
        intro_message_id=message_intro.message_id,
    )

    await state.set_state(Indiv_quiz.BEGIN)
    await send_question_for_user(message.chat.id, 0, correct_id, message.message_id, state, bot)



@router.callback_query(F.data.startswith("answers_"), Indiv_quiz.BEGIN)
async def process_answer(call: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    _, q_idx, a_idx = call.data.split("_")
    question_index = int(q_idx)
    answer_index = int(a_idx)

    data = await state.get_data()
    question_ids = data.get("question_ids", [])
    user_answers = data.get("user_answers", [])
    correct_answers = data.get("correct_answers", [])
    message_intro = data.get("message_intro")

    question_id = question_ids[question_index]
    question = QUESTION_DICT[question_id]
    selected = question["answers"][answer_index]["text"]

    while len(user_answers) <= question_index:
        user_answers.append(None)
    user_answers[question_index] = selected

    await state.update_data(user_answers=user_answers)

    next_index = question_index + 1

    if next_index < len(question_ids):
        await state.update_data(current_question=next_index)
        await call.answer()
        await send_question_for_user(call.message.chat.id, next_index, question_ids, call.message.message_id, state, bot)
    else:
        await call.answer()

        try:
            await call.message.delete()
        except:
            pass

        intro_id = data.get("intro_message_id")
        if intro_id:
            try:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=intro_id)
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=message_intro)
            except:
                pass

        await state.clear()

        # Подсчёт результатов
        correct_count = 0
        if call.from_user.id == data["id_friends"]:
            result_text = "<b>🎉 Вы прошли свой тест!</b>\n\n<b>📋 Результаты:</b>\n\n"
        else:
            result_text = f"<b>🎉 Ваш друг @{call.from_user.username} прошёл тест!</b>\n\n<b>📋 Результаты:</b>\n\n"



        for i, question_id in enumerate(question_ids):
            q = QUESTION_DICT[question_id]
            correct = correct_answers[i]
            friend = user_answers[i]
            is_correct = (correct == friend)

            result_text += (
                f"{'✅' if is_correct else '❌'} <b>{q['question_for_user']}</b>\n"
                f"<b>Правильный ответ:</b> {correct}\n"
                f"<b>Ответ друга:</b> {friend}\n\n"
            )

            if is_correct:
                correct_count += 1

        result_text += f"<b>🏁 Итог:</b> {correct_count} из {len(question_ids)} правильных!"

        if call.from_user.id == data["id_friends"]:
            await call.answer()

        else:
            await bot.send_message(chat_id=call.message.chat.id, text="Результаты отправлены другу 🎯")

            msg = await bot.send_message(
                chat_id=call.message.chat.id,
                text="<b>🌟Теперь твоя очередь устроить дружеский экзамен!🌟</b>\n\n"
                     "Почему бы не предложить ему ответный тест на дружбу?\n"
                     "Пусть проверит, насколько хорошо он знает тебя.",
                reply_markup=reverse()
            )

            await state.update_data(reverse_msg=msg)

        await bot.send_message(
            chat_id=data["id_friends"],
            text=result_text,
            reply_markup=main_menu()
        )

        await add_passed_id_name(session, {
            "friend_id": data["id_friends"],
            "user_id_passed": call.from_user.id,
            "user_name_passed": call.from_user.username,
            "total_questions": correct_count,
            "len_quiz": len(question_ids)
        })