from aiogram.dispatcher.filters.state import State, StatesGroup

# Машина состояния для регистрации пользователей
class RegisterAction(StatesGroup):
    username = State()