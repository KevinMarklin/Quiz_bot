from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    LOCKED = State()

class Sending(StatesGroup):
    SEND = State()

class Mess(StatesGroup):
    MES_USER = State()
    MES_TEXT = State()