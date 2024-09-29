import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import getIMG
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_rating, db_technikal

bot = Bot(config.BOT_TOKEN)


async def set_style(message: types.Message):
    with open('image_for_settings/style.png', mode='rb') as file:
        await bot.send_photo(chat_id=message.from_user.id, photo=file)
    await message.answer(text='Check', parse_mode='HTML')

