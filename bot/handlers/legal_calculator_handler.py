from aiogram import types, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from bot.keyboards.legal_calculator_menu import legal_calculator_menu
from bot.utils.legal_calculator import LegalCalculator, AlimonyStates, PenaltyStates, CourtCostsStates
from bot.utils.database import log_interaction

router = Router()  # Создаем роутер для регистрации хендлеров

# Создаем экземпляр LegalCalculator
legal_calculator = LegalCalculator()

# Основной хендлер для юридического калькулятора
@router.message(Command("legal_calculator"))  # Используем фильтр Command
async def legal_calculator_menu_handler(message: types.Message):
    log_interaction(message.from_user.id, "legal_calculator_menu")
    await message.answer("Выберите расчёт:", reply_markup=legal_calculator_menu())

# Отправка результата с кнопкой "Вернуться в меню калькулятора"
async def send_result_with_menu(message: types.Message, result: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться в меню калькулятора", callback_data="back_to_calculator_menu")]
        ]
    )
    await message.answer(f"{result}\n\nВы можете вернуться в меню калькулятора:", reply_markup=keyboard)

# Расчёт алиментов - начало
@router.callback_query(lambda c: c.data == "calculate_alimony")
async def handle_calculate_alimony_callback(callback_query: types.CallbackQuery, state: FSMContext):
    log_interaction(callback_query.from_user.id, "calculate_alimony")
    await legal_calculator.start_alimony_conversation(callback_query, state)


# Расчёт алиментов - ввод дохода
@router.message(StateFilter(AlimonyStates.waiting_for_income))
async def handle_receive_income(update: types.Message, state: FSMContext):
    await legal_calculator.receive_income(update, state)

# Расчёт алиментов - ввод количества детей
@router.message(StateFilter(AlimonyStates.waiting_for_children))
async def handle_receive_children(update: types.Message, state: FSMContext):
    await legal_calculator.receive_children(update, state)

# Расчёт пени - начало
@router.callback_query(lambda c: c.data == "calculate_penalty")
async def handle_calculate_penalty_callback(callback_query: types.CallbackQuery, state: FSMContext):
    log_interaction(callback_query.from_user.id, "calculate_penalty")
    await legal_calculator.start_penalty_conversation(callback_query, state)

# Расчёт пени - ввод суммы долга
@router.callback_query(StateFilter(PenaltyStates.waiting_for_debt))
async def handle_receive_debt(callback_query: types.CallbackQuery, state: FSMContext):
    await legal_calculator.receive_debt(callback_query, state)

# Расчёт пени - ввод количества дней
@router.callback_query(StateFilter(PenaltyStates.waiting_for_days))
async def handle_receive_days(callback_query: types.CallbackQuery, state: FSMContext):
    await legal_calculator.receive_days(callback_query, state)

# Судебные издержки - начало
@router.callback_query(lambda c: c.data == "court_costs")
async def handle_court_costs_callback(callback_query: types.CallbackQuery, state: FSMContext):
    log_interaction(callback_query.from_user.id, "court_costs")
    await legal_calculator.start_court_costs_conversation(callback_query, state)

# Судебные издержки - ввод суммы иска
@router.message(StateFilter(CourtCostsStates.waiting_for_claim_amount))
async def handle_receive_claim_amount(message: types.Message, state: FSMContext):
    await legal_calculator.receive_claim_amount(message, state)

# Вернуться в меню калькулятора
@router.callback_query(lambda c: c.data == "back_to_calculator_menu")
async def back_to_calculator_menu(callback_query: types.CallbackQuery):
    await legal_calculator.start(callback_query, None)

# Вернуться в главное меню
@router.callback_query(lambda c: c.data == "main_menu")
async def handle_back_to_main_menu(callback_query: types.CallbackQuery):
    log_interaction(callback_query.from_user.id, "back_to_main_menu")
    await callback_query.message.edit_text("Возвращаемся в главное меню.")

# Регистрация хендлеров
def register_legal_handlers(dp, state):
    dp.include_router(router) # Подключаем роутер к диспетчеру