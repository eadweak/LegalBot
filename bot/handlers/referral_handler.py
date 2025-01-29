from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.database import register_user, generate_referral_code, log_interaction


# Хендлер для команды /start с реферальной системой
async def referral_start(message: Message):
    args = message.text.split(maxsplit=1)
    referral_code = args[1] if len(args) > 1 else None  # Получаем реферальный код из аргументов команды /start
    register_user(message.from_user.id, message.from_user.full_name, referral_code)
    user_referral_code = generate_referral_code(message.from_user.id)
    log_interaction(message.from_user.id, f"referral_used: {referral_code}")
    await message.answer(f"Вы успешно зарегистрированы! Ваш реферальный код: {user_referral_code}")


# Регистрация хендлеров
def register_handlers(dp: Dispatcher):
    dp.message.register(referral_start, Command("start"))  # Обработка команды /start
