from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from config import ALL_QUESTIONS_LIST
from core.callback_data.test_friend import Paginator, SelectQuestion, Control, QuizAnswer
from core.database.orm_query import add_user_answer_indiv
from core.dialogs.opros.creat_test import update_selection_menu
from core.keyboards.indiv_test_friend.creat_test import build_selection_keyboard, build_quiz_keyboard, \
    reverse_link_friend_indiv_bk
from core.states.quiz import QuizCreator
from core.keyboards.test_friend.stop_opros import stop_creat_opros
from core.utils.encryption_id import PollLinkGenerator

router = Router()


QUESTIONS_DB = {q["id"]: q for q in ALL_QUESTIONS_LIST}

@router.message(F.text == '⚒️Индивидуальный тест')
async def cmd_start(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    mes_choice = data.get("choice_mes_test")
    await bot.delete_message(chat_id=message.chat.id, message_id=mes_choice)


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
        "🎨 <b>Собери уникальный тест!</b>\n\n"
        "Листай вопросы с помощью кнопок «Вперёд ➡️» и «⬅️ Назад»\n"
        "Отмечай понравившиеся(просто нажми на них)\n"
        "Просматривай выбранные вопросы и заверши подбор в любой момент!\n\n"
        "<b>Совет:</b> Выбери 5 - 10 вопросов, которые лучше всего раскроют вашу дружбу!",
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
        if len(selected_ids) < 10:
            selected_ids.append(q_id)
        else:
            await callback.answer("Максимум 10 вопросов!", show_alert=True)


    await state.update_data(selected_ids=selected_ids)
    await update_selection_menu(callback, state)



@router.callback_query(QuizCreator.selecting_questions, Control.filter())
async def handle_control(callback: types.CallbackQuery, callback_data: Control, state: FSMContext):
    data = await state.get_data()
    selected_ids = data.get("selected_ids", [])
    message_to_edit_id = data.get("message_to_edit_id")
    page = data.get("page", 0)
    last_selected_text = data.get("last_selected_text")
    was_sent_before = data.get("was_sent_before", False)

    if callback_data.action == "view":
        if not selected_ids:
            await callback.answer("Вы ещё не выбрали ни одного вопроса!", show_alert=True)
            return

        # Собираем текст с вопросами
        selected_questions_text = "\n".join(
            f"{index + 1}. {QUESTIONS_DB[q_id]['question']}"
            for index, q_id in enumerate(selected_ids)
        )

        # Если он не изменился — ничего не делаем
        if selected_questions_text == last_selected_text:
            await callback.answer("Вы уже видите актуальный список", show_alert=False)
            return

        await callback.answer("Обновляю список вопросов...", show_alert=False)

        # Обновляем сообщение с вопросами
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

        # Если кнопка уже была добавлена ранее — не обновляем клавиатуру
        if not was_sent_before:
            updated_markup = build_selection_keyboard(
                page=page,
                selected_ids=selected_ids,
                was_sent_before=True
            )
            await state.update_data(was_sent_before=True, last_selected_text=selected_questions_text)

            try:
                await callback.message.edit_reply_markup(reply_markup=updated_markup)
            except Exception as e:
                print(f"Ошибка при обновлении клавиатуры: {e}")
        else:
            # Обновим только last_selected_text, чтобы повторное сравнение работало корректно
            await state.update_data(last_selected_text=selected_questions_text)

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

        start_message = await callback.message.answer("<b>Будь честен с собой и с друзьями!</b>", reply_markup=stop_creat_opros())
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

        # Формируем и выводим итоговый список ответов
        for answer_data in user_answers:
            q_id = answer_data['question_id']
            a_text = answer_data['answer']
            all_answers.append(a_text)
            all_id.append(str(q_id))

        try:
            ser_answers_only = "|||".join(all_answers)
            ser_quiz_id_only = "|||".join(all_id)
            await add_user_answer_indiv(session, ser_answers_only,
                                        callback.from_user.id,
                                        callback.from_user.username,
                                        ser_quiz_id_only)

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
                 f"🚀 <b>Ваша ссылка:</b>\n"
                 f"<code>{encrypted_link}</code>\n\n"
                 f"🔥 Чем больше участников — тем жарче соревнование!",
            reply_markup=reverse_link_friend_indiv_bk(encrypted_link, len(all_id)),
            parse_mode="HTML"
        )

        await state.clear()