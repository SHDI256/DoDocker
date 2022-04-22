from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, Session, engine
from data.db_api.create_tables import User, TrialAccess, Base

from keyboards.inline.register import get_preparation_keyboard
from keyboards.inline.main_menu import get_main_menu_keyboard


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    if message.from_user.id not in [user.id_user for user in Session.query(TrialAccess).all()]:
        new_trial = TrialAccess()
        new_trial.id_user = message.from_user.id
        new_trial.is_trial = True

    if message.from_user.id in [user.id_user for user in Session.query(User).all()]:
        keyboard = get_main_menu_keyboard()

        await message.answer('Главное меню', reply_markup=keyboard)

    else:
        keyboard = get_preparation_keyboard()

        await message.answer(f"Вас приветствует DoDocker, {message.from_user.full_name}!\nВы здесь в первый раз, "
                             f"поэтому для продолжения работы необходимо зарегистрироваться. Готовы продолжить?",
                             reply_markup=keyboard)
