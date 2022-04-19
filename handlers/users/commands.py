from aiogram import types
from loader import dp, Session

from data.db_api.create_tables import User

from states.user_states import BaseStates


@dp.message_handler(state='*', commands=['support'])
async def set_support_state(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BaseStates.all_states[1])

    await message.answer('Отправьте сообщение в поддержку')


@dp.message_handler(state='*', commands=['bot'])
async def set_bot_state(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BaseStates.all_states[0])

    await message.answer('Вы перешли в режим взаимодействия с ботом')


@dp.message_handler(state='*', commands=['docker'])
async def set_docker_state(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    state_data = await state.get_data()

    if message.from_user.id in [user.id_user for user in Session.query(User).all()]:
        await state.set_state(BaseStates.all_states[2])

        await message.answer('Бот готов! Отправьте вашу программу в формате .zip')

    else:
        await message.answer('Вы не зарегистрированы!')
