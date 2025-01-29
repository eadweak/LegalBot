from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.court_menu import court_menu
from bot.utils.database import log_interaction


# Главное меню справочника судов
async def court_menu_handler(message: Message):
    """
    Обработчик для отображения меню "Поиск подсудности".
    """
    log_interaction(message.from_user.id, "court_menu")
    await message.answer("Выберите действие:", reply_markup=court_menu())


# Поиск судов по региону
async def handle_find_courts_by_region(message: Message):
    log_interaction(message.from_user.id, f"find_courts_by_region: {message.text}")
    await message.answer(f"Ищем суды в регионе: {message.text} (заглушка)")


# Поиск суда по адресу
async def handle_find_court_by_address(message: Message):
    log_interaction(message.from_user.id, f"find_court_by_address: {message.text}")
    await message.answer(f"Ищем суд по адресу: {message.text} (заглушка)")


# Регистрация хендлеров
def register_handlers(dp: Dispatcher):
    dp.message.register(court_menu_handler, Command("courts"))  # Команда /courts
    dp.message.register(
        handle_find_courts_by_region,
        lambda message: "Регион" in message.text  # Условие для фильтрации
    )
    dp.message.register(
        handle_find_court_by_address,
        lambda message: "Адрес" in message.text  # Условие для фильтрации

    )


