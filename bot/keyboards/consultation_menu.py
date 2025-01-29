from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types


def consultation_menu():
    """
    Клавиатура для раздела "Статьи".
    """
    keyboard = [
        [InlineKeyboardButton(text="FAQ", callback_data="articles")],
        [InlineKeyboardButton(text="Полезные статьи", callback_data="useful_articles")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_useful_articles_keyboard():
    """
    Возвращает клавиатуру с полезными статьями.
    """
    # Создаем список кнопок
    buttons = [
        [
            InlineKeyboardButton(
                text="Какие субсидии доступны семьям с детьми и как их оформить?",
                url="https://teletype.in/@legalbot/0_MeMbpTQ1P"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как сэкономить на коммунальных платежах: пути получения льгот и субсидий",
                url="https://teletype.in/@legalbot/kmXUU8CDD25"
            )
        ],
        [
            InlineKeyboardButton(
                text="Защита прав потребителя при покупке техники: как вернуть и обменять товар?",
                url="https://teletype.in/@legalbot/DVlxVwS8A9_"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как отказаться от навязанной страховки при оформлении кредита?",
                url="https://teletype.in/@legalbot/8VFjdfD-mlW"
            )
        ],
        [
            InlineKeyboardButton(
                text="Долги по ЖКХ: как договориться о реструктуризации и не попасть под суд?",
                url="https://teletype.in/@legalbot/ICE1ZR7CMgE"
            )
        ],
        [
            InlineKeyboardButton(
                text="Выбор выгодного кредита: как сравнить условия и не переплатить банку",
                url="https://teletype.in/@legalbot/nHwYY89CQyc"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как вернуть незаконно списанные банком комиссии и страховки?",
                url="https://teletype.in/@legalbot/i_wNV8ALGN7"
            )
        ],
        [
            InlineKeyboardButton(
                text="ЗРаздел имущества при разводе: как не остаться в долгах и защитить свои права?",
                url="https://teletype.in/@legalbot/T9IKviF6hjo"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как потребовать возмещение ущерба при оказании некачественных услуг?",
                url="https://teletype.in/@legalbot/MNnQV5mOenG"
            )
        ],
        [
            InlineKeyboardButton(
                text="Коммунальные споры: что делать, если управляющая компания не выполняет обязанности?",
                url="https://teletype.in/@legalbot/5edUsc-M_mM"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как использовать материнский капитал для улучшения жилищных условий?",
                url="https://teletype.in/@legalbot/nR2CYlKmmnI"
            )
        ],
        [
            InlineKeyboardButton(
                text="Какие есть льготы для пенсионеров и как не упустить право на них?",
                url="https://teletype.in/@legalbot/CXT2IQGM-V7"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как защищать свои права при онлайн-покупках и доставках?",
                url="https://teletype.in/@legalbot/_vYUcj3gShB"
            )
        ],
        [
            InlineKeyboardButton(
                text="Банковская карта и безопасность: как защитить средства от списаний и мошенников?",
                url="https://teletype.in/@legalbot/L22FDZO_-Fg"
            )
        ],
        [
            InlineKeyboardButton(
                text="Что делать, если коллекторы угрожают: законные способы защиты",
                url="https://teletype.in/@legalbot/uEYkWEpC4Lz"
            )
        ],
        [
            InlineKeyboardButton(
                text="Льготы и компенсации по налогам: как вернуть часть расходов на лечение, учёбу и жильё",
                url="https://teletype.in/@legalbot/Wve-m9q7O6V"
            )
        ],
        [
            InlineKeyboardButton(
                text="Защита прав потребителя при покупке техники: как вернуть и обменять товар?",
                url="https://teletype.in/@legalbot/DVlxVwS8A9_"
            )
        ],
        [
            InlineKeyboardButton(
                text="Как снизить ежемесячный платёж по ипотеке или рефинансировать её на выгодных условиях",
                url="https://teletype.in/@legalbot/IQth6XETATD"
            )
        ],
        [
            InlineKeyboardButton(
                text="Защита прав потребителя при покупке техники: как вернуть и обменять товар?",
                url="https://teletype.in/@legalbot/DVlxVwS8A9_"
            )
        ],
        [
            InlineKeyboardButton(
                text="Взыскание алиментов: как правильно составить иск и какие документы подготовить?",
                url="https://teletype.in/@legalbot/leC4aUP-TnX"
            )
        ],
        [
            InlineKeyboardButton(
                text="Рассрочка в магазине: как понять, что это не скрытый кредит?",
                url="https://teletype.in/@legalbot/CG0KJRmcRa1"
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
    ]

    # Передаём кнопки в InlineKeyboardMarkup
    return InlineKeyboardMarkup(inline_keyboard=buttons)


