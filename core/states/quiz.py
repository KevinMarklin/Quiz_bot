from aiogram.fsm.state import StatesGroup, State

class FriendTest(StatesGroup):
    QUIZ = State()

class BeginFriendTest(StatesGroup):
    OPROS = State()