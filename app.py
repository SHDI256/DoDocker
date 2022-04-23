from aiogram import executor, types

from loader import dp, bot, engine
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from data.db_api.create_tables import Base

from handlers.users.start import bot_start
from handlers.users.help import bot_help


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    executor.start_polling(dp, on_startup=on_startup)