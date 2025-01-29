from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def bankruptcy_menu():
    """
    Главное меню раздела "Банкротство".
    """
    keyboard = [
        [InlineKeyboardButton(text="Внесудебное банкротство (упрощенная процедура)", callback_data="bankruptcy_out_of_court")],
        [InlineKeyboardButton(text="Судебное банкротство (полная процедура)", callback_data="bankruptcy_court")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def out_of_court_bankruptcy_menu():
    """
    Меню для раздела "Внесудебное банкротство".
    """
    keyboard = [
        [InlineKeyboardButton(text="Пошаговое описание", callback_data="out_of_court_steps")],
        [InlineKeyboardButton(text="Список необходимых документов", callback_data="out_of_court_docs")],
        [InlineKeyboardButton(text="Требования к должнику", callback_data="out_of_court_requirements")],
        [InlineKeyboardButton(text="Последствия банкротства", callback_data="out_of_court_consequences")],
        [InlineKeyboardButton(text="Можно ли остановить/отменить процедуру", callback_data="out_of_court_cancellation")],
        [InlineKeyboardButton(text="Как избежать банкротства", callback_data="out_of_court_avoidance")],
        [InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data="out_of_court_faq")],
        [InlineKeyboardButton(text="Назад", callback_data="bankruptcy")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def court_bankruptcy_menu():
    """
    Меню для раздела "Судебное банкротство".
    """
    keyboard = [
        [InlineKeyboardButton(text="Пошаговое описание", callback_data="court_steps")],
        [InlineKeyboardButton(text="Список необходимых документов", callback_data="court_docs")],
        [InlineKeyboardButton(text="Требования к должнику", callback_data="court_requirements")],
        [InlineKeyboardButton(text="Последствия банкротства", callback_data="court_consequences")],
        [InlineKeyboardButton(text="Можно ли остановить/отменить процедуру", callback_data="court_cancellation")],
        [InlineKeyboardButton(text="Как избежать банкротства", callback_data="court_avoidance")],
        [InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data="court_faq")],
        [InlineKeyboardButton(text="Назад", callback_data="bankruptcy")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


