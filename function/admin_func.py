import logging

from aiogram import types, Bot

import actions
import config
import getIMG
import keyboards
import text_answer
from DB import db_error, db_admin, db_user

bot = Bot(config.BOT_TOKEN)

# Получить доступ к админ панели через команду /admin
async def connect_to_admin(message: types.Message):
    # db_admin.add_user_to_admin(message.from_user.id, 'qwerty1234')
    await message.answer(text=text_answer.ENTRY_ADMIN, parse_mode='HTML')
    await actions.AdminPanelActions.input_pswd.set()

# Проверка валидности введённого пароля
async def check_password_actions(message: types.Message, state):
    await state.update_data(pswd=message.text)
    data_pswd = await state.get_data()
    if db_admin.check_user_admin(message.from_user.id, data_pswd['pswd']) == 1:
        await message.answer(text=text_answer.NOT_ADMIN, parse_mode='HTML')
        await state.finish()
    elif db_admin.check_user_admin(message.from_user.id, data_pswd['pswd']) == 2:
        await message.answer(text=text_answer.ERROR_PSWD, parse_mode='HTML')
        await state.finish()
    elif db_admin.check_user_admin(message.from_user.id, data_pswd['pswd']) == 3:
        logging.info(f'User {message.from_user.id} enter to admin panel')
        await message.answer(text=text_answer.SUSSCES_ADMIN, parse_mode='HTML', reply_markup=keyboards.kb_admin_panel)
        await state.finish()
# Выход из админ панели
async def exit_admin_panel(message: types.Message):
    await message.answer(text=text_answer.CANCEL_IMAGE_BOT, parse_mode='HTML', reply_markup=keyboards.kb_main_menu)

# Добавить админа
async def add_admin(message: types.Message):
    # Вывести список с регистрацией чтобы видно было кого можно ввести
    data_user = db_user.get_all_user()
    list_of_user = ''
    for data in data_user:
        for text in data:
            list_of_user += str(text)
            list_of_user += ' '
        list_of_user += '\n'
    await message.answer(text=text_answer.ID_ADMIN, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=f'<em>{list_of_user}</em>', parse_mode='HTML')
    # Активировать состояние
    await actions.AddAdminActions.id_user.set()

# Ввод пароля для Admina
async def input_pswd_to_admin(message: types.Message, state):
    await state.update_data(id_user=message.text)
    await message.answer(text=text_answer.PSWD_ADMIN, parse_mode='HTML')
    # Установить состояние для ввода пароля
    await actions.AddAdminActions.pswd_admin.set()

# Завершение добавление админа в БД
async def endind_add_admin(message: types.Message, state):
    await state.update_data(pswd=message.text)
    data_admin = await state.get_data()
    db_admin.add_user_to_admin(data_admin['id_user'], data_admin['pswd'])
    logging.info(f"User {data_admin['id_user']} successfully add to admin panel")
    await message.answer(text=f"<b>Пользователь <em>{data_admin['id_user']}</em>"
                              f" успешно добавлен✅</b>", parse_mode='HTML', reply_markup=keyboards.kb_admin_panel)
    await state.finish()

# Вызов машины состояний для удаления админа из БД
async def delete_admin(message: types.Message):
    # Вывести список всех админов, чтобы видно было кого можно удалить
    data_user = db_admin.get_all_admin()
    list_of_user = ''
    for data in data_user:
        for text in data:
            list_of_user += str(text)
            list_of_user += ' '
        list_of_user += '\n'
    await message.answer(text=f'<em>{list_of_user}</em>', parse_mode='HTML')
    await message.answer(text=text_answer.ID_ADMIN, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    await actions.DeleteAdminActions.id_user.set()

# Удаление админа из БД
async def endind_delete_admin(message: types.Message, state):
    await state.update_data(id_user=message.text)
    data_id = await state.get_data()
    db_admin.delete_admin(data_id['id_user'])
    logging.info(f"User {data_id['id_user']} was deleted")
    await message.answer(text=f"<b>Пользователь <em>{data_id['id_user']}</em>"
                              f" успешно удалён✅</b>", parse_mode='HTML', reply_markup=keyboards.kb_admin_panel)
    await state.finish()


# Просмотр ошибок
async def shown_error(message: types.Message):
    # Вывести список всех ошибок
    data_error = db_error.get_all_error()
    list_of_error = ''
    for data in data_error:
        list_of_error += 'ID:'
        for text in data:
            list_of_error += str(text)
            list_of_error += ' '
        list_of_error += '\n'
    await message.answer(text=f'<em>{list_of_error}</em>', parse_mode='HTML')


# Ответить на ошибку пользователю
async def answer_error(message: types.Message):
    await message.answer(text=text_answer.INPUT_ID_ERROR, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    await actions.ErrorAnswerActions.id_error.set()


# Записать ID ошибки чтобы можно было её удалить из БД
async def id_error_for_delete(message: types.Message, state):
    await state.update_data(id_error=message.text)
    await message.answer(text=text_answer.INPUT_ID, parse_mode='HTML')
    await actions.ErrorAnswerActions.id_user.set()


# Отправить ответ на ошибку пользователю
async def send_answer_user(message: types.Message, state):
    await state.update_data(id_user=message.text)
    data_user = await state.get_data()
    db_error.delete_error(data_user['id_error'])
    logging.info(f"Anwser for error user {data_user['id_user']}")
    await bot.send_message(chat_id=data_user['id_user'],
                           text=text_answer.ANSWER_USER_ABOUT_ERROR,
                           parse_mode='HTML',
                           )
    await message.answer(text=f"<b>Ответ отправлен <em>{data_user['id_user']}</em></b>",
                         parse_mode='HTML',
                         reply_markup=keyboards.kb_admin_panel)
    await state.finish()
