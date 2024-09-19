import logging

from aiogram import Bot, Dispatcher, executor

import config
import func_main
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')



dp.message_handler(commands=['start'])(func_main.start_bot)

def main():
    logging.info('START BOT')
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
