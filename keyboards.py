from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Клавиатура с основными кнопками
kb_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Генерация изображения👨‍🎨'), KeyboardButton(text='Настройки генерации⚙️'), ],
    [KeyboardButton(text='Просмотр изображения🖼'), KeyboardButton(text='Рейтинг изображений🥇')],
    [KeyboardButton(text='Оценить изображения🗳'), KeyboardButton(text='Сообщить об ошибке❌')],
    [KeyboardButton(text='Информация о ботеℹ️')],
], resize_keyboard=True)

# Клавиатура для выбора настройки генерации
kb_settings = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Стиль✨'), KeyboardButton(text='Негативный промт🚫')],
    [KeyboardButton(text='Размер изображения🔲'), KeyboardButton(text='Мои настройки🔧')],
    [KeyboardButton(text='Назад🔙')]
], resize_keyboard=True, one_time_keyboard=True)

# Клавиатура для работы со сгенерированной фотографией
kb_save_img = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить✅', callback_data='save'),
     InlineKeyboardButton(text='Отменить🚫', callback_data='cancel')],
    [InlineKeyboardButton(text='Сгенерировать заново🔁', callback_data='repeat')],
], resize_keyboard=True)

# Клавиатура для выбора стиля генерации
kb_set_style = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Стандартный', callback_data='DEFAULT'),
     InlineKeyboardButton(text='Реалистичный', callback_data='UHD')],
    [InlineKeyboardButton(text='Аниме', callback_data='ANIME'),
     InlineKeyboardButton(text='Кандинский', callback_data='KANDINSKY')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
], resize_keyboard=True)

# Клавиатура для выхода из настройки негативного промта
kb_cancel_np = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_np')]
], resize_keyboard=True)

# Клавиатура для выбора размера изображения при генерации которое будет
kb_set_size = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣6️⃣:9️⃣', callback_data='16:9'),
     InlineKeyboardButton(text='9️⃣:1️⃣6️⃣', callback_data='9:16')],
    [InlineKeyboardButton(text='3️⃣:2️⃣', callback_data='3:2'),
     InlineKeyboardButton(text='2️⃣:3️⃣', callback_data='2:3')],
    [InlineKeyboardButton(text='1️⃣:1️⃣', callback_data='1:1')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
], resize_keyboard=True)

# Клавиатура для выхода из выбора файла для просмотра
kb_cancel_sh = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_sh')]
], resize_keyboard=True)

# Клавиатура для уже открытого изображения
kb_open_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Скачать💾', callback_data='save_image_shown'),
     InlineKeyboardButton(text='Отмена🚫', callback_data='cancel_save_image')]
], resize_keyboard=True)

# Клавиатура для оценки изображения
kb_like_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Лайк👍', callback_data='like_image'),
     InlineKeyboardButton(text='Скачать💾', callback_data='save_like_image')],
    [InlineKeyboardButton(text='Далее➡️', callback_data='next_image'),
     InlineKeyboardButton(text='Выход🔙', callback_data='exit_main_menu')]
], resize_keyboard=True)

# Клавиатура для последнего выведенного изображения
kb_ending_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать заново♻️', callback_data='repeat_image_like'),
     InlineKeyboardButton(text='Выход🔙', callback_data='exit_main_menu')]
], resize_keyboard=True)

# Клавиатура выбора места изображения по рейтингу
kb_switch_rating = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🥇', callback_data='first_place')],
    [InlineKeyboardButton(text='🥈', callback_data='second_place')],
    [InlineKeyboardButton(text='🥉', callback_data='third_place')]
], resize_keyboard=True)

# Клавиатура для выхода из сообщение ошибки
kb_exit_error = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выход🔙', callback_data='exit_error')]
], resize_keyboard=True)
