from aiogram import Router

from . import begin_quiz

router = Router()

router.include_router(begin_quiz.router)