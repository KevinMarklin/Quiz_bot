from aiogram.fsm.state import StatesGroup, State


class Idea(StatesGroup):
    message_idea = State()

class Error(StatesGroup):
    message_error = State()