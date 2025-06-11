from aiogram.filters.callback_data import CallbackData


class Paginator(CallbackData, prefix="pag"):
    action: str
    page: int

class SelectQuestion(CallbackData, prefix="sel_q"):
    question_id: str

class Control(CallbackData, prefix="ctrl"):
    action: str

class QuizAnswer(CallbackData, prefix="quiz_a"):
    question_id: str
    answer_text: str
