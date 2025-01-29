import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm import state
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import TOKEN
from bot.handlers import (
    consultation_handler,
    court_handler,
    subscription_handler,
    referral_handler,
    consultation_request_handler,
    service_request_handler,
    feedback_handler,
    faq_handler,
)
from bot.handlers import document_handler
from bot.handlers.about_handler import register_about_handlers
from bot.handlers.bankruptcy_handler import register_bankruptcy_handlers
from bot.handlers.court_lookup_handler import register_court_handlers
from bot.handlers.court_lookup_handler import router as court_router
from bot.handlers.document_handler import help_request, handle_help_request
from bot.handlers.feedback_handler import handle_feedback
from bot.handlers.legal_calculator_handler import register_legal_handlers, handle_receive_income
from bot.handlers.main_handler import register_handlers as register_main_handlers
from bot.handlers.service_request_handler import register_handlers as register_service_request_handlers
from bot.utils.court_parcer import parse_and_fill_database
from bot.utils.database import initialize_database
from bot.utils.database_utils import check_database, is_courts_table_empty
from bot.utils.database_utils import initialize_database
from handlers.document_handler import (
    handle_document, handle_download, handle_fill, handle_help, handle_back
)

# Инициализация бота, диспетчера и роутера
bot = Bot(token=TOKEN)
storage = MemoryStorage()  # FSM хранит данные в памяти
dp = Dispatcher(storage=storage)
router = Router()

# Инициализация базы данных
initialize_database()
check_database()
if is_courts_table_empty():
    parse_and_fill_database()

def register_document_handlers(dp):
    # Регистрация всех обработчиков для документов
    dp.callback_query.register(handle_document, lambda c: c.data.startswith("doc_"))
    dp.callback_query.register(handle_download, lambda c: c.data.endswith("_download"))
    dp.callback_query.register(handle_fill, lambda c: c.data.endswith("_fill"))
    dp.callback_query.register(handle_help, lambda c: c.data.endswith("_help"))
    dp.callback_query.register(handle_back, lambda c: c.data == "category_back")

    # Регистрируем обработчик для кнопки "Обратиться за помощью к специалисту"
    dp.callback_query.register(help_request, lambda c: c.data.endswith("_help"))

    # Обработка текстовых сообщений от пользователя фидбек
    dp.message.register(
        lambda message: handle_feedback(message, bot),
        # StateFilter(None)  # Обрабатываем все сообщения вне FSM
    )
    # Обработка текстовых сообщений от пользователя
    dp.message.register(
        lambda message: handle_help_request(message, bot),
         #StateFilter(None)  # Только вне FSM
    )

# Регистрация всех хендлеров
def register_all_handlers(dp: Dispatcher, bot: Bot):
    print("Регистрация всех обработчиков начата")

    # Подключаем основной роутер
    register_main_handlers(dp)
    dp.include_router(router)
    dp.include_router(court_router)
    register_bankruptcy_handlers(dp)
    register_about_handlers(dp)

    # Регистрация хендлеров FSM (приоритетные)
    court_handler.register_handlers(dp)
    register_legal_handlers(dp, state)

    # Регистрация специфических хендлеров (второй приоритет)
    subscription_handler.register_subscription_handlers(dp)
    referral_handler.register_handlers(dp)
    faq_handler.register_handlers(dp)
    document_handler.register_document_handlers(dp)
    register_document_handlers(dp)
    register_court_handlers(dp)

    # Регистрация общих текстовых хендлеров (последний приоритет)
    feedback_handler.register_feedback_handlers(dp, bot)
    consultation_handler.register_handlers(dp, bot)
    consultation_request_handler.register_handlers(dp, bot)
    register_service_request_handlers(dp, bot)
    service_request_handler.register_handlers(dp, bot)
    print("Регистрация всех обработчиков завершена")

# Основной блок запуска
async def main():
    initialize_database()

    # Удаляем вебхук (если используется) и регистрируем все хендлеры
    await bot.delete_webhook(drop_pending_updates=True)
    register_all_handlers(dp, bot)  # Регистрируем все хендлеры
    print("Бот запущен!")
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
