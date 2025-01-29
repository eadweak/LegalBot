from aiogram.types import CallbackQuery, Message
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.court_menu import court_menu
from bot.utils.court_lookup import find_court_by_address
from aiogram import Dispatcher
from aiogram.filters import StateFilter

router = Router()

# Состояния
class CourtLookupStates(StatesGroup):
    waiting_for_address = State()

# Обработчик для отображения меню справочника судов
async def court_guide_handler(callback: CallbackQuery):
    """
    Обработчик для отображения главного меню справочника судов.
    """
    await callback.message.edit_text("Выберите действие:", reply_markup=court_menu())
    await callback.answer()

# Начало поиска суда
async def start_find_court(callback: CallbackQuery, state: FSMContext):
    """
    Начало поиска суда.
    """
    await callback.message.edit_text("Введите район, чтобы найти подсудный суд:")
    await state.set_state(CourtLookupStates.waiting_for_address)
    await callback.answer()

# Обработка введённого адреса
async def process_address(message: Message, state: FSMContext):
    """
    Обработка адреса и поиск суда.
    """
    address = message.text.strip()
    court = find_court_by_address(address)

    if court:
        response = (
            f"🏛 Найден суд:\n\n"
            f"Название: {court['name']}\n"
            f"Адрес: {court['address']}\n"
            f"📞 Телефон: {court['phone']}\n"
            f"✉️ Email: {court['email']}\n"
            f"🌐 Сайт: {court['url']}"
        )
    else:
        response = "⚠️ К сожалению, для данного адреса не найден соответствующий суд."

    await message.answer(response, reply_markup=court_menu())
    await state.clear()

def register_court_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для поиска суда по адресу.
    """
    dp.callback_query.register(court_guide_handler, lambda c: c.data == "court_guide")
    dp.callback_query.register(start_find_court, lambda c: c.data == "enter_address")
    dp.message.register(process_address, StateFilter(CourtLookupStates.waiting_for_address))


