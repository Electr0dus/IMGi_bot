import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import getIMG
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_rating, db_technikal, db_tech_image

bot = Bot(config.BOT_TOKEN)

# Вызвать функцию оценки изображения
async def like_image(message: types.Message):
    logging.info(f'Open like image User: {message.from_user.id}')
    # Костыль, чтобы скрыть основную клавиатуру
    await message.answer(text=message.text, reply_markup=types.ReplyKeyboardRemove())
    await message.delete()
    # Получить список изображений для вывода их пользователю для оценки
    # data_image[current_number][0] - имя файла data_image[current_number][1] - папка где файл хранится
    # Получить значение текущей записи, чтобы потом увеличить его и перезаписать в БД
    current_number = db_tech_image.get_current_number(message.from_user.id)
    data_image = db_photo.get_all_image()
    path_image = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user' #Путь для вывода изображений

    # Открыть изображения для просмотра
    with open(f'{path_image}/{data_image[current_number][1]}/{data_image[current_number][0]}', mode='rb') as file_name:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=file_name,
                             reply_markup=keyboards.kb_like_image)
    # Увеличить значение
    current_number += 1
    # Записать новое значение в БД
    db_tech_image.add_current_number(message.from_user.id, current_number)

# Выход в основное меню
async def exit_to_main(call: types.CallbackQuery):
    # Затереть значение текущего изображения в 1 чтобы с самого начала можно было начать просмотр
    db_tech_image.add_current_number(call.from_user.id, 0)
    await call.message.delete()
    await call.message.answer(text=text_answer.CANCEL_IMAGE_BOT,
                              parse_mode='HTML',
                              reply_markup=keyboards.kb_main_menu)

# Просмотр изображений далее
async def next_image_like(call: types.CallbackQuery):
    # Получить значение текущей записи, чтобы потом увеличить его и перезаписать в БД
    current_number = db_tech_image.get_current_number(call.from_user.id)
    max_number_image = db_photo.get_all_count()
    if current_number < max_number_image:
        data_image = db_photo.get_all_image()
        path_image = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user' #Путь для вывода изображений
        # Открыть изображения для просмотра
        with open(f'{path_image}/{data_image[current_number][1]}/{data_image[current_number][0]}', mode='rb') as file_name:
            await bot.send_photo(chat_id=call.from_user.id,
                                 photo=file_name,
                                 reply_markup=keyboards.kb_like_image)
        # Увеличить значение
        current_number += 1
        # Записать новое значение в БД
        db_tech_image.add_current_number(call.from_user.id, current_number)
    else: #вывести, что все фото просмотрены и на выбор два действия, начать заново, либо выйти из меню просмотра
        await call.message.answer(text=text_answer.ENDING_IMAGE_LIKE,
                                  parse_mode='HTML',
                                  reply_markup=keyboards.kb_ending_image)

# Реализация, когда долистали доконца и нажали начать заново
async def repeat_shown_image(call: types.CallbackQuery):
    # Затереть значение текущего изображения в 1 чтобы с самого начала можно было начать просмотр
    db_tech_image.add_current_number(call.from_user.id, 0)
    await call.message.delete()
    current_number = db_tech_image.get_current_number(call.from_user.id)
    data_image = db_photo.get_all_image()
    path_image = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user'  # Путь для вывода изображений

    # Открыть изображения для просмотра
    with open(f'{path_image}/{data_image[current_number][1]}/{data_image[current_number][0]}', mode='rb') as file_name:
        await bot.send_photo(chat_id=call.from_user.id,
                             photo=file_name,
                             reply_markup=keyboards.kb_like_image)
    # Увеличить значение
    current_number += 1
    # Записать новое значение в БД
    db_tech_image.add_current_number(call.from_user.id, current_number)