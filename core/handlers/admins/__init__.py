from aiogram import Router

from . import blockmes, answer_error_message, all_users, sending_messages, mes_admin, del_quiz_passed

router = Router()

router.include_router(blockmes.router)
router.include_router(all_users.router)
router.include_router(answer_error_message.router)
router.include_router(sending_messages.router)
router.include_router(mes_admin.router)
router.include_router(del_quiz_passed.router)