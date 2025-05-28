from aiogram.fsm.state import StatesGroup, State


class Donate(StatesGroup):
        AMOUNT_STARS = State()