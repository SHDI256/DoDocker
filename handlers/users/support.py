from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(state='*', commands=['support'])
def set_support_state(message: types.Message):
    state = await dp.get_current(message.from_user.id)
    await state.set_state()

    