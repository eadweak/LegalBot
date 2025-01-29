from aiogram.types import CallbackQuery
from aiogram import Dispatcher

async def about_us(callback: CallbackQuery):
    """
    Обработчик для кнопки "Информация о нас".
    """
    await callback.message.edit_text(
        "ИП Рыженко Е.В.\n"
        "Контакты:\n"
        "- Телефон: +7 (909) 014-79-33\n"
        "- Email: evruzhenko@icloud.com\n"
    )
    await callback.answer()  # Убираем "часики" Telegram

def register_about_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для раздела "О нас".
    """
    dp.callback_query.register(about_us, lambda c: c.data == "about")
