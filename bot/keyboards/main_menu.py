from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    """
       Возвращает главное меню в виде InlineKeyboardMarkup.
       """
    keyboard = [
        [InlineKeyboardButton(text="Статьи", callback_data='consultations')],
        [InlineKeyboardButton(text="Юридический калькулятор", callback_data="legal_calculator")],
        [InlineKeyboardButton(text="Поиск подсудности", callback_data='jurisdiction')],
        [InlineKeyboardButton(text="Составление документов", callback_data='documents')],
        [InlineKeyboardButton(text="Банкротство (Практическое пособие)", callback_data='bankruptcy')],
        [InlineKeyboardButton(text="Оставить заявку на консультацию с юристом или заказать услугу", callback_data='consult_registry')],
        [InlineKeyboardButton(text="Справочник судов РФ", callback_data='court_guide')],
        [InlineKeyboardButton(text="Информация о нас", callback_data='about')],
        [InlineKeyboardButton(text="Жалобы и предложения", callback_data="feedback")],
        [InlineKeyboardButton(text="Управление подпиской", callback_data="subscriptions")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
