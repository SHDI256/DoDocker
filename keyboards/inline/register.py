from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_for_register(texts, data):
    btn_set = InlineKeyboardButton(texts[0], callback_data=data[0])
    btn_change = InlineKeyboardButton(texts[1], callback_data=data[1])
    return InlineKeyboardMarkup().row(btn_set, btn_change)
