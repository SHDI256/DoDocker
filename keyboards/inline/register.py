from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_for_register():
    btn_set = InlineKeyboardButton('Да', callback_data='set')
    btn_change = InlineKeyboardButton('Нет, сменить никнейм', callback_data='change')

    return InlineKeyboardMarkup().row(btn_set, btn_change)


def get_preparation_keyboard():
    btn_ok = InlineKeyboardButton('Да!', callback_data='ok')
    btn_why = InlineKeyboardButton('Зачем?', callback_data='why')
    btn_cancel = InlineKeyboardButton('Позже', callback_data='later')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(btn_ok)
    keyboard.row(btn_why, btn_cancel)

    return keyboard


def get_trial_access_keyboard():
    btn_ok = InlineKeyboardButton('Попробовать!', callback_data='start_trial')
    btn_back = InlineKeyboardButton('Назад', callback_data='back')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(btn_ok, btn_back)

    return keyboard
