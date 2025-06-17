from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, ReplyKeyboardMarkup, \
    KeyboardButton

from config import FRIEND_TEST



def begin_opros() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="▶️Приступить к прохождению теста"))

    return builder.as_markup(resize_keyboard=True)


def build_keyboard(question_index: int, answers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, answer in enumerate(answers):
        builder.button(
            text=answer["text"],
            callback_data=f"answers_{question_index}_{i}"
        )
    builder.adjust(2)
    return builder.as_markup()


async def send_question_for_user(chat_id: int, question_index: int, message_id: int, state: FSMContext, bot: Bot):
    question = FRIEND_TEST[question_index]
    markup = build_keyboard(question_index, question["answers"])

    # Попробуем обновить сообщение, если уже есть
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
        # Если не можем редактировать — отправим новое
        msg = await bot.send_photo(
            chat_id=chat_id,
            photo=question["image_url"],
            caption=question["question_for_user"],
            reply_markup=markup
        )
        await state.update_data(current_question_message_id=msg.message_id)


def reverse_link_friend_bk(encrypted_link):
    kb = InlineKeyboardBuilder()
    kb.button(text="📤 Отправить друзьям",
    url=f"https://t.me/share/url?url={encrypted_link}&text=🔥СЕРЬЁЗНЫЙ ВЫЗОВ!🔥\n"
        f"Ты уверен, что знаешь меня на 11/11?")
    return kb.as_markup()



