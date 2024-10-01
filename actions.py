from aiogram.dispatcher.filters.state import State, StatesGroup

# Машина состояния для регистрации пользователей
class RegisterAction(StatesGroup):
    username = State()


# Машина состония для ввода текста сгенерированой картинки
class GenerateAction(StatesGroup):
    prompt = State()
    file_name = State()


# Машина состояния для ввода негативного промта
class NegativePromptAction(StatesGroup):
    negative_prompt = State()

# Машина состояния для получения имени файла изображения
class ShownImageActions(StatesGroup):
    name_image = State()