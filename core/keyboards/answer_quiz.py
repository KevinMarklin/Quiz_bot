
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import FRIEND_TEST


def builds_keyboard(question_index: int, answers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, answer in enumerate(answers):
        builder.button(
            text=answer["text"],
            callback_data=f"answer_{question_index}_{i}"
        )
    builder.adjust(2)
    return builder.as_markup()


async def send_question(chat_id: int, question_index: int, message_id: int, state: FSMContext, bot: Bot):
    question = FRIEND_TEST[question_index]
    markup = builds_keyboard(question_index, question["answers"])

    # Попробуем обновить сообщение, если уже есть
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=question["image_url"], caption=question["question"]),
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
            caption=question["question"],
            reply_markup=markup
        )
        await state.update_data(current_question_message_id=msg.message_id)




def link_friends(encrypted_link):
    kb = InlineKeyboardBuilder()
    kb.button(text="📤 Отправить друзьям",
    url=f"https://t.me/share/url?url={encrypted_link}&text=🔥СЕРЬЁЗНЫЙ ВЫЗОВ!🔥\n"
        f"Ты уверен, что знаешь меня на 11/11?")
    return kb.as_markup()