import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import getIMG
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_rating, db_technikal, db_tech_image

bot = Bot(config.BOT_TOKEN)

# 