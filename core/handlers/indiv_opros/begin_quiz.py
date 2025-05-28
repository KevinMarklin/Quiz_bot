from aiogram import types, F, Router, Bot


router = Router()




@router.message(F.text == '📖Создать свой опрос')
async def creat_quiz(message: types.Message, bot: Bot):
    await message.answer("В разработке")

