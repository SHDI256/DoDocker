from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_management_keyboard():
    btn_set = InlineKeyboardButton('Пересобрать контейнер', callback_data='rebuild')
    btn_change = InlineKeyboardButton('Удалить контейнер', callback_data='delete')

    return InlineKeyboardMarkup().row(btn_set, btn_change)
