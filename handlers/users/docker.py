from aiogram import types
from loader import dp, bot, Session

from states.user_states import BaseStates
from utils.docker_api.get_container import get_container
from data.config import BOT_TOKEN

from data.db_api.create_tables import User

import urllib


@dp.message_handler(state=BaseStates.all_states[2], content_types=['document'])
async def get_archive(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    state_data = await state.get_data()

    await message.answer('Принято!')
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = message.document.file_name
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{fi}', f'./{name}')
    key = await get_container(name, './program')
    await message.answer(f'Контейнер готов! \n\nЧтобы получить его, используйте ключ:\n{key}\n\n'
                         f'на сайте\n127.0.0.1:5000')
