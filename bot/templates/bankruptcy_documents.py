# Шаблон заявления о банкротстве
BANKRUPTCY_APPLICATION_TEMPLATE = """
ИСКОВОЕ ЗАЯВЛЕНИЕ О БАНКРОТСТВЕ

В {court}
Истец: {fio}, проживающий по адресу: {address}.

Прошу признать меня банкротом в связи с невозможностью исполнения обязательств перед кредиторами.

Дата: {current_date}
Подпись: ___________
"""

# Шаблон списка имущества
PROPERTY_LIST_TEMPLATE = """
СПИСОК ИМУЩЕСТВА

1. Адрес: {address}
   Тип: {property_type}
   Площадь: {area} кв.м.
   Стоимость: {value} рублей.

2. Адрес: {second_address}
   Тип: {second_property_type}
   Площадь: {second_area} кв.м.
   Стоимость: {second_value} рублей.

Общий итог: {total_value} рублей.
"""

# Шаблон заявления о внесудебном банкротстве
OUT_OF_COURT_BANKRUPTCY_TEMPLATE = """
ЗАЯВЛЕНИЕ О ВНЕСУДЕБНОМ БАНКРОТСТВЕ

ФИО: {fio}
Адрес: {address}

Прошу признать меня банкротом во внесудебном порядке. 
Причина: {reason}

Список кредиторов:
{creditors}

Дата: {current_date}
Подпись: ___________
"""

# Шаблон списка кредиторов
CREDITORS_LIST_TEMPLATE = """
СПИСОК КРЕДИТОРОВ

1. Кредитор: {creditor_1}
   Сумма задолженности: {amount_1} рублей.

2. Кредитор: {creditor_2}
   Сумма задолженности: {amount_2} рублей.

Общая сумма задолженности: {total_amount} рублей.
"""

def generate_court_bankruptcy_application(data: dict) -> str:
    """
    Генерирует заявление о банкротстве на основе шаблона.
    :param data: Словарь с данными для заполнения шаблона.
    :return: Строка с заполненным документом.
    """
    return BANKRUPTCY_APPLICATION_TEMPLATE.format(**data)


def generate_property_list(data: dict) -> str:
    """
    Генерирует список имущества на основе шаблона.
    :param data: Словарь с данными для заполнения шаблона.
    :return: Строка с заполненным документом.
    """
    return PROPERTY_LIST_TEMPLATE.format(**data)


def generate_out_of_court_bankruptcy_application(data: dict) -> str:
    """
    Генерирует заявление о внесудебном банкротстве.
    :param data: Словарь с данными для заполнения шаблона.
    :return: Строка с заполненным документом.
    """
    return OUT_OF_COURT_BANKRUPTCY_TEMPLATE.format(**data)


def generate_creditors_list(data: dict) -> str:
    """
    Генерирует список кредиторов на основе шаблона.
    :param data: Словарь с данными для заполнения шаблона.
    :return: Строка с заполненным документом.
    """
    return CREDITORS_LIST_TEMPLATE.format(**data)
