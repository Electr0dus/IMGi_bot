from aiogram import types
import text_answer
import logging
# Функция приветсвия по команде /start
async def start_bot(messega: types.Message):
    logging.info('COMMAND "START" username - ' + messega.from_user.username)
    await messega.answer(text=text_answer.START_BOT, parse_mode='HTML')