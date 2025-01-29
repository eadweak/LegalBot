from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def faq_categories_menu():
    """
    Клавиатура с категориями юридических статей.
    """
    keyboard = [
        [InlineKeyboardButton(text="Налоговое право", callback_data="faq_tax")],
        [InlineKeyboardButton(text="Субсидии и выплаты", callback_data="faq_subsidies")],
        [InlineKeyboardButton(text="Пенсии", callback_data="faq_pensions")],
        [InlineKeyboardButton(text="Кредиты", callback_data="faq_loans")],
        [InlineKeyboardButton(text="Трудовое право", callback_data="faq_labor")],
        [InlineKeyboardButton(text="Права потребителей", callback_data="faq_consumer")],
        [InlineKeyboardButton(text="Семейное право", callback_data="faq_family")],
        [InlineKeyboardButton(text="Назад в главное меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def faq_questions_menu(category):
    """
    Клавиатура с вопросами по выбранной категории.
    """
    faq_data = {
        "faq_tax": [
            {"question": "Какие налоговые льготы доступны?", "callback": "faq_tax_1"},
            {"question": "Как проверить задолженность по налогам?", "callback": "faq_tax_2"},
            {"question": "Что делать, если пришла неверная налоговая квитанция?", "callback": "faq_tax_3"},
            {"question": "Как получить налоговый вычет на квартиру?", "callback": "faq_tax_4"},
            {"question": "Как зарегистрироваться в качестве самозанятого?", "callback": "faq_tax_5"},
            {"question": "Какие штрафы за неуплату налогов?", "callback": "faq_tax_6"},
            {"question": "Можно ли оспорить налоговое решение?", "callback": "faq_tax_7"},
            {"question": "Какие налоги платят ИП?", "callback": "faq_tax_8"},
            {"question": "Как подать налоговую декларацию?", "callback": "faq_tax_9"},
            {"question": "Как получить справку об уплаченных налогах?", "callback": "faq_tax_10"},
        ],
        "faq_labor": [
            {"question": "Что делать, если не выплачивают зарплату?", "callback": "faq_labor_1"},
            {"question": "Могу ли я уволиться без отработки 2 недель?", "callback": "faq_labor_2"},
            {"question": "Как восстановиться на работе после незаконного увольнения?", "callback": "faq_labor_3"},
            {"question": "Какие выплаты положены при увольнении?", "callback": "faq_labor_4"},
            {"question": "Как подтвердить трудовой стаж без трудовой книжки?", "callback": "faq_labor_5"},
            {"question": "Можно ли уйти в отпуск раньше графика?", "callback": "faq_labor_6"},
            {"question": "Как правильно оформить удалённую работу?", "callback": "faq_labor_7"},
            {"question": "Могу ли я отказаться от командировки?", "callback": "faq_labor_8"},
            {"question": "Что делать, если вас заставляют работать сверхурочно?", "callback": "faq_labor_9"},
            {"question": "Как получить справку о доходах для кредита?", "callback": "faq_labor_10"},
        ],
        "faq_consumer": [
            {"question": "Что делать, если товар оказался некачественным?", "callback": "faq_consumer_1"},
            {"question": "Как вернуть товар в магазин?", "callback": "faq_consumer_2"},
            {"question": "Что делать, если магазин отказывается возвращать деньги?", "callback": "faq_consumer_3"},
            {"question": "Как проверить срок годности товара?", "callback": "faq_consumer_4"},
            {"question": "Можно ли вернуть бракованный товар без чека?", "callback": "faq_consumer_5"},
            {"question": "Как подать жалобу на продавца?", "callback": "faq_consumer_6"},
            {"question": "Что делать, если гарантийный ремонт затягивается?", "callback": "faq_consumer_7"},
            {"question": "Можно ли отказаться от услуги, если она выполнена некачественно?", "callback": "faq_consumer_8"},
            {"question": "Какие права у потребителя при покупке онлайн?", "callback": "faq_consumer_9"},
            {"question": "Что делать, если товар не доставили?", "callback": "faq_consumer_10"},
        ],
        "faq_loans": [
            {"question": "Как получить ипотечный кредит?", "callback": "faq_loans_1"},
            {"question": "Какие льготы по ипотеке доступны?", "callback": "faq_loans_2"},
            {"question": "Что делать, если не могу платить кредит?", "callback": "faq_loans_3"},
            {"question": "Как проверить свою кредитную историю?", "callback": "faq_loans_4"},
            {"question": "Какие документы нужны для автокредита?", "callback": "faq_loans_5"},
            {"question": "Как выбрать лучший кредит?", "callback": "faq_loans_6"},
            {"question": "Можно ли досрочно погасить кредит?", "callback": "faq_loans_7"},
            {"question": "Что делать, если банк подал в суд за кредит?",
             "callback": "faq_loans_8"},
            {"question": "Как узнать точный остаток по кредиту?", "callback": "faq_loans_9"},
            {"question": "Какие льготы доступны многодетным семьям по кредитам?", "callback": "faq_loans_10"},
        ],
        "faq_pensions": [
            {"question": "Как оформить пенсию по возрасту?", "callback": "faq_pensions_1"},
            {"question": "Какие льготы положены пенсионерам?", "callback": "faq_pensions_2"},
            {"question": "Как узнать размер своей пенсии?", "callback": "faq_pensions_3"},
            {"question": "Как оформить пенсию по инвалидности?", "callback": "faq_pensions_4"},
            {"question": "Какие документы нужны для пенсии?", "callback": "faq_pensions_5"},
            {"question": "Как получить дополнительную пенсию?", "callback": "faq_pensions_6"},
            {"question": "Можно ли оформить пенсию через Госуслуги?", "callback": "faq_pensions_7"},
            {"question": "Какие льготы для ветеранов труда?",
             "callback": "faq_pensions_8"},
            {"question": "Можно ли пересчитать пенсию?", "callback": "faq_pensions_9"},
            {"question": "Что делать, если задерживают пенсию?", "callback": "faq_pensions_10"},
        ],
        "faq_subsidies": [
            {"question": "Как оформить субсидию на жилье?", "callback": "faq_subsidies_1"},
            {"question": "Какие льготы положены многодетным семьям?", "callback": "faq_subsidies_2"},
            {"question": "Как получить компенсацию за коммунальные услуги?", "callback": "faq_subsidies_3"},
            {"question": "Какие субсидии доступны студентам?", "callback": "faq_subsidies_4"},
            {"question": "Как оформить пособие на ребенка?", "callback": "faq_subsidies_5"},
            {"question": "Можно ли получить льготы по инвалидности?", "callback": "faq_subsidies_6"},
            {"question": "Какие субсидии доступны для пенсионеров?", "callback": "faq_subsidies_7"},
            {"question": "Как получить помощь при потере работы?",
             "callback": "faq_subsidies_8"},
            {"question": "Что делать, если отказали в субсидии?", "callback": "faq_subsidies_9"},
            {"question": "Как узнать доступные льготы и выплаты?", "callback": "faq_subsidies_10"},
        ],
        "faq_family": [
            {"question": "Как подать заявление на развод?", "callback": "faq_family_1"},
            {"question": "Какие документы нужны для алиментов?", "callback": "faq_family_2"},
            {"question": "Как оформить опеку над ребёнком?", "callback": "faq_family_3"},
            {"question": "Как изменить фамилию ребёнка?", "callback": "faq_family_4"},
            {"question": "Как оспорить отцовство?", "callback": "faq_family_5"},
            {"question": "Можно ли выселить бывшего супруга из квартиры?", "callback": "faq_family_6"},
            {"question": "Как делится имущество при разводе?", "callback": "faq_family_7"},
            {"question": "Какие права имеет отец на ребёнка после развода?",
             "callback": "faq_family_8"},
            {"question": "Можно ли лишить родительских прав?", "callback": "faq_family_9"},
            {"question": "Что делать, если ребёнок отказывается жить с одним из родителей?", "callback": "faq_family_10"},
        ],
    }

    keyboard = []
    if category in faq_data:
        for item in faq_data[category]:
            keyboard.append([InlineKeyboardButton(text=item["question"], callback_data=item["callback"])])
    keyboard.append([InlineKeyboardButton(text="Назад к категориям", callback_data="faq_categories")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def consultation_button(article_id, category):
    """
    Клавиатура с кнопкой записи на консультацию.
    """
    # Создаем кнопки
    buttons = [
        [InlineKeyboardButton(text="Записаться на консультацию с юристом", callback_data=f"consult_{article_id}")],
        [InlineKeyboardButton(text="Назад к вопросам", callback_data=f"faq_questions_{category}")]
    ]
    # Передаем кнопки в InlineKeyboardMarkup
    return InlineKeyboardMarkup(inline_keyboard=buttons)
