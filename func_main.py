from aiogram import types
import text_answer
import logging
import actions

import db_user
import db_set_img
import db_photo
import db_rating
import db_error

import keyboards

# Функция приветсвия по команде /start
async def start_bot(messega: types.Message):
    logging.info(f'COMMAND "START" username - {messega.from_user.username}')  #+ messega.from_user.username
    await messega.answer(text=text_answer.START_BOT, parse_mode='HTML')

# Функция для регистрации /register
async def register_bot(message: types.Message):
    await message.answer(text=text_answer.REGISTER_BOT, parse_mode='HTML')
    await actions.RegisterAction.username.set()

# Функция для проверки регистрации пользователей и добавление их в бд
async def add_db_users(message: types.Message, state):
    await state.update_data(username=message.text)
    username = await state.get_data() #Получить переданное имя пользователя
    #проверить на отсутсвие данного пользователя в БД
    if db_user.check_users(message.from_user.id):
        db_user.create(message.from_user.id, username['username'])
        db_set_img.create_user_id(message.from_user.id)
        db_photo.create_user_id(message.from_user.id)
    else:
        #Ответить что данный пользователь уже есть
        logging.warning(f'User {message.from_user.id} is register')
        await message.answer(text=text_answer.IS_ADD_BD, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)
        await state.finish()
        return
    #поздравить с успещной регистрацией
    logging.info(f'User {message.from_user.id} successfully register')
    await message.answer(text=text_answer.TRUE_REGISTER_USER, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)
    await state.finish()