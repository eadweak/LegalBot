from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from bot.keyboards.bankruptcy_menu import (
    bankruptcy_menu,
    out_of_court_bankruptcy_menu,
    court_bankruptcy_menu
)
from bot.utils.bankruptcy_texts import (
    get_out_of_court_steps_text,
    get_out_of_court_docs_text,
    get_out_of_court_requirements_text,
    get_out_of_court_consequences_text,
    get_out_of_court_cancellation_text,
    get_out_of_court_avoidance_text,
    get_out_of_court_faq_text,
)
from bot.utils.bankruptcy_texts import (
    get_court_steps_text,
    get_court_docs_text,
    get_court_requirements_text,
    get_court_consequences_text,
    get_court_cancellation_text,
    get_court_avoidance_text,
    get_court_faq_text,
)



async def handle_back_to_bankruptcy_menu(callback: CallbackQuery):
    """
    Обработчик для кнопки "Назад" в разделе банкротства.
    """
    await callback.message.edit_text(
        "Вы вернулись в главное меню раздела 'Банкротство'.",
        reply_markup=bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_steps(callback: CallbackQuery):
    """
    Обработчик для кнопки "Пошаговое описание".
    """
    await callback.message.edit_text(
        get_court_steps_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_docs(callback: CallbackQuery):
    """
    Обработчик для кнопки "Список необходимых документов".
    """
    await callback.message.edit_text(
        get_court_docs_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_requirements(callback: CallbackQuery):
    """
    Обработчик для кнопки "Требования к должнику".
    """
    await callback.message.edit_text(
        get_court_requirements_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_consequences(callback: CallbackQuery):
    """
    Обработчик для кнопки "Последствия банкротства".
    """
    await callback.message.edit_text(
        get_court_consequences_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_cancellation(callback: CallbackQuery):
    """
    Обработчик для кнопки "Можно ли остановить/отменить процедуру".
    """
    await callback.message.edit_text(
        get_court_cancellation_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_avoidance(callback: CallbackQuery):
    """
    Обработчик для кнопки "Как избежать банкротства".
    """
    await callback.message.edit_text(
        get_court_avoidance_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court_faq(callback: CallbackQuery):
    """
    Обработчик для кнопки "Часто задаваемые вопросы".
    """
    await callback.message.edit_text(
        get_court_faq_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()


async def handle_out_of_court_consequences(callback: CallbackQuery):
    """
    Обработчик для кнопки "Последствия банкротства".
    """
    await callback.message.edit_text(
        get_out_of_court_consequences_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_out_of_court_cancellation(callback: CallbackQuery):
    """
    Обработчик для кнопки "Можно ли остановить/отменить процедуру".
    """
    await callback.message.edit_text(
        get_out_of_court_cancellation_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_out_of_court_avoidance(callback: CallbackQuery):
    """
    Обработчик для кнопки "Как избежать банкротства".
    """
    await callback.message.edit_text(
        get_out_of_court_avoidance_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_out_of_court_faq(callback: CallbackQuery):
    """
    Обработчик для кнопки "Часто задаваемые вопросы".
    """
    await callback.message.edit_text(
        get_out_of_court_faq_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

# Хендлер для Пошаговой процедуры внесудебного банкротства
async def handle_out_of_court_steps(callback: CallbackQuery):
    await callback.message.edit_text(
        text=get_out_of_court_steps_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

# Хендлер для "Необходимых документов для внесудебного банкротства"
async def handle_out_of_court_docs(callback: CallbackQuery):
    await callback.message.edit_text(
        text=get_out_of_court_docs_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

# Хендлер для "Требований к должнику для внесудебного банкротства"
async def handle_out_of_court_requirements(callback: CallbackQuery):
    await callback.message.edit_text(
        text=get_out_of_court_requirements_text(),
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

# Хендлер для "Пошаговой процедуры судебного банкротства"
async def handle_court_steps(callback: CallbackQuery):
    await callback.message.edit_text(
        text=get_court_steps_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

# Хендлер для "Необходимых документов для судебного банкротства"
async def handle_court_docs(callback: CallbackQuery):
    await callback.message.edit_text(
        text=get_court_docs_text(),
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_out_of_court(callback: CallbackQuery):
    print(f"handle_out_of_court вызван. Callback data: {callback.data}")
    await callback.message.edit_text(
        "Вы выбрали раздел 'Внесудебное банкротство'.",
        reply_markup=out_of_court_bankruptcy_menu()
    )
    await callback.answer()

async def handle_court(callback: CallbackQuery):
    print(f"handle_court вызван. Callback data: {callback.data}")
    await callback.message.edit_text(
        "Вы выбрали раздел 'Судебное банкротство'.",
        reply_markup=court_bankruptcy_menu()
    )
    await callback.answer()

# Регистрация хендлеров
def register_bankruptcy_handlers(dp: Dispatcher):
    print("Регистрация обработчиков банкротства начата")
    dp.callback_query.register(handle_out_of_court, lambda c: c.data == "bankruptcy_out_of_court")
    dp.callback_query.register(handle_court, lambda c: c.data == "bankruptcy_court")
    dp.callback_query.register(handle_out_of_court_steps, lambda c: c.data == "out_of_court_steps")
    dp.callback_query.register(handle_out_of_court_docs, lambda c: c.data == "out_of_court_docs")
    dp.callback_query.register(handle_out_of_court_requirements, lambda c: c.data == "out_of_court_requirements")
    dp.callback_query.register(handle_out_of_court_consequences, lambda c: c.data == "out_of_court_consequences")
    dp.callback_query.register(handle_out_of_court_cancellation, lambda c: c.data == "out_of_court_cancellation")
    dp.callback_query.register(handle_out_of_court_avoidance, lambda c: c.data == "out_of_court_avoidance")
    dp.callback_query.register(handle_out_of_court_faq, lambda c: c.data == "out_of_court_faq")
    dp.callback_query.register(handle_court_steps, lambda c: c.data == "court_steps")
    dp.callback_query.register(handle_court_docs, lambda c: c.data == "court_docs")
    dp.callback_query.register(handle_court_requirements, lambda c: c.data == "court_requirements")
    dp.callback_query.register(handle_court_consequences, lambda c: c.data == "court_consequences")
    dp.callback_query.register(handle_court_cancellation, lambda c: c.data == "court_cancellation")
    dp.callback_query.register(handle_court_avoidance, lambda c: c.data == "court_avoidance")
    dp.callback_query.register(handle_court_faq, lambda c: c.data == "court_faq")
    print("Регистрация обработчиков банкротства завершена")


