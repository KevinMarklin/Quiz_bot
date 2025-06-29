import toml
from aiogram import Router, F, Bot
from aiogram.types import Message
import re

router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]


@router.message(F.reply_to_message)
async def handle_reply_to_user(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        return

    original = message.reply_to_message

    # 1. Пытаемся найти ID в тексте (в вашем формате)
    text = original.text or ""
    match = re.search(r'id=(\d+)', text)
    print(match)
    if match:
        target_user_id = int(match.group(1))
    # 2. Пробуем взять ID из forward_from (если сообщение было переслано)
    elif original.forward_from:
        target_user_id = original.forward_from.id
    # 3. Или просто из отправителя
    elif original.from_user:
        target_user_id = original.from_user.id
    else:
        await message.answer("⚠️ Не удалось определить, кому отправить сообщение (id не найден).")
        return

    await bot.send_message(target_user_id, f"💬 Ответ поддержки:\n\n{message.text}")
    await message.answer("✅ Сообщение отправлено пользователю.")
