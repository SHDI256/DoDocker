from aiogram import types
from loader import dp, bot, Session

from states.user_states import BaseStates, RegisterStates

from keyboards.inline.register import get_keyboard_for_register

from data.db_api.create_tables import User, Containers

import re


@dp.message_handler(state='*', commands=['register'])
async def set_register_state(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(RegisterStates.all_states[0])

    name = message.from_user.username
    buttons_text = ('Да', 'Нет, сменить никнейм')
    buttons_callback_data = ('set', 'change')
    kb = get_keyboard_for_register(buttons_text, buttons_callback_data)

    await message.answer(f'Никнейм по умолчанию :{name}\n\nПродолжить регистрацию?',
                         reply_markup=kb)


@dp.callback_query_handler(lambda call: call.data == 'set', state=RegisterStates.all_states[0])
async def change_nickname(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(RegisterStates.all_states[2])
    await state.update_data(nickname=call.from_user.username)
    await bot.send_message(call.from_user.id, 'Никнейм установлен!\n\nВаш email:')

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'change', state=RegisterStates.all_states[0])
async def change_nickname(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(RegisterStates.all_states[1])

    await bot.send_message(call.from_user.id, 'Придумайте свой новый никнейм')

    await call.answer()


@dp.message_handler(state=RegisterStates.all_states[1])
async def set_nickname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(RegisterStates.all_states[2])

    await state.update_data(nickname=message.text)

    await message.answer('Никнейм установлен!\n\nВаш email:')


@dp.message_handler(state=RegisterStates.all_states[2])
async def set_nickname(message: types.Message):
    if message.text == re.findall(re.compile('.+@.+[.].+'), message.text)[0]:

        state = dp.current_state(user=message.from_user.id)
        state_data = await state.get_data()

        user = User()
        user.name = state_data['nickname']
        user.email = message.text
        Session.add(user)
        Session.commit()

        await message.answer('Регистрация прошла успешно!')

        state = dp.current_state(user=message.from_user.id)
        await state.set_state(BaseStates.all_states[0])
    else:
        await message.answer('Некорректный email, попробуйте ещё раз')