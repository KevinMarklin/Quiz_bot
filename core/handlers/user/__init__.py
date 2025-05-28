from aiogram import Router

from . import start, support, donate_author, info_test_friend

router = Router()

router.include_router(start.router)
router.include_router(support.router)
router.include_router(donate_author.router)
router.include_router(info_test_friend.router)
