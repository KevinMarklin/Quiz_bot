import toml
from aiogram import Router, F, Bot
from aiogram.types import Message
import re

router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]


@router.message(F.reply_to_message)
async def handle_reply_to_user(message: Message, bot: Bot):

    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        return

    original_text = message.reply_to_message.text

    # Извлекаем ID из оригинального сообщения
    match = re.search(r'id=(\d+)', original_text)

    if match:
        user_id = int(match.group(1))  # приводим к int
        await bot.send_message(user_id, f"💬 Ответ поддержки:\n\n{message.text}")
        await message.answer("✅ Сообщение отправлено пользователю.")
    else:
        await message.answer("⚠️ Не удалось определить, кому отправить сообщение (id не найден).")
