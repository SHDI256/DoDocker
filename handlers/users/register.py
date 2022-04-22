from aiogram import types
from loader import dp, bot, Session, engine

from states.user_states import BaseStates, RegisterStates

from keyboards.inline.register import get_keyboard_for_register
from keyboards.default.main_menu import get_main_menu_keyboard

from data.db_api.create_tables import User, Containers, Base

import re


@dp.callback_query_handler(lambda call: call.data == 'ok', state='*')
async def set_register_state_after_callback(call: types.CallbackQuery):
    if call.from_user.id not in [user.id_user for user in Session.query(User).all()]:
        state = dp.current_state(user=call.from_user.id)
        await state.set_state(RegisterStates.all_states[0])

        name = call.from_user.username
        if name == 'None':
            await state.set_state(RegisterStates.all_states[1])
            await bot.send_message(call.from_user.id, 'Придумайте свой новый никнейм')

        else:
            kb = get_keyboard_for_register()

            await bot.send_message(call.from_user.id, f'Никнейм по умолчанию: {name}\n\nПродолжить регистрацию?',
                                 reply_markup=kb)

        await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'why', state='*')
async def why_register(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Зачем регистрироваться? Учётная запись даёт доступ ко всем функциям бота, '
                                              'позволяя не только создавать контейнеры, но и управлять ими. Также Вы можете опробовать бота один раз прямо сейчас!')

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'later', state='*')
async def cancel_register(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Обязательно возвращайтесь!')

    await call.answer()


@dp.message_handler(state='*', commands=['register'])
async def set_register_state_after_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(RegisterStates.all_states[0])

    name = message.from_user.username
    if name == 'None':
        await state.set_state(RegisterStates.all_states[1])
        await message.answer('Придумайте свой новый никнейм')

    else:
        kb = get_keyboard_for_register()

        await message.answer(f'Никнейм по умолчанию: {name}\n\nПродолжить регистрацию?',
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
    try:
        if message.text == re.findall(re.compile('.+@.+[.].+'), message.text)[0]:

            state = dp.current_state(user=message.from_user.id)
            state_data = await state.get_data()

            if message.from_user.id in [user.id_user for user in Session.query(User).all()]:
                await message.answer('Вы уже зарегистрированы!')

            else:
                new_user = User()
                new_user.id_user = message.from_user.id
                new_user.name = state_data['nickname']
                new_user.email = message.text
                Session.add(new_user)
                Session.commit()

                keyboard = get_main_menu_keyboard()

                await message.answer('Регистрация прошла успешно!', reply_markup=keyboard)

            await state.set_state(BaseStates.all_states[0])

        else:
            await message.answer('Некорректный email, попробуйте ещё раз')

    except Exception:
        await message.answer('Некорректный email, попробуйте ещё раз')
