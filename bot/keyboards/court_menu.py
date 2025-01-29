from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def court_menu():
    """
    Клавиатура для раздела "Поиск подсудности".
    """
    keyboard = [
        [InlineKeyboardButton(text="Ввести адрес", callback_data="enter_address")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)