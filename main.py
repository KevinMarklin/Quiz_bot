# import asyncio
# import logging
# import os
#
# from aiogram import Bot, Dispatcher
# from aiogram.client.bot import DefaultBotProperties
# from core.middlewares.is_locked import AccessMiddleware
# from config import Config
# from core.middlewares.db import DatabaseMiddleware
# from core.handlers import setup_handlers
# from core.database.factory import creat_db, session_maker
# from alembic import command
# from alembic.config import Config as AlembicConfig
#
# def run_migrations():
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     alembic_cfg = AlembicConfig(os.path.join(base_dir, "alembic.ini"))
#     command.upgrade(alembic_cfg, "head")
#
# async def main():
#     run_migrations()
#
#     print("DEBUG: DATABASE_URL =", os.getenv("DATABASE_URL"))
#
#     await creat_db()
#
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
#
#     config = Config.from_file("config.toml")
#
#     BOT_TOKEN = config.telegram.bot_token
#
#     dp = Dispatcher()
#     dp.update.middleware(DatabaseMiddleware(session_pool=session_maker))
#
#     setup_handlers(dp)
#     dp.message.middleware(AccessMiddleware())
#
#     bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
#
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
#
# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Программа прервана админом.")

