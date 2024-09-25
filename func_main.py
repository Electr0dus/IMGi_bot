import logging

from aiogram import types, Bot
import actions
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_error, db_rating
import getIMG
import keyboards
import text_answer
import config

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


# функция для отработки генерации изображения
async def generate_photo(message: types.Message, state):
    await state.update_data(prompt=message.text)
    prompt = await state.get_data()
    await message.answer(text=text_answer.DELAY_GEN_IMAGE)
    await getIMG.generate_image(prompt=prompt['prompt'])
    # Отправка фото пользователю
    with open('generic_photo_user/user.png', mode='rb') as file:
        await bot.send_photo(chat_id=message.from_user.id, photo=file)
    await state.finish()
