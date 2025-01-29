# Логика регистрации консультации
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

""" Выбор темы консультации """
def consultation_topics():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Семейное право", callback_data="topic_family")],
        [InlineKeyboardButton(text="Налоговые вопросы", callback_data="topic_tax")],
    ])
