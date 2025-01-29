import os
from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from bot.config import ADMIN_USER_ID
from bot.utils.database import log_interaction


# Заявка на консультацию
async def consultation_request(message: Message):
    log_interaction(message.from_user.id, "consultation_request")
    await message.answer("Введите ваше имя, контактные данные и краткое описание вопроса:")


# Обработка данных заявки
async def handle_consultation_request(message: Message, bot: Bot, state: FSMContext):
    log_interaction(message.from_user.id, f"consultation_request_data: {message.text}")
    # Проверяем, что нет активного состояния
    if await state.get_state() is not None:
        return  # Игнорируем сообщение, если пользователь находится в процессе другого диалога

    # Проверяем наличие директории и файла
    directory = "/db"
    os.makedirs(directory, exist_ok=True)  # Создаём директорию, если её нет
    file_path = os.path.join(directory, "consult_requests.csv")

    if not os.path.exists(file_path):  # Если файл отсутствует, создаём его
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("user_id,request\n")  # Добавляем заголовки столбцов

    # Сохраняем заявку в файл
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{message.from_user.id},{message.text}\n")

    # Отправляем уведомление администратору
    await bot.send_message(
        ADMIN_USER_ID,
        f"Новая заявка на консультацию:\n\n"
        f"Пользователь: {message.from_user.full_name}\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    await message.answer("Спасибо! Ваша заявка успешно отправлена. Юрист свяжется с вами в ближайшее время.")


# Регистрация хендлеров
def register_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(consultation_request, Command("consultation_request"))

    async def process_consultation_request(msg: Message, state: FSMContext):
        await handle_consultation_request(msg, bot, state)

    dp.message.register(
        process_consultation_request,
        lambda message: True,  # Обрабатываем сообщения
        StateFilter(None)  # Только при отсутствии активного состояния
    )
