from multiprocessing.resource_tracker import register

from aiogram import Dispatcher, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

from bot.handlers.service_request_handler import service_request
from bot.handlers.consultation_request_handler import consultation_request
from bot.handlers.document_handler import handle_fill, handle_download, handle_help, handle_document
from bot.handlers.faq_handler import ContactState
from bot.handlers.subscription_handler import subscription_status, pay_subscription, successful_payment
from bot.keyboards.legal_calculator_menu import legal_calculator_menu
from bot.keyboards.main_menu import main_menu
from bot.keyboards.consultation_menu import consultation_menu, get_useful_articles_keyboard
from bot.keyboards.document_menu import document_categories_menu, document_list_menu
from bot.keyboards.court_menu import court_menu
from bot.keyboards.faq_menu import faq_categories_menu, faq_questions_menu
from bot.utils.faq_data import FAQ
from bot.keyboards.bankruptcy_menu import out_of_court_bankruptcy_menu, court_bankruptcy_menu, bankruptcy_menu
from bot.handlers.bankruptcy_handler import handle_out_of_court, handle_court
from bot.handlers.court_lookup_handler import court_guide_handler, start_find_court, process_address
from bot.handlers.court_lookup_handler import CourtLookupStates
from bot.handlers.about_handler import about_us
from bot.keyboards.subscription_menu import subscription_menu
from bot.utils.legal_calculator import LegalCalculator


# Состояния FSM
class UserState(StatesGroup):
    started = State()

# Главное меню
async def main_menu_handler(message: Message, state: FSMContext):
    await state.set_state(None)  # Сбрасываем состояние
    await message.answer("Добро пожаловать в главное меню:", reply_markup=main_menu())

# Обработчики главного меню
async def handle_consultations(callback: CallbackQuery, state: FSMContext):
    """
    Обработка нажатия на кнопку "Статьи".
    """
    await callback.message.edit_text("Вы выбрали: Статьи.", reply_markup=consultation_menu())
    await callback.answer()

async def handle_legal_calculator(callback: CallbackQuery, state: FSMContext):
    legal_calculator = LegalCalculator()
    await legal_calculator.start(callback, state)
    await callback.answer()

async def handle_jurisdiction(callback: CallbackQuery, state: FSMContext):
    """
    Обработка нажатия на кнопку "Поиск подсудности".
    """
    await callback.message.edit_text("Введите адрес для поиска подсудности.", reply_markup=court_menu())
    await callback.answer()

