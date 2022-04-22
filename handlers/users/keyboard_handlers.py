from aiogram import types
from loader import dp, bot, Session, engine

from states.user_states import BaseStates, RegisterStates

from keyboards.inline.management import get_management_keyboard

from data.db_api.create_tables import User, Containers, Base


@dp.message_handler(lambda msg: msg.text == 'Новый контейнер', state='*')
async def new_container(message: types.Message):
    if message.from_user.id in [user.id_user for user in Session.query(User).all()]:
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(BaseStates.all_states[2])

        await bot.send_message(message.from_user.id, 'Бот готов! Отправьте вашу программу в формате .zip')


@dp.message_handler(lambda msg: msg.text == 'Мои контейнеры', state='*')
async def user_containters(message: types.Message):
    if message.from_user.id in [user.id_user for user in Session.query(User).all()]:
        containers = list(Session.query(Containers).filter(Containers.user_id == message.from_user.id))

        if len(containers) > 0:
            keyboard = get_management_keyboard()

            await bot.send_message(message.from_user.id, 'Ваши контейнеры:\n\n' + '\n'.join(
                [f'{i + 1}. {container.key}' for i, container in enumerate(containers)]),
                                   reply_markup=keyboard)

        else:
            await bot.send_message(message.from_user.id, 'У Вас ещё нет контейнеров')

            state = dp.current_state(user=message.from_user.id)
            await state.set_state(BaseStates.all_states[0])


@dp.message_handler(lambda msg: msg.text == 'Требования к программе', state='*')
async def req(message: types.Message):
    await message.answer('Данный бот упаковывает программы Python с помощью технологии Docker. '
                                              'Всё происходит автоматически: вам лишь нужно отправить архив с программой в формате .zip, '
                                              'в котором ОБЯЗАТЕЛЬНО должен находиться главный файл (main.py либо app.py)')


@dp.message_handler(lambda msg: msg.text == 'Как это работает?ц', state='*')
async def how(message: types.Message):
    await message.answer('Поиск главного файла\nВыявление зависимостей\nСоздание Dockerfile`а\nСоздание образа\nУпаковка контейнера')
