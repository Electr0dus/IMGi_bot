import logging

from aiogram import types, Bot

from IMGi_bot import actions
from IMGi_bot import config
from IMGi_bot import getIMG
from IMGi_bot import keyboards
from IMGi_bot import text_answer
from IMGi_bot.DB import db_photo, db_user, db_set_img, db_rating, db_technikal

bot = Bot(config.BOT_TOKEN)


# Вывод клавиатуры с меню настройками генерации
async def menu_settings(message: types.Message):
    logging.info(f'Menu Settings: user {message.from_user.id}')
    await message.answer(text=text_answer.WELCOME_SETTINGS, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Вернуться обратно в главное меню
async def bact_to_main_menu(message: types.Message):
    logging.info(f'Bact to main menu: user {message.from_user.id}')
    await message.answer(text=text_answer.CANCEL_IMAGE_BOT, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)

# Выбор стиля генерации изображения
async def set_style(message: types.Message):
    logging.info(f'Setting the style: user {message.from_user.id}')
    with open('D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/function/image_for_settings/style.png', mode='rb') as file:
        await bot.send_photo(chat_id=message.from_user.id, photo=file, reply_markup=keyboards.kb_set_style)
    await message.answer(text=text_answer.SET_STYLE, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

# Вернуться обратно в выбор настройки генерации изображения
async def bact_settings(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(text=text_answer.WELCOME_SETTINGS, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Установка стиля "Стандартный"
async def set_DEFAULT(call: types.CallbackQuery):
    logging.info(f'SET STYLE "DEFAULT": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "DEFAULT")
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Установка стиля "Реалистичный"
async def set_UHD(call: types.CallbackQuery):
    logging.info(f'SET STYLE "UHD": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "UHD")
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Установка стиля "ANIME"
async def set_ANIME(call: types.CallbackQuery):
    logging.info(f'SET STYLE "ANIME": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "ANIME")
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Установка стиля "KANDINSKY"
async def set_KANDINSKY(call: types.CallbackQuery):
    logging.info(f'SET STYLE "KANDINSKY": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "KANDINSKY")
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)
