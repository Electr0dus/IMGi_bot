import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import actions
import config
from IMGi_bot.function import reg_func, setting_func
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

# Сгенерировать заново изображение
dp.callback_query_handler(text='repeat')(reg_func.repeat_image)
# Сохранить сгенерированное изображение
dp.callback_query_handler(text='save')(reg_func.save_gen_image)
# Отменить сгенерированное изображение
dp.callback_query_handler(text='cancel')(reg_func.cancel_image)

# Хэндлеры для вывода клавиатура настройки
dp.message_handler(text=['Настройки генерации⚙️'])(setting_func.menu_settings)
# Вернуться обратно в главное меню
dp.message_handler(text=['Назад🔙'])(setting_func.bact_to_main_menu)
# Вернутся в настройку генерации изображения
dp.callback_query_handler(text='back')(setting_func.bact_settings)
# Настройка стиля
dp.message_handler(text=['Стиль✨'])(setting_func.set_style)
# Установка стиля DEFAULT
dp.callback_query_handler(text='DEFAULT')(setting_func.set_DEFAULT)
# Установка стиля UHD
dp.callback_query_handler(text='UHD')(setting_func.set_UHD)
# Установка стиля ANIME
dp.callback_query_handler(text='ANIME')(setting_func.set_ANIME)
# Установка стиля KANDINSKY
dp.callback_query_handler(text='KANDINSKY')(setting_func.set_KANDINSKY)
# Установка негативного промта
dp.message_handler(text=['Негативный промт🚫'])(setting_func.call_negativ_prompt)
# Вызов машины состояния для установки значения
dp.message_handler(state=actions.NegativePromptAction.negative_prompt)(setting_func.set_negative_prompt)
# Вернутся в настройку генерации изображения
dp.callback_query_handler(state=actions.NegativePromptAction.negative_prompt, text='cancel_np')(setting_func.cancel_np)
# Зайти в меню настройки размера изображения
dp.message_handler(text=['Размер изображения🔲'])(setting_func.switch_size_image)
# Установить размер 16 на 9
dp.callback_query_handler(text='16:9')(setting_func.set_16by9)
# Установить размер 9 на 16
dp.callback_query_handler(text='9:16')(setting_func.set_9by16)
# Установить размер 3 на 2
dp.callback_query_handler(text='3:2')(setting_func.set_3by2)
# Установить размер 2 на 3
dp.callback_query_handler(text='2:3')(setting_func.set_2by3)


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
