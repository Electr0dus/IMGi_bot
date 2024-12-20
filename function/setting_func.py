import logging

from aiogram import types, Bot

import actions
import config
import getIMG
import keyboards
import text_answer
from DB import db_photo, db_user, db_set_img, db_rating, db_technikal

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
    db_set_img.set_style_user(call.from_user.id, "DEFAULT", 'Стандартный')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Установка стиля "Реалистичный"
async def set_UHD(call: types.CallbackQuery):
    logging.info(f'SET STYLE "UHD": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "UHD", 'Реалистичный')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Установка стиля "ANIME"
async def set_ANIME(call: types.CallbackQuery):
    logging.info(f'SET STYLE "ANIME": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "ANIME", 'Аниме')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Установка стиля "KANDINSKY"
async def set_KANDINSKY(call: types.CallbackQuery):
    logging.info(f'SET STYLE "KANDINSKY": user {call.from_user.id}')
    db_set_img.set_style_user(call.from_user.id, "KANDINSKY", 'Кандинский')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Вызов установки негативного промта
async def call_negativ_prompt(message: types.Message):
    await message.answer(text=text_answer.NEGATIVE_PROMPT, parse_mode='HTML', reply_markup=keyboards.kb_cancel_np)
    await actions.NegativePromptAction.negative_prompt.set()

# Установка негативного промта
async def set_negative_prompt(message: types.Message, state):
    await state.update_data(negative=message.text)
    data = await state.get_data()
    logging.info(f'SET NEGATIVE PROMPT: user {message.from_user.id}')
    db_set_img.set_negative_prompt(message.from_user.id, data['negative'])
    await message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)
    await state.finish()

# Выход из настройки негативного промта
async def cancel_np(call: types.CallbackQuery, state):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=text_answer.WELCOME_SETTINGS, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Настройка размера изображения
async def switch_size_image(message: types.Message):
    for img in range(1, 6):
        with open(f'D:/Рабочий стол/Urban University/DIPLOM_project/IMGi_bot/function/image_for_settings/{img}.png', mode='rb') as photo:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo)
    await message.answer(text=text_answer.SET_SIZE, parse_mode='HTML', reply_markup=keyboards.kb_set_size)


# Установка формата 16:9
async def set_16by9(call: types.CallbackQuery):
    logging.info(f'SET SIZE "16:9": user {call.from_user.id}')
    db_set_img.set_size_image(call.from_user.id, 1024, 576, '16:9')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Установка формата 9:16
async def set_9by16(call: types.CallbackQuery):
    logging.info(f'SET SIZE "9:16": user {call.from_user.id}')
    db_set_img.set_size_image(call.from_user.id, 576, 1024, '9:16')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Установка формата 3:2
async def set_3by2(call: types.CallbackQuery):
    logging.info(f'SET SIZE "3:2": user {call.from_user.id}')
    db_set_img.set_size_image(call.from_user.id, 1024, 680, '3:2')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Установка формата 2:3
async def set_2by3(call: types.CallbackQuery):
    logging.info(f'SET SIZE "2:3": user {call.from_user.id}')
    db_set_img.set_size_image(call.from_user.id, 680, 1024, '2:3')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)

# Установка формата 1:1
async def set_1by1(call: types.CallbackQuery):
    logging.info(f'SET SIZE "1:1": user {call.from_user.id}')
    db_set_img.set_size_image(call.from_user.id, 1024, 1024, '1:1')
    await call.message.delete()
    await call.message.answer(text=text_answer.STYLE_SUSSCES, parse_mode='HTML', reply_markup=keyboards.kb_settings)


# Просмотр текущих настроек пользователя генерации изображения
async def current_settings_user(message: types.Message):
    data_settings = db_set_img.get_set_user(message.from_user.id)
    await message.answer(text=f'<b>Стиль:</b> <em>{data_settings[0][1]}</em>\n'
                              f'<b>Негативный промт:</b> <em>{data_settings[0][2]}</em>\n'
                              f'<b>Размер:</b> <em>{data_settings[0][5]}</em>\n',
                         parse_mode='HTML',
                         reply_markup=keyboards.kb_settings)
