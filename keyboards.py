from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Генерация изображения👨‍🎨'), KeyboardButton(text='Настройки генерации⚙️'),],
    [KeyboardButton(text='Просмотр изображения🖼'), KeyboardButton(text='Рейтинг изображений🥇')],
    [KeyboardButton(text='Оценить изображения🗳'), KeyboardButton(text='Сообщеть об ошибке❌')],
    [KeyboardButton(text='Информация о ботеℹ️')],
], resize_keyboard=True)
