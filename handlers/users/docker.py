from aiogram import types
from loader import dp, bot, Session

from states.user_states import BaseStates, ManagementStates
from utils.docker_api.get_container import get_container
from data.config import BOT_TOKEN, PASSWORD

from data.db_api.create_tables import User, Containers, TrialAccess

from keyboards.inline.management import get_management_keyboard

import urllib

from server import public_url

import os


@dp.message_handler(state=BaseStates.all_states[3])
async def set_container_name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text not in [container.name for container in Session.query(Containers)]:
        await state.update_data(container_name=message.text)
        await state.set_state(BaseStates.all_states[2])

        await message.answer('Название установлено! Отправьте вашу программу в формате .zip')

    else:
        await message.answer('Такое имя уже существует. Пожалуйста, придумайте другое')


@dp.message_handler(state=BaseStates.all_states[2], content_types=['document'])
async def get_archive(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    state_data = await state.get_data()

    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = message.document.file_name

    if name[-4:] != '.zip':
        await message.answer('Программа отправлена не в формате .zip!')

    else:
        await message.answer('Принято!')
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{fi}', f'./{name}')
        key = await get_container(name, './program')

        if not key:
            await message.answer('Отсутствует или неправильно назван главный файл!')
        else:
            await message.answer(f'Контейнер готов! \n\nЧтобы получить его, используйте ключ:\n{key}\n\n'
                                 f'на сайте\n{public_url}')

            if message.from_user.id not in [user.id_user for user in Session.query(TrialAccess).all()]:
                new_trial = TrialAccess()
                new_trial.id_user = message.from_user.id
                Session.add(new_trial)
                Session.commit()

            new_container = Containers()
            new_container.key = key
            new_container.user = Session.query(User).filter(User.id_user == message.from_user.id).first()
            new_container.name = state_data['container_name']
            Session.add(new_container)
            Session.commit()

            await state.set_state(BaseStates.all_states[0])


@dp.callback_query_handler(lambda call: call.data == 'new', state='*')
async def new_container(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(BaseStates.all_states[3])

    await bot.send_message(call.from_user.id, 'Бот готов! Назовите ваш контейнер')

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'rebuild', state='*')
async def set_rebuild_state(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(ManagementStates.all_states[0])

    await bot.send_message(call.from_user.id, 'Введите номер контейнера, который хотите пересобрать')

    await call.answer()


@dp.message_handler(state=ManagementStates.all_states[0])
async def rebuild_container(message: types.Message):
    containers = list(Session.query(Containers).filter(Containers.user_id == message.from_user.id))

    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > len(containers):
        await message.answer('Несуществующий номер контейнера, попробуйте ещё раз')

    else:
        key = containers[int(message.text) - 1].key
        os.remove(f'containers/{key}.tar')
        os.chdir('containers')
        os.system('echo %s|sudo -S %s' % (PASSWORD, f'sudo docker save {key}:0.0 > {key}.tar'))
        os.chdir('../')

        await message.answer(f'Контейнер готов! \n\nЧтобы получить его, используйте ключ:\n{key}\n\n'
                             f'на сайте\n{public_url}')

        keyboard = get_management_keyboard()

        await bot.send_message(message.from_user.id, 'Ваши контейнеры:\n\n' + '\n'.join(
            [f'{i + 1}. {container.name}' for i, container in enumerate(containers)]),
                               reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == 'delete', state='*')
async def delete_container(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(ManagementStates.all_states[1])

    await bot.send_message(call.from_user.id, 'Введите номера контейнеров через пробел, которые хотите удалить')

    await call.answer()


@dp.message_handler(state=ManagementStates.all_states[1])
async def rebuild_container(message: types.Message):
    containers = list(Session.query(Containers).filter(Containers.user_id == message.from_user.id))

    numbers = message.text.split()
    try:
        numbers = map(int, numbers)
        for n in numbers:
            if n < 1 or n > len(containers):
                await message.answer('Несуществующий номер контейнера, попробуйте ещё раз')
                break

            else:
                key = containers[n - 1].key
                os.remove(f'containers/{key}.tar')

                Session.query(Containers).filter(Containers.key == key).delete()

        else:
            containers = list(Session.query(Containers).filter(Containers.user_id == message.from_user.id))

            if len(containers) > 0:
                keyboard = get_management_keyboard()
                await bot.send_message(message.from_user.id, 'Ваши контейнеры:\n\n' + '\n'.join(
                    [f'{i + 1}. {container.key}' for i, container in enumerate(containers)]),
                                       reply_markup=keyboard)

            else:
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(BaseStates.all_states[0])

            await message.answer('Контейнер успешно удалён!')

    except Exception:
        await message.answer('Несуществующий номер контейнера, попробуйте ещё раз')


@dp.callback_query_handler(lambda call: call.data == 'new', state='*')
async def set_new_container_state(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(BaseStates.all_states[2])

    await bot.send_message(call.from_user.id, 'Бот готов! Отправьте вашу программу в формате .zip')

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'my', state='*')
async def user_containters(call: types.CallbackQuery):
    containers = list(Session.query(Containers).filter(Containers.user_id == call.from_user.id))

    if len(containers) > 0:
        keyboard = get_management_keyboard()

        await bot.send_message(call.from_user.id, 'Ваши контейнеры:\n\n' + '\n'.join(
            [f'{i + 1}. {container.name}' for i, container in enumerate(containers)]),
                               reply_markup=keyboard)

    else:
        await bot.send_message(call.from_user.id, 'У Вас ещё нет контейнеров')

        state = dp.current_state(user=call.from_user.id)
        await state.set_state(BaseStates.all_states[0])

    await call.answer()
