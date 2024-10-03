import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import getIMG
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_check_like, db_set_img, db_rating, db_technikal, db_tech_image

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

# Поставить лайк текущему изображению просматриваемым пользователем
async def send_like_image(call: types.CallbackQuery):
    # data_image[current_number][0] - имя файла data_image[current_number][1] - папка где файл хранится
    # Получить значение текущей записи, чтобы потом увеличить его и перезаписать в БД
    current_number = db_tech_image.get_current_number(call.from_user.id)
    # Уменьшаем значение на 1, т.к. при просмотре этот параметр уже увеличился на 1
    current_number -= 1
    data_image = db_photo.get_all_image()
    # СДЕЛАТЬ ПРОВЕРКУ НА ТО, ПОСТАВИЛ ЛИ УЖЕ ЛАЙК ДАННЫЙ ПОЛЬЗОВАТЕЛЬ ИЗОБРАЖЕНИЮ ИЛИ ЕЩЁ НЕТ
    # Если вернёт true, значит данное изображение текущий пользователь не лайкнул
    if db_check_like.check_like_image(call.from_user.id, data_image[current_number][1], data_image[current_number][0]):
        # Получить текущее значение лайков
        current_like = db_rating.get_like_current(data_image[current_number][1], data_image[current_number][0])
        # Увеличить значение лайка на один
        current_like += 1
        # Добавить в БД кто лайкнул фото и чьё это изображение с его именем
        db_check_like.add_like_image(call.from_user.id, data_image[current_number][1], data_image[current_number][0])
        # Записать новое значение лайка в БД
        db_rating.send_like_image(data_image[current_number][1], data_image[current_number][0], current_like)
        logging.info(f'Like is set image {data_image[current_number][0]} User: {call.from_user.id}')
        await call.message.answer(text=text_answer.STYLE_SUSSCES,
                              parse_mode='HTML')
    else: # Если вернуло False, значит этот пользователь уже лайкнул текущее изображение
        await call.message.answer(text=text_answer.DONT_LIKE, parse_mode='HTML')
        logging.info(f'Like WAS set image {data_image[current_number][0]} User: {call.from_user.id}')

# Сохранение фото при пролистывании всех изображений
async def save_like_image(call: types.CallbackQuery):
    # Получить текущее фото для сохранения
    current_number = db_tech_image.get_current_number(call.from_user.id)
    # Уменьшаем значение на 1, т.к. при просмотре этот параметр уже увеличился на 1
    current_number -= 1
    data_image = db_photo.get_all_image()
    logging.info(f'Save image like {data_image[current_number][0]} User: {call.from_user.id}')
    path_local = f'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user/{data_image[current_number][1]}/{data_image[current_number][0]}'
    with open(path_local, mode='rb') as file_image:
        await bot.send_document(chat_id=call.from_user.id,
                                document=file_image)

