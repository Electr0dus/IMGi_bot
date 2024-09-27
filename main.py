import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import actions
import config
import reg_func
from IMGi_bot.DB import db_error, db_rating, db_photo, db_user, db_set_img, db_technikal

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')

# Начало работы ботав
dp.message_handler(commands=['start'])(reg_func.start_bot)
# Регистрация пользователя в боте
dp.message_handler(commands=['register'])(reg_func.register_bot)
dp.message_handler(state=actions.RegisterAction.username)(reg_func.add_db_users)
# Генерация изображения
dp.message_handler(text=['Генерация изображения👨‍🎨'])(reg_func.st_generate_photo)
dp.message_handler(state=actions.GenerateAction.prompt)(reg_func.st_get_file_name)
dp.message_handler(state=actions.GenerateAction.file_name)(reg_func.generate_photo)
# Сохранение сгенерированного изображения
# dp.callback_query_handler(text='save')(reg_func.save_image)
# Сгенерировать заново изображение
dp.callback_query_handler(text='repeat')(reg_func.repeat_image)
# Сохранить сгенерированное изображение
dp.callback_query_handler(text='save')(reg_func.save_gen_image)


def main():
    db_user.create_db()  # Создание таблицы с пользователем
    db_set_img.create_db()  # Создание таблицы с настройками генерации фото
    db_photo.create_db()  # Создание таблицы с хранением сгенерированных фото
    db_rating.create_db()  # Создание таблицы с рейтингом фото
    db_error.create_db()  # Создание таблицы с ошибками, оставленными пользователями
    db_technikal.create_db()  # Создание таблицы с технической информацией для действий пользователя со генерированным изображением

    logging.info('START BOT')
    executor.start_polling(dp, skip_updates=False)


# , on_startup=getIMG.generate_image

if __name__ == '__main__':
    main()
