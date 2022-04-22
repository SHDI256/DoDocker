from aiogram import types
from loader import dp, Session, bot

from data.db_api.create_tables import TrialAccess

from states.user_states import BaseStates

from keyboards.inline.register import get_preparation_keyboard


@dp.callback_query_handler(lambda call: call.data == 'start_trial', state='*')
async def start_trial(call: types.CallbackQuery):
    if call.from_user.id not in [user.id_user for user in Session.query(TrialAccess)]:

        state = dp.current_state(user=call.from_user.id)
        await state.set_state(BaseStates.all_states[2])

        await bot.send_message(call.from_user.id, 'Бот готов! Отправьте вашу программу в формате .zip')

    else:
        await bot.send_message(call.from_user.id, 'Ваш пробный доступ истёк, пожалуйста, зарегистрируйтесь!')

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'back', state='*')
async def start_trial(call: types.CallbackQuery):
    keyboard = get_preparation_keyboard()

    await bot.send_message(call.from_user.id, f"Вас приветствует DoDocker, {call.from_user.full_name}!\nВы здесь в первый раз, "
                                              "поэтому для продолжения работы необходимо зарегистрироваться. Готовы продолжить?",
                           reply_markup=keyboard)

    await call.answer()
