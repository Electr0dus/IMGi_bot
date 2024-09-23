import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import func_main
import db_user
import actions
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')


#Начало работы с ботом
dp.message_handler(commands=['start'])(func_main.start_bot)
# Регистрация пользователя в боте
dp.message_handler(commands=['register'])(func_main.register_bot)
dp.message_handler(state=actions.RegisterAction)(func_main.add_db_users)

def main():
    db_user.create_db()  # Создание таблицы с пользователем
    logging.info('START BOT')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
