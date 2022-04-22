from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard():
    btn_new = InlineKeyboardButton('Новый контейнер', callback_data='new')
    btn_my = InlineKeyboardButton('Мои контейнеры', callback_data='my')
    btn_req = InlineKeyboardButton('Требования к программе', callback_data='req')
    btn_how = InlineKeyboardButton('Как это работает?', callback_data='how')
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(btn_new)
    keyboard.row(btn_my, btn_req)
    keyboard.row(btn_how)

    return keyboard
