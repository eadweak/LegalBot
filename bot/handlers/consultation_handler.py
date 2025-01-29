from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from bot.handlers.main_handler import handle_consultation_registry
from bot.keyboards.main_menu import main_menu
from bot.utils.database import log_interaction
from aiogram import Dispatcher, Bot  # Добавлен импорт Bot

# Регистрация хендлеров
def register_handlers(dp: Dispatcher, bot: Bot):
    # Логика регистрации хендлеров
    dp.callback_query.register(handle_consultation_registry, lambda c: c.data == "consult_registry")