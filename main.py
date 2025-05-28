import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from core.middlewares.is_locked import AccessMiddleware
from config import Config
from core.middlewares.db import DatabaseMiddleware
from core.handlers import setup_handlers
from core.database.factory import creat_db, session_maker


async def main():
    await creat_db()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    config = Config.from_file("config.toml")

    dp = Dispatcher()

    dp.update.middleware(DatabaseMiddleware(session_pool=session_maker))


    setup_handlers(dp)
    dp.message.middleware(AccessMiddleware())

    bot = Bot(config.telegram.bot_token, default=DefaultBotProperties(parse_mode='HTML'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа прервана админом.")