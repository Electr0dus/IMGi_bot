import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_rating, db_technikal

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
    await message.answer(text=text_answer.NAME_FILE_SHOWN, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    # Вывести имена всех существующих фото пользователя
    await message.answer(text=f'<b>Ваши изображения:</b>📁\n<em>{message_name_file}</em>',
                         parse_mode='HTML',
                         reply_markup=keyboards.kb_cancel_sh)
    await actions.ShownImageActions.name_image.set()

# Выйти из просмотра всех файлов
async def exit_sh_file(call: types.CallbackQuery, state):
    await call.message.delete()
    await state.finish()
    await call.message.answer(text=text_answer.CANCEL_IMAGE_BOT, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)

# Активировали машину состояний и ждём имени файла или отмены показа изображений
async def actions_shown_image(message: types.Message, state):
    await state.update_data(name_image=message.text)
    data_image = await state.get_data() # Получить имя файла, который необходимо открыть
    path_local = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user'
    try:
        with open(f"{path_local}/{message.from_user.id}/{data_image['name_image']}", mode='rb') as file_image:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=file_image,
                                 reply_markup=keyboards.kb_open_image)
            logging.info(f"User {message.from_user.id} open file {data_image['name_image']}")
    except FileNotFoundError:
        await message.answer(text=f"❌<b>ФАЙЛА <em>\"{data_image['name_image']}\"</em> НЕ СУЩЕСТВУЕТ</b>❌",
                             parse_mode='HTML')
        logging.info(f"User {message.from_user.id} the file does not exist {data_image['name_image']}")

