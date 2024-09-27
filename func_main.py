import logging

from aiogram import types, Bot

import actions
import config
import getIMG
import keyboards
import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_error, db_rating

bot = Bot(config.BOT_TOKEN)


# Функция приветсвия по команде /start
async def start_bot(messega: types.Message):
    logging.info(f'COMMAND "START" username - {messega.from_user.id}')  # + messega.from_user.username
    await messega.answer(text=text_answer.START_BOT, parse_mode='HTML')


# Функция для регистрации /register
async def register_bot(message: types.Message):
    await message.answer(text=text_answer.REGISTER_BOT, parse_mode='HTML')
    await actions.RegisterAction.username.set()


# Функция для проверки регистрации пользователей и добавление их в бд
async def add_db_users(message: types.Message, state):
    await state.update_data(username=message.text)
    username = await state.get_data()  # Получить переданное имя пользователя
    # проверить на отсутсвие данного пользователя в БД
    if db_user.check_users(message.from_user.id):
        db_user.create(message.from_user.id, username['username'])
        db_set_img.create_user_id(message.from_user.id)
        db_photo.create_user_id(message.from_user.id)
        db_error.create_user_id(message.from_user.id)
        db_rating.create_user_id(message.from_user.id, username['username'])
    else:
        # Ответить что данный пользователь уже есть
        logging.warning(f'User {message.from_user.id} is register')
        await message.answer(text=text_answer.IS_ADD_BD, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)
        await state.finish()
        return
    # поздравить с успещной регистрацией
    logging.info(f'User {message.from_user.id} successfully register')
    await message.answer(text=text_answer.TRUE_REGISTER_USER, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)
    await state.finish()


# Функция для активации состояния для генерации изображения
async def st_generate_photo(message: types.Message):
    await message.answer(text=text_answer.GENERATE_BOT, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    await actions.GenerateAction.prompt.set()


# Функция для получения имени файла от пользователя ввиде (myFile.png)
async def st_get_file_name(message: types.Message, state):
    await state.update_data(prompt=message.text)
    await message.answer(text=text_answer.FILE_NAME_BOT, parse_mode='HTML')
    await actions.GenerateAction.file_name.set()


# функция для отработки генерации изображения
async def generate_photo(message: types.Message, state):
    # {'prompt': 'мот', 'file_name': 'мойфайл.png'} - Вывод данных полученных от пользователя
    await state.update_data(file_name=message.text)
    data = await state.get_data()
    # Проверить, что файл назван правильно и что этого файла нет в базе данных для конкретного пользователя!!!!
    if getIMG.check_name_file(data['file_name']):  # Проверить корректность ввода файла
        if db_photo.check_photo(data['file_name'],
                                message.from_user.id):  # Проверить, что такогоже файла болешь нет в БД
            await message.answer(text=text_answer.DELAY_GEN_IMAGE)
            await getIMG.generate_image(prompt=data['prompt'], file_name=data['file_name'])
            # Отправка фото пользователю
            with open(f"generic_photo_user/{data['file_name']}", mode='rb') as file:
                await bot.send_photo(chat_id=message.from_user.id, photo=file, reply_markup=keyboards.kb_save_img)
        else:
            logging.warning(f"This file is already in the database: {data['file_name']}")
            await message.answer(text=text_answer.ERROR_NAME_FILE, parse_mode='HTML')
            # Вывести имена всех существующих фото пользователя
            await message.answer(text=db_photo.get_all_photo(message.from_user.id))
            # Вернуть обратно в состояние ввода имени файла
            await actions.GenerateAction.file_name.set()
            return 0
    else:
        logging.warning(f"Invalid file name: {data['file_name']}")
        await message.answer(text=text_answer.ERROR_CORRECT_FILE, parse_mode='HTML')
        # Вернуть обратно в состояние ввода имени файла
        await actions.GenerateAction.file_name.set()
        return 0
    # Если файл назван не правильно или такой файл уже существует то отправить на состояние заново, другое имя должен будет придумать
    # чтобы пользователь придумывал другое имя и при этом вывести ему все существующие названия файлов под его user_id
    await state.finish()


# Функция для сохранения сгенерированного ботом фото
async def save_image(call, state):
    data = await state.get_data()
    print(data)


# Сгенерировать заново изображение
async def repeat_image(call: types.CallbackQuery):
    pass