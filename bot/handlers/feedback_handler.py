import os
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher, Bot
from aiogram.filters import StateFilter
from bot.config import ADMIN_USER_ID
from bot.utils.database import log_interaction


# Жалобы и предложения
async def feedback_request(callback: CallbackQuery):
    """
    Обработчик для кнопки "Жалобы и предложения".
    """
    log_interaction(callback.from_user.id, "feedback_request")
    await callback.message.edit_text(
        "Введите ваш отзыв, предложение или жалобу. Мы внимательно их рассмотрим:"
    )
    await callback.answer()


# Обработка данных отзыва
async def handle_feedback(message: Message, bot: Bot):
    """
    Обработка текстовых сообщений.
    """
    print(f"Обработчик вызван для сообщения: {message.text}")  # Отладка
    log_interaction(message.from_user.id, f"feedback_data: {message.text}")
    print("Проверяем что таблица существует")
    # Убедимся, что директория существует
    import os
    os.makedirs("1bot/db", exist_ok=True)
    print("Сохраняем отзыв в файл")
    # Сохраняем отзыв в файл
    with open("1bot/db/feedbacks.txt", "a", encoding="utf-8") as file:
        file.write(f"{message.from_user.id}: {message.text}\n")
    print("Направляем уведомление администратору")
    # Уведомляем администратора
    await bot.send_message(
        ADMIN_USER_ID,
        f"Новое сообщение от пользователя:\n\n"
        f"Пользователь: {message.from_user.full_name}\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )
    await message.answer("Спасибо за ваш отзыв! Мы его рассмотрим.")

# Регистрация хендлеров
def register_feedback_handlers(dp: Dispatcher, bot: Bot):
    print("Регистрация обработчиков для жалоб и предложений начата")

    # Обработчик кнопки
    dp.callback_query.register(feedback_request, lambda c: c.data == "feedback")

    # Обработчик текстовых сообщений
    dp.message.register(
        lambda message: handle_feedback(message, bot),
        StateFilter(None)  # Обрабатываем все сообщения вне FSM
    )

    print("Регистрация обработчиков для жалоб и предложений завершена")


