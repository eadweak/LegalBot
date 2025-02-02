def get_document_template(template_id):
    """
    Возвращает документ по номеру шаблона.
    """
    templates = {
        1: "Договор аренды:\n\n[Ваш шаблон договора аренды]",
        2: "Исковое заявление:\n\n[Ваш шаблон искового заявления]",
    }
    return templates.get(template_id, "Шаблон не найден. Укажите корректный номер.")


def generate_document(template_name, data):
    """
    Генерирует документ на основе имени шаблона и переданных данных.
    """
    templates = {
        "divorce": (
            "ИСКОВОЕ ЗАЯВЛЕНИЕ О РАСТОРЖЕНИИ БРАКА\n\n"
            "В {court}\n"
            "Истец: {fio}, проживающий по адресу: {address}.\n"
            "Ответчик: {spouse}, проживающий по адресу: {spouse_address}.\n\n"
            "Прошу расторгнуть брак, зарегистрированный {date}, актовая запись № {record}.\n\n"
            "Дата: {current_date}\n"
            "Подпись: ___________"
        ),
        "alimony_agreement": (
            "СОГЛАШЕНИЕ ОБ УПЛАТЕ АЛИМЕНТОВ\n\n"
            "Мы, {fio}, проживающий по адресу: {address}, и {spouse}, проживающий по адресу: {spouse_address},\n"
            "заключили настоящее соглашение об уплате алиментов на содержание ребёнка {child_name}.\n\n"
            "Сумма алиментов: {alimony_amount} рублей ежемесячно.\n\n"
            "Дата: {current_date}\n"
            "Подписи сторон: ____________ / ____________"
        ),
    }

    # Проверка наличия шаблона
    if template_name not in templates:
        return "Шаблон не найден. Укажите корректное имя шаблона."

    # Форматирование и возврат готового документа
    return templates[template_name].format(**data)
