from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard():
    btn_new = KeyboardButton('Новый контейнер')
    btn_my = KeyboardButton('Мои контейнеры')
    btn_req = KeyboardButton('Требования к программе')
    btn_how = KeyboardButton('Как это работает?')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(btn_new)
    keyboard.row(btn_my, btn_req)
    keyboard.row(btn_how)

    return keyboard

def get_main_menu_not_reg_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Опробовать!'))
