import logging

from aiogram import types, Bot

import config
import text_answer


bot = Bot(config.BOT_TOKEN)

# Показать сообщение об Боте
async def about_info_bot(message: types.Message):
    logging.info(f'INFO about bot User {message.from_user.id}')
    await message.answer(text=text_answer.INFO_BOT, parse_mode='HTML')
