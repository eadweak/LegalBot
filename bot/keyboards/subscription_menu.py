from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscription_menu():
    """
    Клавиатура для управления подпиской.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Узнать статус моей подписки", callback_data="subscription_status")],
        [InlineKeyboardButton(text="Оплатить подписку", callback_data="pay_subscription")],
        [InlineKeyboardButton(text="Пригласить друга за подписку", callback_data="invite_friend")],
        [InlineKeyboardButton(text="Ввести лицензионный ключ подписки", callback_data="enter_license_key")],
        [InlineKeyboardButton(text="Купить лицензионный ключ подписки", callback_data="buy_license_key")],
    ])
    return keyboard

