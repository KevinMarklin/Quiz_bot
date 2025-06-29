import toml
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import re
from aiogram.filters import Command
from core.states.admin import Mess

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


@router.message(Command("mes_user"))
async def mes_user(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Введите айди пользователя")

    await state.set_state(Mess.MES_USER)


@router.message(Mess.MES_USER)
async def mes_user2(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(id_mes_user=message.text)
    await message.answer("Введите текст")
    await state.set_state(Mess.MES_TEXT)


@router.message(Mess.MES_TEXT)
async def mes_user2(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(text_mes_user=message.text)
    data = await state.get_data()
    mes_id = data.get("id_mes_user")
    mes_text = data.get("text_mes_user")
    try:
        await bot.send_message(chat_id=mes_id, text=mes_text)
        await message.answer("✅ Сообщение отправлено")
    except Exception as e:
        print(e)
        await message.answer("Ошибка отправления ответа")

    await state.clear()