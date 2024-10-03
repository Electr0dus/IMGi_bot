import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import getIMG
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_error

bot = Bot(config.BOT_TOKEN)


#Активировать состояние для написание ошибки пользователем о работе бота
async def actions_error_user(message: types.Message):
    await message.answer(text=text_answer.ERROR_MESSAGE, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    await actions.ErrorActions.message_error.set()

# Записать в БД ошибку отправленную пользователем
async def write_error_user(message: types.Message, state):
    logging.warning(f'Add ERROR User {message.from_user.id}')
    await state.update_data(error=message.text)
    data_error = await state.get_data()
    # Записать ошибку в БД
    db_error.write_error(message.from_user.id, data_error['error'])
    await message.answer(text=text_answer.ANSWER_ABOUT_ERROR, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)