from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession

from config import FRIEND_TEST
from core.database.orm_query import add_user_answer
from core.keyboards.test_friend.answer_quiz import send_question
from core.keyboards.test_friend.begin_opros import reverse_link_friend_bk
from core.keyboards.test_friend.stop_opros import stop_creat_opros

from core.states.quiz import FriendTest
from core.utils.encryption_id import PollLinkGenerator


router = Router()


@router.message(F.text == '🎯Классический тест')
async def creat_quiz(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    mes_choice = data.get("choice_mes_test")

    await bot.delete_message(chat_id=message.chat.id, message_id=mes_choice)

    intro_msg = await message.answer("<b>Будь честен с собой и с друзьями.</b>",
                                     reply_markup=stop_creat_opros())

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

        await state.clear()

        ser_answers_only = "|||".join(user_answers)
        await add_user_answer(session, ser_answers_only, user_id, user_name)

        bot_user = await bot.get_me()
        bot_name = bot_user.username
        link_generator = PollLinkGenerator(bot_name)
        encrypted_link = link_generator.generate_link(user_id)

        if reverse_test_friend == True:

            await bot.send_message(
                chat_id=user_id,
                text=f"🎉 ОПРОС УСПЕШНО ЗАВЕРШЁН! 🎉\n\n"
                     f"━━━━━━━━━━━━━━━━━━━━\n"
                     f"📣 Теперь <b>поделитесь ссылкой</b> с друзьями:\n"
                     f"«Узнай, на сколько хорошо знают тебя твои друзья»\n"
                     f"Распространите ее во всех социальных сетях и раскидайте\n\n"
                     f"🚀 *Ваша ссылка:*\n"
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
                     f"«Узнай, на сколько хорошо знают тебя твои друзья.\n"
                     f"Распространяй её во всех социальных сетях»\n\n"
                     f"🚀 <b>Ваша ссылка:</b>\n"
                     f"<code>{encrypted_link}</code>\n\n"
                     f"🔥 Чем больше участников — тем жарче соревнование!",
                reply_markup=reverse_link_friend_bk(encrypted_link),
                parse_mode="HTML"
            )











