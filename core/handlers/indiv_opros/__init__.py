from aiogram import Router

from . import begin_quiz, begin_friend

router = Router()

router.include_router(begin_quiz.router)
router.include_router(begin_friend.router)