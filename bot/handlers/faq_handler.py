from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.utils.database import log_interaction, save_consult_request  # Функция для сохранения
from bot.keyboards.faq_menu import faq_categories_menu, faq_questions_menu, consultation_button
from bot.utils.faq_data import FAQ

class ContactState(StatesGroup):
    waiting_for_contact = State()

# Главное меню FAQ
async def faq_menu(callback: CallbackQuery):
    """
    Обработчик главного меню FAQ.
    """
    log_interaction(callback.from_user.id, "faq_menu")
    await callback.message.edit_text("Выберите категорию:", reply_markup=faq_categories_menu())
    await callback.answer()


# Меню с вопросами выбранной категории
async def faq_category(callback: CallbackQuery):
    """
    Обработчик выбора категории FAQ.
    """
    category = callback.data
    if category in FAQ.keys():
        log_interaction(callback.from_user.id, f"faq_category: {category}")
        await callback.message.edit_text(f"Вопросы в категории '{category}':", reply_markup=faq_questions_menu(category))
    else:
        await callback.answer("Категория не найдена.", show_alert=True)


# Ответ на конкретный вопрос
async def faq_question(callback: CallbackQuery):
    """
    Обработчик выбора конкретного вопроса.
    """
    question_id = callback.data
    for category, items in FAQ.items():
        for item in items:
            if item["callback"] == question_id:
                log_interaction(callback.from_user.id, f"faq_question: {item['question']}")
                await callback.message.edit_text(
                    f"{item['question']}\n\n{item['answer']}",
                    reply_markup=consultation_button(item['callback'], category)  # Передаём category
                )
                return
    await callback.answer("Вопрос не найден.", show_alert=True)


async def handle_back_to_questions(callback: CallbackQuery):
    """
    Обработчик кнопки "Назад к вопросам".
    """
    # Извлекаем категорию из callback_data
    callback_data = callback.data  # Пример: "faq_questions_faq_tax"
    category = callback_data.replace("faq_questions_", "")  # Получаем "faq_tax"

    # Проверяем, существует ли такая категория
    try:
        await callback.message.edit_text(
            "Выберите вопрос:",
            reply_markup=faq_questions_menu(category)
        )
    except ValueError:
        await callback.answer("Категория не найдена.", show_alert=True)

async def handle_consult_request(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки "Записаться на консультацию с юристом".
    """
    article_id = callback.data.replace("consult_", "")
    print(f"Пользователь {callback.from_user.id} запросил консультацию по теме: {article_id}")

    # Сохраняем тему консультации в FSM
    await state.set_data({"article_id": article_id})
    await state.set_state(ContactState.waiting_for_contact)

    # Сообщение пользователю
    await callback.message.answer(
        f"Вы запросили консультацию по теме: {article_id}. Пожалуйста, отправьте ваши контактные данные (имя, телефон или email)."
    )
    await callback.answer()


async def process_contact(message: Message, state: FSMContext):
    """
    Обработчик для получения контактных данных от пользователя.
    """
    # Извлекаем данные из FSM
    user_data = await state.get_data()
    article_id = user_data.get("article_id")
    contact_info = message.text  # Контактные данные от пользователя

    # Сохраняем запрос в базу данных (если у вас есть функция save_consult_request)
    print(f"Сохранение данных: Пользователь {message.from_user.id}, Тема: {article_id}, Контакты: {contact_info}")

    # Уведомляем администратора
    admin_id = 1313342422  # Укажите ID администратора
    await message.bot.send_message(
        admin_id,
        f"Новый запрос на консультацию:\nПользователь: @{message.from_user.username} (ID: {message.from_user.id})\n"
        f"Тема: {article_id}\nКонтакты: {contact_info}"
    )

    # Завершаем FSM
    await state.clear()
    await message.answer("Ваши данные отправлены. С вами свяжутся в ближайшее время.")

# Регистрация хендлеров
def register_handlers(dp: Dispatcher):
    """
    Регистрация хендлеров для FAQ.
    """
    dp.callback_query.register(faq_menu, lambda callback: callback.data == "faq_categories")
    dp.callback_query.register(
        faq_category,
        lambda callback: callback.data in FAQ.keys()  # Проверяем, является ли callback категорией
    )
    dp.callback_query.register(
        faq_question,
        lambda callback: any(
            callback.data == item["callback"] for category in FAQ.values() for item in category
        )  # Проверяем, является ли callback вопросом
    )
    dp.callback_query.register(
        handle_back_to_questions,
        lambda callback: callback.data.startswith("faq_questions_")  # Проверяем, является ли это кнопка "Назад"
    )
    dp.callback_query.register(
        handle_consult_request,
        lambda callback: callback.data.startswith("consult_")  # Проверяем, является ли это кнопка "Записаться"
    )
    dp.message.register(process_contact, ContactState.waiting_for_contact)
