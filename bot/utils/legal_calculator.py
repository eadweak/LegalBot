from cgitb import handler

from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Определяем последовательность состояний для FSM
class AlimonyStates(StatesGroup):
    waiting_for_income = State()
    waiting_for_children = State()

class PenaltyStates(StatesGroup):
    waiting_for_debt = State()
    waiting_for_days = State()

class CourtCostsStates(StatesGroup):
    waiting_for_claim_amount = State()

class LegalCalculator:
    def __init__(self):
        pass

    async def start(self, update: CallbackQuery | Message, state: FSMContext):
        keyboard = [
            [InlineKeyboardButton(text="1. Расчёт алиментов", callback_data="calculate_alimony")],
            [InlineKeyboardButton(text="2. Расчёт пени", callback_data="calculate_penalty")],
            [InlineKeyboardButton(text="3. Налоговый калькулятор", callback_data="tax_calculator")],
            [InlineKeyboardButton(text="4. Судебные издержки", callback_data="court_costs")],
            [InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        if isinstance(update, CallbackQuery):
            await update.answer()
            await update.message.edit_text("Выберите опцию:", reply_markup=reply_markup)
        elif isinstance(update, Message):
            await update.answer("Выберите опцию:", reply_markup=reply_markup)

    async def handle_callback(self, update: CallbackQuery, state: FSMContext):
        query = update
        await query.answer()

        if query.data == "calculate_alimony":
            await self.start_alimony_conversation(query, state)
        elif query.data == "calculate_penalty":
            await self.start_penalty_conversation(query, state)
        elif query.data == "court_costs":
            await self.start_court_costs_conversation(query, state)

    # Алименты
    async def start_alimony_conversation(self, update: CallbackQuery, state: FSMContext):
        # Редактируем сообщение с кнопки и запрашиваем доход
        await update.message.edit_text("Введите ваш доход:")
        # Устанавливаем состояние ожидания дохода
        await state.set_state(AlimonyStates.waiting_for_income)
        print("Перешли в состояние AlimonyStates.waiting_for_income")

    async def receive_income(self, update: types.Message, state: FSMContext):
        try:
            income = float(update.text)
            await state.update_data(income=income)
            await update.answer("Введите количество детей:")
            await state.set_state(AlimonyStates.waiting_for_children)
        except ValueError:
            await update.answer("Пожалуйста, введите корректное число.")

    async def receive_children(self, update: types.Message, state: FSMContext):
        try:
            data = await state.get_data()
            income = data.get("income", 0)
            children = int(update.message.text)
            rate = 0.25 if children == 1 else 0.33 if children == 2 else 0.5
            alimony = income * rate
            await update.message.answer(f"Алименты составляют: {alimony:.2f} руб. (доход: {income}, дети: {children})")
            await state.clear()
        except ValueError:
            await update.message.answer("Пожалуйста, введите корректное число.")

    # Пеня
    async def start_penalty_conversation(self, update: CallbackQuery, state: FSMContext):
        await update.message.edit_text("Введите сумму долга:")
        await state.set_state(PenaltyStates.waiting_for_debt)

    async def receive_debt(self, update: Update, state: FSMContext):
        try:
            debt = float(update.text)
            await state.update_data(debt=debt)
            await update.answer("Введите количество дней просрочки:")
            await state.set_state(PenaltyStates.waiting_for_days)
        except ValueError:
            await update.answer("Пожалуйста, введите корректное число.")

    async def receive_days(self, update: Message, state: FSMContext):
        try:
            data = await state.get_data()
            debt = data.get("debt", 0)
            days = int(update.text)
            rate = 0.01
            penalty = debt * rate * days
            await update.answer(f"Сумма пени: {penalty:.2f} руб. (долг: {debt}, дни: {days})")
            await state.clear()
        except ValueError:
            await update.answer("Пожалуйста, введите корректное число.")

    # Судебные издержки
    async def start_court_costs_conversation(self, update: CallbackQuery, state: FSMContext):
        await update.message.edit_text("Введите сумму иска:")
        await state.set_state(CourtCostsStates.waiting_for_claim_amount)

    async def receive_claim_amount(self, update: Message, state: FSMContext):
        try:
            claim_amount = float(update.text)
            if claim_amount <= 100000:
                court_fee = claim_amount * 0.04
            elif claim_amount <= 200000:
                court_fee = 4000 + (claim_amount - 100000) * 0.03
            else:
                court_fee = 7000 + (claim_amount - 200000) * 0.02
            await update.answer(f"Судебные издержки: {court_fee:.2f} руб.")
            await state.clear()
        except ValueError:
            await update.answer("Пожалуйста, введите корректное число.")