from aiogram import types
from loader import dp, bot

from states.support_states import SupportStates


@dp.callback_query_handler(lambda call: call.data.isdigit(), state='*')
async def support_answer(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.update_data(to_user=call.data)
    await state.set_state(SupportStates.all_states[1])
    await bot.send_message(call.from_user.id, 'Ответьте пользователю')

    await call.answer()


@dp.message_handler(state=SupportStates.all_states[1])
async def get_support_answer(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    state_data = await state.get_data()
    await bot.send_message(state_data['to_user'], f'Ответ поддержки:\n\n{message.text}')
    await message.answer('Ваш ответ отправлен пользователю!')