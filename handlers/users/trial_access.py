from aiogram import types
from loader import dp, Session, bot

from data.db_api.create_tables import User

from states.user_states import BaseStates


@dp.callback_query_handler(lambda call: call.data == 'start_trial', state='*')
async def start_trial(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(BaseStates.all_states[2])

    await bot.send_message(call.from_user.id, 'Бот готов! Отправьте вашу программу в формате .zip')

    await call.answer()