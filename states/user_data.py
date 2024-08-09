from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    name = State()
    age = State()
