def get_bankruptcy_steps(bankruptcy_type):
    if bankruptcy_type == "court":
        return (
            "Судебное банкротство: пошаговая инструкция\n\n"
            "1. **Проверка задолженности**:\n"
            "   - Минимальная сумма для судебного банкротства: 500 тысяч рублей.\n"
            "   - Отсутствие возможности погасить долг в течение 6 месяцев.\n\n"
            "2. **Сбор документов**:\n"
            "   - Паспорт.\n"
            "   - Справки о доходах за последние 3 года.\n"
            "   - Документы на имущество.\n"
            "   - Копия ИНН.\n"
            "   - Выписки по кредитам и займам.\n\n"
            "3. **Подача заявления в арбитражный суд**:\n"
            "   - Заполнение заявления о банкротстве.\n"
            "   - Прикрепление всех документов.\n"
            "   - Оплата госпошлины (300 рублей).\n\n"
            "4. **Судебное разбирательство**:\n"
            "   - Суд назначает финансового управляющего.\n"
            "   - Рассматриваются возможности реструктуризации долга или продажи имущества.\n\n"
            "5. **Завершение процедуры**:\n"
            "   - Суд списывает оставшуюся задолженность (при отсутствии нарушений).\n"
            "   - Завершается разбирательство."
        )
    elif bankruptcy_type == "out_of_court":
        return (
            "Внесудебное банкротство: пошаговая инструкция\n\n"
            "1. **Проверка задолженности**:\n"
            "   - Сумма долгов: от 50 до 500 тысяч рублей.\n"
            "   - Отсутствие имущества для погашения задолженности.\n"
            "   - Не менее 6 месяцев с момента последнего платежа.\n\n"
            "2. **Подготовка документов**:\n"
            "   - Паспорт.\n"
            "   - Копия ИНН.\n"
            "   - Справки о задолженности.\n"
            "   - Список кредиторов.\n\n"
            "3. **Подача заявления в МФЦ**:\n"
            "   - Подать заявление через ближайший центр \"Мои документы\".\n"
            "   - Передать полный пакет документов.\n\n"
            "4. **Рассмотрение заявления**:\n"
            "   - МФЦ проверяет корректность данных.\n"
            "   - Процедура длится около 6 месяцев.\n\n"
            "5. **Списание долгов**:\n"
            "   - После завершения проверки ваши долги будут списаны.\n"
            "   - Вы получите уведомление о завершении процедуры."
        )
