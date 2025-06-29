import toml

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

config = toml.load('config.toml')
ADMIN_IDS = [config["support"]["id1"]]




@router.message(Command("help"))
async def sending_mes(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        return

    await message.answer('/look_users - Посмотреть всех пользователей\n'
                         '/sending_mes - Отправить рассылку\n'
                         '/ban_message - Заблокировать отпраку сообщений\n'
                         '/del_quiz_passed - Удалить таблицу с тестами и с passed\n'
                         'mes_user - отправка сообщения по айди'
                         '')

