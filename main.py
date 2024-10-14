import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import actions
import config
from function import reg_func, setting_func, shown_func, like_func, raiting_func, error_func, about_func, admin_func
from DB import db_error, db_rating, db_photo, db_user, db_set_img, db_technikal, db_tech_image, db_check_like, db_admin

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
# Установить размер 1 на 1
dp.callback_query_handler(text='1:1')(setting_func.set_1by1)
#Получить текущие настройки бота
dp.message_handler(text=['Мои настройки🔧'])(setting_func.current_settings_user)
#Работа кнопки "Просмотр изображения"
dp.message_handler(text=['Просмотр изображения🖼'])(shown_func.all_image_user)
# Машина состояний просмотра изображения
dp.message_handler(state=actions.ShownImageActions.name_image)(shown_func.actions_shown_image)
# Выйти из просмотра всех файлов
dp.callback_query_handler(state=actions.ShownImageActions.name_image, text='cancel_sh')(shown_func.exit_sh_file)
# Выбрать другое изображение или выйти в основное меню
dp.callback_query_handler(text='cancel_save_image')(shown_func.cancel_current_image)
# Сохранение изображения на устройство
dp.callback_query_handler(text='save_image_shown')(shown_func.save_current_image)
# Оценить изображение
dp.message_handler(text=['Оценить изображения🗳'])(like_func.like_image)
# Выход в основное меню из оценки изображений
dp.callback_query_handler(text='exit_main_menu')(like_func.exit_to_main)
# Реализация пролистывания фотографий дальше
dp.callback_query_handler(text='next_image')(like_func.next_image_like)
# Реализовать повтор просмотр изображений
dp.callback_query_handler(text='repeat_image_like')(like_func.repeat_shown_image)
# Реализация лайка для изображения конкретным пользователем
dp.callback_query_handler(text='like_image')(like_func.send_like_image)
# Сохранить изображение при просмотре всех фотографий
dp.callback_query_handler(text='save_like_image')(like_func.save_like_image)
# Предоставления выбора места изображения
dp.message_handler(text=['Рейтинг изображений🥇'])(raiting_func.switch_rating_image)
# Показать изображения первого места
dp.callback_query_handler(text='first_place')(raiting_func.shown_first_place)
# Показать изображения второго места
dp.callback_query_handler(text='second_place')(raiting_func.shown_second_place)
# Показать изображения третьего места
dp.callback_query_handler(text='third_place')(raiting_func.shown_third_place)
# Добавить ошибку о боте пользователем
dp.message_handler(text=['Сообщить об ошибке❌'])(error_func.actions_error_user)
# Машина состояний для записи ошибки в БД
dp.message_handler(state=actions.ErrorActions.message_error)(error_func.write_error_user)
# Выйти из меню записи ошибки
dp.callback_query_handler(state=actions.ErrorActions.message_error, text='exit_error')(error_func.exit_to_main)
# Информация о боте
dp.message_handler(text=['Информация о ботеℹ️'])(about_func.about_info_bot)
# Вход в админ панель
dp.message_handler(commands=['admin'])(admin_func.connect_to_admin)
# Проверка пароля для входа в админ панель
dp.message_handler(state=actions.AdminPanelActions.input_pswd)(admin_func.check_password_actions)
# Выход из админ панели
dp.message_handler(text=['Выйти🔙'])(admin_func.exit_admin_panel)
# Добавить админа
dp.message_handler(text=['Добавить админа➕'])(admin_func.add_admin)
# Ввод пароля для админа
dp.message_handler(state=actions.AddAdminActions.id_user)(admin_func.input_pswd_to_admin)
# Завершение добавление админа
dp.message_handler(state=actions.AddAdminActions.pswd_admin)(admin_func.endind_add_admin)
# Удаление админа
dp.message_handler(text=['Удалить админа✖️'])(admin_func.delete_admin)
# Завершение удаление админа
dp.message_handler(state=actions.DeleteAdminActions.id_user)(admin_func.endind_delete_admin)
# Вывести список всех ошибок
dp.message_handler(text=['Просмотр ошибок🚫'])(admin_func.shown_error)
# Ответить на ошибку пользователя
dp.message_handler(text=['Ответить на ошибку📩'])(admin_func.answer_error)
# Отправить ID ошибки в машину состояний
dp.message_handler(state=actions.ErrorAnswerActions.id_error)(admin_func.id_error_for_delete)
# Отправить ответ пользователю об исправлении его ошибки
dp.message_handler(state=actions.ErrorAnswerActions.id_user)(admin_func.send_answer_user)


def main():
    db_user.create_db()  # Создание таблицы с пользователем
    db_set_img.create_db()  # Создание таблицы с настройками генерации фото
    db_photo.create_db()  # Создание таблицы с хранением сгенерированных фото
    db_rating.create_db()  # Создание таблицы с рейтингом фото
    db_error.create_db()  # Создание таблицы с ошибками, оставленными пользователями
    db_technikal.create_db()  # Создание таблицы с технической информацией для действий пользователя со генерированным изображением
    db_tech_image.create_db() # Создать таблицу с технической информацией для сохранения фото
    db_check_like.create_db() # Создать таблицу для проверки, какие изображения были уже лайкнуты
    db_admin.create_db() # Создать таблицу для админ панели
    logging.info('START BOT')
    executor.start_polling(dp, skip_updates=True)


# , on_startup=getIMG.generate_image

if __name__ == '__main__':
    main()
