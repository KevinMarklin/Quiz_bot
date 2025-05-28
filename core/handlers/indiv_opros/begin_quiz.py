from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

router = Router()




@router.message(F.text == '📖Создать свой опрос')
async def creat_quiz(message: types.Message, bot: Bot):
    await message.answer("В разработке")

