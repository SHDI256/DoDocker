from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_for_support_message(text, data):
    btn = InlineKeyboardButton(text, callback_data=data)
    return InlineKeyboardMarkup().add(btn)
