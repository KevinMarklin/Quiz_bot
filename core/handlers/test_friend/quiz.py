from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
import asyncio
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
import re
from config import FRIEND_TEST
from core.database.orm_query import look_user_quiz, delete_user_quiz, add_user_answer
from core.keyboards.answer_quiz import send_question
from core.keyboards.answer_quiz import link_friends
from core.keyboards.begin_opros import reverse_link_friend_bk
from core.keyboards.del_quiz import del_quiz
from core.keyboards.stop_opros import stop_creat_quiz
from core.keyboards.start import main_menu
from core.states.quiz import FriendTest
from core.utils.encryption_id import PollLinkGenerator

router = Router()


@router.message(F.text == '📚Создать тест на дружбу')
@router.message(Command('create_quiz'))
async def creat_quiz(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user_id = message.from_user.id

    user_quiz_exists = await look_user_quiz(session, user_id)
    if user_quiz_exists == True:
        del_message = await message.answer("🌟У вас уже есть тест для друга,\n"
                                           "удалите его, чтобы создать новый!🌟",
                                                 reply_markup=del_quiz())

        await state.update_data(
            del_message_id=del_message.message_id
        )
        return


    intro_msg = await message.answer("😉 Отвечай четсно",
                                     reply_markup=ReplyKeyboardRemove())

    await state.set_state(FriendTest.QUIZ)
    await state.update_data(
        current_question=0,
        user_answers=[],
        intro_message_id=intro_msg.message_id
    )

    await send_question(message.chat.id, 0, message.message_id, state, bot)


@router.callback_query(F.data.startswith("answer_"), FriendTest.QUIZ)
async def process_answer(call: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    user_id = call.from_user.id
    user_name = call.from_user.username

    _, q_idx, a_idx = call.data.split("_")
    question_index = int(q_idx)
    answer_index = int(a_idx)

    data = await state.get_data()
    user_answers = data.get("user_answers", [])
    reverse_test_friend = data.get("reverse_test_friend")

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
        await send_question(call.message.chat.id, next_index, call.message.message_id, state, bot)
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
            except Exception:
                pass

        # Отправляем результаты отдельным сообщением
        summary = "\n".join(
            f"{FRIEND_TEST[i]['question_for_user']}: {ans}" for i, ans in enumerate(user_answers)
        )
        await state.clear()

        ser_answers_only = " ".join(re.findall(r":\s*(.*?)(?:\n|$)", summary))
        await add_user_answer(session, ser_answers_only, user_id, user_name)

        bot_user = await bot.get_me()
        bot_name = bot_user.username
        link_generator = PollLinkGenerator(bot_name)
        encrypted_link = link_generator.generate_link(user_id)

        # await bot.send_message(
        #     chat_id=user_id,
        #     text=f"🎉 *ОПРОС УСПЕШНО ЗАВЕРШЁН!* 🎉\n\n"
        #          f"━━━━━━━━━━━━━━━━━━━━\n"
        #          f"📣 Теперь <b>поделитесь ссылкой</b> с друзьями:\n"
        #          f"«Пусть они тоже испытают этот крутой вызов!»\n\n"
        #          f"🚀 Ссылка для друзей:\n"
        #          f"{encrypted_link}"
        # )

        if reverse_test_friend == True:

            await bot.send_message(
                chat_id=user_id,
                text=f"🎉 ОПРОС УСПЕШНО ЗАВЕРШЁН! 🎉\n\n"
                     f"━━━━━━━━━━━━━━━━━━━━\n"
                     f"📣 Теперь <b>поделитесь ссылкой</b> с друзьями:\n"
                     f"«Узнай, на сколько хорошо знают тебя твои друзья»\n\n"
                     f"🚀 *Ссылка для друзей:*\n"
                     f"<code>{encrypted_link}</code>\n\n"
                     f"🔥 Чем больше участников — тем жарче соревнование!",
                reply_markup=reverse_link_friend_bk(encrypted_link),
                parse_mode="HTML"
            )
            await state.update_data(reverse_test_friend=False)


        else:
            await bot.send_message(
                chat_id=user_id,
                text=f"🎉 ОПРОС УСПЕШНО ЗАВЕРШЁН! 🎉\n\n"
                     f"━━━━━━━━━━━━━━━━━━━━\n"
                     f"📣 Теперь <b>поделитесь ссылкой</b> с друзьями:\n"
                     f"«Узнай, на сколько хорошо знают тебя твои друзья»\n\n"
                     f"🚀 *Ссылка для друзей:*\n"
                     f"<code>{encrypted_link}</code>\n\n"
                     f"🔥 Чем больше участников — тем жарче соревнование!",
                reply_markup=link_friends(encrypted_link),
                parse_mode="HTML"
            )












