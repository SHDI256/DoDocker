from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    STATE_BOT = State()
    STATE_SUPPORT = State()
    STATE_DOCKER = State()


class RegisterStates(StatesGroup):
    STATE_REGISTER = State()
    STATE_CHANGE = State()
    STATE_EMAIL = State()


class ManagementStates(StatesGroup):
    STATE_REBUILD = State()
    STATE_DELETE = State()
