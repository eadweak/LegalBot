from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def legal_calculator_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton("Расчёт алиментов", callback_data="calculate_alimony"))
    menu.add(InlineKeyboardButton("Расчёт пени", callback_data="calculate_penalty"))
    menu.add(InlineKeyboardButton("Налоговый калькулятор", callback_data="tax_calculator"))
    menu.add(InlineKeyboardButton("Судебные издержки", callback_data="court_costs"))
    menu.add(InlineKeyboardButton("Назад в главное меню", callback_data="main_menu"))
    return menu
