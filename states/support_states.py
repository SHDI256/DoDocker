from aiogram.dispatcher.filters.state import State, StatesGroup


class SupportStates(StatesGroup):
    STATE_WAIT = State()
    STATE_ANSWER = State()
