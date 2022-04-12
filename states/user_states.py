from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    STATE_BOT = State()
    STATE_SUPPORT = State()
    