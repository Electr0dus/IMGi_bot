from aiogram.dispatcher.filters.state import State, StatesGroup

# Машина состояния для регистрации пользователей
class RegisterAction(StatesGroup):
    username = State()


# Машина состония для ввода текста сгенерированой картинки
class GenerateAction(StatesGroup):
    prompt = State()
    file_name = State()