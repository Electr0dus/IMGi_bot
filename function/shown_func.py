import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_tech_image

bot = Bot(config.BOT_TOKEN)


# Получить список всех изображений конкретного пользователя
async def all_image_user(message: types.Message):
    logging.info(f'User {message.from_user.id} scans files')
    # Получить все файлы с изображениями конкретного пользователя
    all_file = db_photo.get_all_photo(message.from_user.id)
    message_name_file: str = ''
    for name_image in all_file:
        for name in name_image:
            message_name_file += f'{str(name)}\n'

    # Вывести имена всех существующих фото пользователя
    await message.answer(text=f'<b>Ваши изображения:</b>📁\n<em>{message_name_file}</em>',
                         parse_mode='HTML',
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=text_answer.NAME_FILE_SHOWN, parse_mode='HTML', reply_markup=keyboards.kb_cancel_sh)
    await actions.ShownImageActions.name_image.set()

# Выйти из просмотра всех файлов
async def exit_sh_file(call: types.CallbackQuery, state):
    await call.message.delete()
    await state.finish()
    await call.message.answer(text=text_answer.CANCEL_IMAGE_BOT, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)

# Активировали машину состояний и ждём имени файла или отмены показа изображений
async def actions_shown_image(message: types.Message, state):
    await message.delete()
    await state.update_data(name_image=message.text)
    data_image = await state.get_data() # Получить имя файла, который необходимо открыть
    path_local = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user'
    try:
        with open(f"{path_local}/{message.from_user.id}/{data_image['name_image']}", mode='rb') as file_image:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=file_image,
                                 reply_markup=keyboards.kb_open_image)
            # Сохранить текущее изображение, для дальнейшего его сохранения
            db_tech_image.add_current_image(message.from_user.id, data_image['name_image'])
            logging.info(f"User {message.from_user.id} open file {data_image['name_image']}")
            await state.finish()
    except FileNotFoundError:
        await message.answer(text=f"❌<b>ФАЙЛА <em>\"{data_image['name_image']}\"</em> НЕ СУЩЕСТВУЕТ</b>❌",
                             parse_mode='HTML')
        logging.info(f"User {message.from_user.id} the file does not exist {data_image['name_image']}")

# Отмена сохранения текущего изображения
async def cancel_current_image(call: types.CallbackQuery):
    await call.message.delete()
    # Затереть данные в технической таблице текущего изображения
    db_tech_image.add_current_image(call.from_user.id, None)
    await call.message.answer(text=text_answer.OTHER_IMAGE, parse_mode='HTML', reply_markup=keyboards.kb_cancel_sh)
    await actions.ShownImageActions.name_image.set()

#Сохранение текущего выбранного изображения на устройство
async def save_current_image(call: types.CallbackQuery):
    # Получить текущее изображение для сохранения
    await call.message.delete()
    image_current = db_tech_image.get_current_image(call.from_user.id)
    path_local = f'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user/{call.from_user.id}/{image_current[0]}'
    with open(path_local, mode='rb') as file_image:
        await bot.send_document(chat_id=call.from_user.id,
                                document=file_image,
                                reply_markup=keyboards.kb_main_menu)
    # Затереть данные в технической таблице текущего изображения
    logging.info(f'File {image_current[0]} downloaded successfully User: {call.from_user.id}')
    db_tech_image.add_current_image(call.from_user.id, None)


