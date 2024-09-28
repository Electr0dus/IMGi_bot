from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Клавиатура с основными кнопками
kb_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Генерация изображения👨‍🎨'), KeyboardButton(text='Настройки генерации⚙️'),],
    [KeyboardButton(text='Просмотр изображения🖼'), KeyboardButton(text='Рейтинг изображений🥇')],
    [KeyboardButton(text='Оценить изображения🗳'), KeyboardButton(text='Сообщеть об ошибке❌')],
    [KeyboardButton(text='Информация о ботеℹ️')],
], resize_keyboard=True)

kb_save_img = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить✅', callback_data='save'),
     InlineKeyboardButton(text='Отменить🚫', callback_data='cancel')],
    [InlineKeyboardButton(text='Сгенерировать заново🔁', callback_data='repeat')],
], resize_keyboard=True, )
