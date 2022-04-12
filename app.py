from aiogram import executor, types

from loader import dp, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.docker_api.get_container import get_container


from handlers.users.start import bot_start
from handlers.users.help import bot_help

from data.config import BOT_TOKEN

import urllib

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


@dp.message_handler(content_types=['document'])
async def get_archive(message: types.Message):
    await message.answer('Принято!')
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = message.document.file_name
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{fi}',f'./{name}')
    key = await get_container(name, './program')
    await message.answer(f'Контейнер готов! \n\n Чтобы получить его, используйте ключ:\n{key}\n\n'
                         f'на сайте\n127.0.0.1:5000')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)