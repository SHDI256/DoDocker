from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, bot


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            '/bot - Взаимодействовать с ботом',
            '/register - Зарегестрироваться',
            '',
            '/docker - Упаковать программу',
            '/support - Включить саппорт-меню',
            '/req - Требования к упаковываемой программе')
    
    await message.answer("\n".join(text))


@dp.message_handler(state='*', commands=['req'])
async def set_docker_state(message: types.Message):
    await message.answer('Данный бот упаковывает программы Python с помощью технологии Docker. '
                         'Всё происходит автоматически: вам лишь нужно отправить архив с программой в формате .zip, '
                         'в котором ОБЯЗАТЕЛЬНО должен находиться главный файл (main.py либо app.py)')


@dp.callback_query_handler(lambda call: call.data == 'req', state='*')
async def req(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Данный бот упаковывает программы Python с помощью технологии Docker. '
                                              'Всё происходит автоматически: вам лишь нужно отправить архив с программой в формате .zip, '
                                              'в котором ОБЯЗАТЕЛЬНО должен находиться главный файл (main.py либо app.py)')

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'how', state='*')
async def how(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Поиск главного файла\nВыявление зависимостей\nСоздание Dockerfile`а\nСоздание образа\nУпаковка контейнера')

    await call.answer()
