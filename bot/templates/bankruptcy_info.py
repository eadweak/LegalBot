def get_bankruptcy_general_info(bankruptcy_type):
    if bankruptcy_type == "court":
        return (
            "Судебное банкротство:\n\n"
            "Процедура, проводимая через арбитражный суд. Позволяет списать долги, если сумма задолженности превышает 500 тысяч рублей."
        )
    elif bankruptcy_type == "out_of_court":
        return (
            "Внесудебное банкротство:\n\n"
            "Процедура банкротства, проводимая через МФЦ. Подходит для граждан с долгами от 50 до 500 тысяч рублей."
        )

def get_bankruptcy_procedure_info(bankruptcy_type):
    if bankruptcy_type == "court":
        return (
            "Процедура судебного банкротства:\n"
            "1. Сбор документов (паспорт, справки о долгах, доходах и имуществе).\n"
            "2. Подача заявления в арбитражный суд.\n"
            "3. Судебное разбирательство.\n"
            "4. Утверждение плана реструктуризации или продажа имущества."
        )
    elif bankruptcy_type == "out_of_court":
        return (
            "Процедура внесудебного банкротства:\n"
            "1. Подготовка заявления и списка долгов.\n"
            "2. Подача заявления в ближайший МФЦ.\n"
            "3. Рассмотрение заявления МФЦ.\n"
            "4. Списание долгов после завершения процедуры (обычно 6 месяцев)."
        )

def generate_court_bankruptcy_document(user_input):
    try:
        data = user_input.split("\n")
        fio = data[0]
        address = data[1]
        debt_amount = data[2]
        creditors = data[3:]

        document = (
            f"Заявление о признании банкротом (судебное)\n\n"
            f"Я, {fio}, проживающий по адресу: {address}, заявляю о признании меня банкротом через арбитражный суд. "
            f"Моя задолженность составляет {debt_amount} рублей.\n\n"
            f"Список кредиторов:\n" + "\n".join(creditors) +
            "\n\nПодписано: ____________________\nДата: ____________________"
        )
        return document
    except IndexError:
        raise ValueError("Неверный формат данных. Пожалуйста, отправьте все необходимые поля.")

def generate_out_of_court_bankruptcy_document(user_input):
    try:
        data = user_input.split("\n")
        fio = data[0]
        address = data[1]
        debt_amount = data[2]
        creditors = data[3:]

        document = (
            f"Заявление о признании банкротом (внесудебное)\n\n"
            f"Я, {fio}, проживающий по адресу: {address}, заявляю о признании меня банкротом через МФЦ. "
            f"Моя задолженность составляет {debt_amount} рублей.\n\n"
            f"Список кредиторов:\n" + "\n".join(creditors) +
            "\n\nПодписано: ____________________\nДата: ____________________"
        )
        return document
    except IndexError:
        raise ValueError("Неверный формат данных. Пожалуйста, отправьте все необходимые поля.")
