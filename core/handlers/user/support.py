import toml
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from core.keyboards.back import back_menu
from core.states.support import Error

router = Router()

config = toml.load('config.toml')
SUPPORT_CHAT_ID1 = config['support']['id1']



@router.message(F.text == '🆘 Поддержка')
@router.message(Command("support"))
async def error(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer('<b>✨ Дорогой друг!✨</b>\n\n'
                         'Опиши проблему, с которой ты столкнулся!',
                         reply_markup=back_menu())

    await state.update_data(support_mes=message.text)
    await state.set_state(Error.message_error)

@router.message(Error.message_error)
async def mes_error(message: Message, state: FSMContext, bot: Bot):
    message_error = f"Сообщение от @{message.from_user.username} (id={message.from_user.id}):\n\n{message.text}"

    await bot.send_message(chat_id=SUPPORT_CHAT_ID1,
                           text=message_error)

    await message.answer('<b>✨Спасибо за обратную связь!✨</b>\n\n'
                         'Проверим всё в ближайшие 24 часа\n'
                         'Напишем, как всё исправим')
    await state.clear()


