from aiogram import types
from loader import dp, bot

from states.user_states import BaseStates
from keyboards.inline.support import get_keyboard_for_support_message
from data.config import SUPPORTS

from random import choice


@dp.message_handler(state=BaseStates.all_states[1])
async def get_message_for_support(message: types.Message):
    kb = get_keyboard_for_support_message('Ответить', message.from_user.id)

    await bot.send_message(choice(SUPPORTS), f'{message.from_user.username} спросил:\n\n{message.text}', reply_markup=kb)
    await message.answer('Ваше сообщение отправлено в поддержку!')