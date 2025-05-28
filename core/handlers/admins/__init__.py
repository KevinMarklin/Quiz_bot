from aiogram import Router

from . import blockmes, answer_error_message, all_users, sending_messages

router = Router()

router.include_router(blockmes.router)
router.include_router(all_users.router)
router.include_router(answer_error_message.router)
router.include_router(sending_messages.router)