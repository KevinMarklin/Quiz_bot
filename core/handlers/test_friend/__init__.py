from .import begin_opros, del_quiz, quiz, stop_quiz
from aiogram import Router

router = Router()

router.include_router(quiz.router)
router.include_router(del_quiz.router)
router.include_router(begin_opros.router)
router.include_router(stop_quiz.router)
