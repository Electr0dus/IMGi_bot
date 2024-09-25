import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import func_main

from IMGi_bot.DB import db_error, db_rating, db_photo, db_user, db_set_img

import actions

import getIMG

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')


#Начало работы ботав
dp.message_handler(commands=['start'])(func_main.start_bot)
# Регистрация пользователя в боте
dp.message_handler(commands=['register'])(func_main.register_bot)
dp.message_handler(state=actions.RegisterAction)(func_main.add_db_users)
# Генерация изображения
dp.message_handler(text=['Генерация изображения👨‍🎨'])(func_main.st_generate_photo)
dp.message_handler(state=actions.GenerateAction)(func_main.generate_photo)
def main():
    db_user.create_db()  # Создание таблицы с пользователем
    db_set_img.create_db() # Создание таблицы с настройками генерации фото
    db_photo.create_db() # Создание таблицы с хранением сгенерированных фото
    db_rating.create_db() # Создание таблицы с рейтингом фото
    db_error.create_db() # Создание таблицы с ошибками, оставленными пользователями

    logging.info('START BOT')
    executor.start_polling(dp, skip_updates=False)
# , on_startup=getIMG.generate_image

if __name__ == '__main__':
    main()