# Хендлер для кнопки "Составление документов"
async def handle_documents(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию документов:", reply_markup=document_categories_menu())
    await callback.answer()

# Хендлер для кнопки "Банкротство"
async def handle_bankruptcy(callback: CallbackQuery, state: FSMContext):
    """
    Обработка нажатия на кнопку "Банкротство".
    """
    await callback.message.edit_text("Вы выбрали: Банкротство.", reply_markup=bankruptcy_menu())
    await callback.answer()

async def handle_consultation_registry(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки "Записаться на консультацию с юристом".
    """
    if callback.data == "consult_registry":
        register_id = callback.data.replace("register_", "Консультация")
        print(f"Пользователь {callback.from_user.id} запросил консультацию по теме: {register_id}")

        # Сохраняем тему консультации в FSM
        await state.set_data({"register_id": register_id})
        await state.set_state(ContactState.waiting_for_contact)
        # Сообщение пользователю
        await callback.message.answer(
            f"Вы запросили консультацию у юриста. Пожалуйста, отправьте ваши контактные данные (имя, телефон или email)."
        )
        await callback.answer()


async def handle_consultation_menu(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки "Статьи" и переходов между уровнями меню FAQ.
    """
    if callback.data == "articles":
        await callback.message.edit_text("Выберите категорию юридических статей:", reply_markup=faq_categories_menu())
    elif callback.data in FAQ.keys():
        await callback.message.edit_text(
            f"Вы выбрали категорию: {callback.data.replace('_', ' ').capitalize()}\nВыберите вопрос:",
            reply_markup=faq_questions_menu(callback.data)
        )
    elif callback.data.startswith("faq_question_"):
        question_id = callback.data
        for category, items in FAQ.items():
            for item in items:
                if item["callback"] == question_id:
                    await callback.message.edit_text(
                        f"Вопрос: {item['question']}\n\nОтвет:\n{item['answer']}"
                    )
                    return
    elif callback.data == "main_menu":
        await callback.message.edit_text("Вы вернулись в главное меню.", reply_markup=main_menu())
    elif callback.data == "faq_categories":
        await callback.message.edit_text("Выберите категорию юридических статей:", reply_markup=faq_categories_menu())
    await callback.answer()

#Хендлер для работы с категориями и документами
async def handle_document_menu(callback: CallbackQuery):
    # Обработка выбора категории
    if callback.data.startswith("category_"):
        # Извлекаем ключ категории из callback_data
        category_key = callback.data.replace("category_", "")
        menu = document_list_menu(category_key)  # Генерация меню документов
        if menu:  # Проверяем, что меню успешно создано
            await callback.message.edit_text(
                "Выберите документ:", reply_markup=menu
            )
        else:
            await callback.message.answer("Меню для выбранной категории недоступно.")

    # Обработка выбора документа
    elif callback.data.startswith("doc_"):
        # Передача управления в функцию для отображения подменю действий
        await handle_document(callback)

    # Обработка кнопки "Назад"
    elif callback.data == "category_back":
        await callback.message.edit_text(
            "Выберите категорию документов:",
            reply_markup=document_categories_menu()
        )

    # Обработка ошибок
    else:
        await callback.message.answer("Произошла ошибка. Попробуйте снова.")

    # Завершаем обработку
    await callback.answer()

async def subscription_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=subscription_menu())
    await callback.answer()


async def handle_useful_articles(callback: CallbackQuery):
    """
    Обработчик для кнопки "Полезные статьи".
    """
    await callback.message.edit_text(
        "Выберите статью, которая вас интересует:",
        reply_markup=get_useful_articles_keyboard()
    )
    await callback.answer()  # Убираем "часики" Telegram

# Регистрация хендлеров
def register_handlers(dp: Dispatcher):
    print("Регистрация обработчиков из register_handlers начата")
    dp.message.register(main_menu_handler, Command("start"))
    dp.callback_query.register(handle_download, lambda c: c.data.endswith("_download"))
    dp.callback_query.register(handle_consultations, lambda c: c.data == "consultations")
    dp.callback_query.register(handle_legal_calculator, lambda c: c.data == "legal_calculator")
    dp.callback_query.register(handle_jurisdiction, lambda c: c.data == "jurisdiction")
    dp.callback_query.register(handle_documents, lambda c: c.data == "documents")
    dp.callback_query.register(handle_bankruptcy, lambda c: c.data == "bankruptcy")
    dp.callback_query.register(handle_out_of_court, lambda c: c.data == "bankruptcy_out_of_court")
    dp.callback_query.register(handle_court, lambda c: c.data == "bankruptcy_court")
    dp.callback_query.register(handle_consultation_registry, lambda c: c.data == "consult_registry")
    dp.callback_query.register(handle_consultation_menu, lambda c: c.data in ["articles", "main_menu"])

    # Хендлер для кнопки "Полезные статьи"
    dp.callback_query.register(handle_useful_articles, lambda c: c.data == "useful_articles")

    # Хендлеры для кнопок "Составление документов"
    dp.callback_query.register(handle_document_menu, lambda c: c.data.startswith("category_") or c.data.startswith(
        "doc_") or c.data == "category_back")
    dp.callback_query.register(handle_fill, lambda c: c.data.endswith("_fill"))
    dp.callback_query.register(handle_help, lambda c: c.data.endswith("_help"))
    dp.callback_query.register(handle_document, lambda c: c.data.startswith("doc_"))
    dp.message.register(service_request, Command("service_request"))

    # Обработчики для "Справочник судов РФ"
    dp.callback_query.register(court_guide_handler, lambda c: c.data == "court_guide")
    dp.callback_query.register(start_find_court, lambda c: c.data == "enter_address")
    dp.message.register(process_address, StateFilter(CourtLookupStates.waiting_for_address))

    # Обработчики для меню подписки
    dp.callback_query.register(subscription_menu_handler, lambda c: c.data == "manage_subscription")

    # Обработчики для кнопки узнать статус подписки
    dp.callback_query.register(subscription_status, lambda c: c.data == "subscription_status")

    # Обработчики для кнопки оплатить подписку
    dp.callback_query.register(pay_subscription, lambda c: c.data == "pay_subscription")
    dp.message.register(successful_payment, lambda message: message.successful_payment)

    print("Регистрация обработчиков из register_handlers завершена")