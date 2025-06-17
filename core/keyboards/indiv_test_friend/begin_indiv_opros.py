from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import ALL_QUESTIONS_LIST
from core.keyboards.test_friend.begin_opros import build_keyboard

QUESTION_DICT = {q["id"]: q for q in ALL_QUESTIONS_LIST}

def begin_opros_indiv() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="◀️Приступить к прохождению теста"))

    return builder.as_markup(resize_keyboard=True)



async def send_question_for_user(chat_id: int, question_index: int, question_ids: list, message_id: int, state: FSMContext, bot: Bot):
    question_id = question_ids[question_index]
    question = QUESTION_DICT[question_id]
    markup = build_keyboard(question_index, question["answers"])

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=question["image_url"], caption=question["question_for_user"]),
            chat_id=chat_id,
            message_id=message_id
        )
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=markup
        )
    except:
        msg = await bot.send_photo(
            chat_id=chat_id,
            photo=question["image_url"],
            caption=question["question_for_user"],
            reply_markup=markup
        )
        await state.update_data(current_question_message_id=msg.message_id)


