import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_rating, db_technikal, db_tech_image

bot = Bot(config.BOT_TOKEN)

# Отправить пользователю изображение с наибольшим колличеством лайков
async def switch_rating_image(message: types.Message):
    await message.answer(text=text_answer.PLACE_IMG,
                         parse_mode='HTML',
                         reply_markup=keyboards.kb_switch_rating)


# Вывод всех изображений Первого места
async def shown_first_place(call: types.CallbackQuery):
    logging.info(f'GET First place User {call.from_user.id}')
    # Путь для открытия фала для вывода изображения
    file_path = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user'
    # Получить значение максимальных лайков для первого места
    data_max_like = db_rating.get_max_like(1)
    # file_name[0] - имя файла file_name[1] - кол-во лайков file_name[2] - имя папки пользователя file_name[3] - имя автора изображения
    for file_name in data_max_like:
        with open(f'{file_path}/{file_name[2]}/{file_name[0]}', mode='rb') as file_img:
            # Отправить фото пользователю
            await bot.send_photo(chat_id=call.from_user.id,
                                 photo=file_img,
                                 caption=f'🥇\n'
                                         f'<b>Имя автора®️: <em>{file_name[3]}</em></b>\n'
                                         f'<b>Число лайков👍: <em>{file_name[1]}</em></b>',
                                 parse_mode='HTML')
        with open(f'{file_path}/{file_name[2]}/{file_name[0]}', mode='rb') as file_img:
            # Отправить сразу документ для скачивания изображения
            await bot.send_document(chat_id=call.from_user.id,
                                    document=file_img)

# Вывод всех изображений Второго места
async def shown_second_place(call: types.CallbackQuery):
    logging.info(f'GET Second place User {call.from_user.id}')
    # Путь для открытия фала для вывода изображения
    file_path = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user'
    # Получить значение максимальных лайков для первого места
    data_max_like = db_rating.get_max_like(2)
    # file_name[0] - имя файла file_name[1] - кол-во лайков file_name[2] - имя папки пользователя file_name[3] - имя автора изображения
    for file_name in data_max_like:
        with open(f'{file_path}/{file_name[2]}/{file_name[0]}', mode='rb') as file_img:
            # Отправить фото пользователю
            await bot.send_photo(chat_id=call.from_user.id,
                                 photo=file_img,
                                 caption=f'🥈\n'
                                         f'<b>Имя автора®️: <em>{file_name[3]}</em></b>\n'
                                         f'<b>Число лайков👍: <em>{file_name[1]}</em></b>',
                                 parse_mode='HTML')
        with open(f'{file_path}/{file_name[2]}/{file_name[0]}', mode='rb') as file_img:
            # Отправить сразу документ для скачивания изображения
            await bot.send_document(chat_id=call.from_user.id,
                                    document=file_img)


# Вывод всех изображений Первого места
async def shown_third_place(call: types.CallbackQuery):
    logging.info(f'GET Third place User {call.from_user.id}')
    # Путь для открытия фала для вывода изображения
    file_path = 'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/generic_photo_user'
    # Получить значение максимальных лайков для первого места
    data_max_like = db_rating.get_max_like(3)
    # file_name[0] - имя файла file_name[1] - кол-во лайков file_name[2] - имя папки пользователя file_name[3] - имя автора изображения
    for file_name in data_max_like:
        with open(f'{file_path}/{file_name[2]}/{file_name[0]}', mode='rb') as file_img:
            # Отправить фото пользователю
            await bot.send_photo(chat_id=call.from_user.id,
                                 photo=file_img,
                                 caption=f'🥉\n'
                                         f'<b>Имя автора®️: <em>{file_name[3]}</em></b>\n'
                                         f'<b>Число лайков👍: <em>{file_name[1]}</em></b>',
                                 parse_mode='HTML')
        with open(f'{file_path}/{file_name[2]}/{file_name[0]}', mode='rb') as file_img:
            # Отправить сразу документ для скачивания изображения
            await bot.send_document(chat_id=call.from_user.id,
                                    document=file_img)
