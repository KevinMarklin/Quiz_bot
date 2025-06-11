from aiogram import types, F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from config import ALL_QUESTIONS_LIST
from core.callback_data.test_friend import Paginator, SelectQuestion, Control, QuizAnswer
from core.database.orm_query import add_user_answer
from core.dialogs.opros.creat_test import update_selection_menu
from core.keyboards.indiv_test_friend.creat_test import build_selection_keyboard, build_quiz_keyboard
from core.keyboards.test_friend.begin_opros import reverse_link_friend_bk
from core.states.quiz import QuizCreator
from core.keyboards.test_friend.stop_opros import stop_creat_opros
from core.utils.encryption_id import PollLinkGenerator

router = Router()


QUESTIONS_DB = {q["id"]: q for q in ALL_QUESTIONS_LIST}

@router.message(F.text == '⚒️Индивидуальный тест')
async def cmd_start(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()

# Удаление ненужно Reply клавиатуры
    await bot.send_message(
        chat_id=message.chat.id,
        text=".",
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)

    await state.set_state(QuizCreator.selecting_questions)
    await state.update_data(selected_ids=[], page=0)

    keyboard = build_selection_keyboard(page=0, selected_ids=[])
    await message.answer(
        "🎨 *Собери уникальный тест!*\n\n"
        "Листай вопросы с помощью кнопок «Вперёд ➡️» и «⬅️ Назад»\n"
        "Отмечай понравившиеся(просто нажми на них)\n"
        "Просматривай выбранные вопросы и заверши подбор в любой момент!\n\n"
        "*Совет:* Выбери 5 - 10 вопросов, которые лучше всего раскроют вашу дружбу!",
        reply_markup=keyboard
    )







@router.callback_query(QuizCreator.selecting_questions, Paginator.filter())
async def handle_pagination(callback: types.CallbackQuery, callback_data: Paginator, state: FSMContext):
    await callback.answer()
    page = callback_data.page
    if callback_data.action == "next":
        page += 1
    elif callback_data.action == "prev":
        page -= 1

    await state.update_data(page=page)
    await update_selection_menu(callback, state)


@router.callback_query(QuizCreator.selecting_questions, SelectQuestion.filter())
async def handle_question_selection(callback: types.CallbackQuery, callback_data: SelectQuestion, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    selected_ids = data['selected_ids']

    q_id = callback_data.question_id
    if q_id in selected_ids:
        selected_ids.remove(q_id)
    else:
        selected_ids.append(q_id)

    await state.update_data(selected_ids=selected_ids)
    await update_selection_menu(callback, state)



@router.callback_query(QuizCreator.selecting_questions, Control.filter())
async def handle_control(callback: types.CallbackQuery, callback_data: Control, state: FSMContext):
    data = await state.get_data()
    selected_ids = data.get("selected_ids", [])
    message_to_edit_id = data.get("message_to_edit_id")

    if callback_data.action == "view":
        if not selected_ids:
            await callback.answer("Вы ещё не выбрали ни одного вопроса!", show_alert=True)
            return


        selected_questions_text = "\n".join(
            f"{index + 1}. {QUESTIONS_DB[q_id]['question']}"
            for index, q_id in enumerate(selected_ids)
        )

        await callback.answer("Обновляю список вопросов...", show_alert=False)

        try:
            if message_to_edit_id:
                await callback.bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=message_to_edit_id,
                    text=f"Выбранные вопросы:\n{selected_questions_text}"
                )
            else:
                sent_message = await callback.message.answer(f"Выбранные вопросы:\n{selected_questions_text}")
                await state.update_data(message_to_edit_id=sent_message.message_id)

        except Exception as e:
            print(f"Ошибка при обновлении сообщения: {e}")
            sent_message = await callback.message.answer(f"Выбранные вопросы:\n{selected_questions_text}")
            await state.update_data(message_to_edit_id=sent_message.message_id)

    elif callback_data.action == "finish":
        if not selected_ids:
            await callback.answer("Нужно выбрать хотя бы один вопрос!", show_alert=True)
            return

        # Начинаем квиз
        await state.set_state(QuizCreator.taking_quiz)
        await state.update_data(user_answers=[], quiz_question_index=0)
        await callback.answer("Отлично! Начинаем тест.",
                              show_alert=True)
        await callback.message.delete()

        if message_to_edit_id:
            await callback.bot.delete_message(chat_id=callback.message.chat.id,
                                          message_id=message_to_edit_id)


        # Отправляем первый вопрос
        first_question_id = selected_ids[0]
        question_data = QUESTIONS_DB[first_question_id]
        keyboard = build_quiz_keyboard(first_question_id)

        start_message = await callback.message.answer("Тест начинается!", reply_markup=stop_creat_opros())
        await callback.message.answer_photo(
            photo=question_data["image_url"],
            caption=question_data["question"],
            reply_markup=keyboard
        )
        await state.update_data(start_message=start_message.message_id)

@router.callback_query(QuizCreator.taking_quiz, QuizAnswer.filter())
async def handle_quiz_answer(callback: types.CallbackQuery,
                             callback_data: QuizAnswer,
                             state: FSMContext,
                             session: AsyncSession,
                             bot: Bot):
    await callback.answer()
    all_answers = []
    all_id = []

    # Сохраняем ответ
    data = await state.get_data()
    user_answers = data["user_answers"]
    start_message = data["start_message"]
    user_answers.append({
        "question_id": callback_data.question_id,
        "answer": callback_data.answer_text
    })

    # Определяем следующий вопрос
    quiz_question_index = data["quiz_question_index"] + 1
    selected_ids = data["selected_ids"]

    await state.update_data(user_answers=user_answers, quiz_question_index=quiz_question_index)

    await callback.message.delete()  # Удаляем старый вопрос

    if quiz_question_index < len(selected_ids):
        # Отправляем следующий вопрос
        next_question_id = selected_ids[quiz_question_index]
        question_data = QUESTIONS_DB[next_question_id]
        keyboard = build_quiz_keyboard(next_question_id)
        await callback.message.answer_photo(
            photo=question_data["image_url"],
            caption=question_data["question"],
            reply_markup=keyboard
        )
    else:
        # Завершаем квиз
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=start_message)
        await callback.message.answer("🎉 Тест завершен! Спасибо за ваши ответы.",
                                      reply_markup=ReplyKeyboardRemove())

        # Формируем и выводим итоговый список ответов
        result_text = "<b>Ваши ответы:</b>\n\n"
        for answer_data in user_answers:
            q_id = answer_data['question_id']
            a_text = answer_data['answer']
            all_answers.append(a_text)
            all_id.append(str(q_id))

        try:
            result = " ".join(["; ".join(all_id), "; ".join(all_answers)])
            await add_user_answer(session, result, callback.from_user.id, callback.from_user.username)
        except Exception as e:
            await callback.message.answer("Произошла ошибка в сохранения ответов. Попробуй повторить снова")
            print(e)

        bot_user = await bot.get_me()
        bot_name = bot_user.username
        link_generator = PollLinkGenerator(bot_name)
        encrypted_link = link_generator.generate_link(callback.from_user.id)

        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=f"🎉 ОПРОС УСПЕШНО ЗАВЕРШЁН! 🎉\n\n"
                 f"━━━━━━━━━━━━━━━━━━━━\n"
                 f"📣 Теперь <b>поделитесь ссылкой</b> с друзьями:\n"
                 f"«Узнай, на сколько хорошо знают тебя твои друзья.\n"
                 f"Распространяй её во всех социальных сетях»\n\n"
                 f"🚀 *Ваша ссылка:*\n"
                 f"<code>{encrypted_link}</code>\n\n"
                 f"🔥 Чем больше участников — тем жарче соревнование!",
            reply_markup=reverse_link_friend_bk(encrypted_link),
            parse_mode="HTML"
        )

        await state.clear()