from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CATEGORY_MAPPING = {
    "family": "Семейное право",
    "subsidies": "Субсидии и выплаты",
    "pension": "Пенсионное право",
    "loans": "Кредиты и услуги при кредитах",
    "employment": "Трудовое право",
    "inheritance": "Наследственное право",
    "housing": "Жилищное право",
    "administrative": "Административное право",
    "consumer": "Защита прав потребителей",
    "tax": "Налоговое право",
}

def document_categories_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Семейное право", callback_data="category_family")],
            [InlineKeyboardButton(text="Субсидии и выплаты", callback_data="category_subsidies")],
            [InlineKeyboardButton(text="Пенсионное право", callback_data="category_pension")],
            [InlineKeyboardButton(text="Кредиты и услуги при кредитах", callback_data="category_loans")],
            [InlineKeyboardButton(text="Трудовое право", callback_data="category_employment")],
            [InlineKeyboardButton(text="Наследственное право", callback_data="category_inheritance")],
            [InlineKeyboardButton(text="Жилищное право", callback_data="category_housing")],
            [InlineKeyboardButton(text="Административное право", callback_data="category_administrative")],
            [InlineKeyboardButton(text="Защита прав потребителей", callback_data="category_consumer")],
            [InlineKeyboardButton(text="Налоговое право", callback_data="category_tax")],
            [InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu")],
            ]
    )


def document_list_menu(category):
    if category == "family":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Брачный договор" , callback_data="doc_marriage")],
                [InlineKeyboardButton(text="Заявление о расторжении брака", callback_data="doc_divorce")],
                [InlineKeyboardButton(text="Исковое заявление на алименты", callback_data="doc_alimony_claim")],
                [InlineKeyboardButton(text="Соглашение об алиментах", callback_data="doc_alimony_agreement")],
                [InlineKeyboardButton(text="Определение места жительства ребенка", callback_data="doc_child_residence")],
                [InlineKeyboardButton(text="Заявление об установлении отцовства", callback_data="doc_fatherhood")],
                [InlineKeyboardButton(text="Заявление об отказе от родительских прав", callback_data="doc_parental_rights")],
                [InlineKeyboardButton(text="Иск о лишении родительских прав", callback_data="doc_parental_rights_claim")],
                [InlineKeyboardButton(text="Признание брака недействительным", callback_data="doc_annul_marriage")],
                [InlineKeyboardButton(text="Соглашение об общении с ребенком", callback_data="doc_communication_child")],
                [InlineKeyboardButton(text="Иск об уменьшении алиментов", callback_data="doc_reduce_alimony")],
                [InlineKeyboardButton(text="Соглашение о разделе имущества", callback_data="doc_property_division")],
                [InlineKeyboardButton(text="Соглашение о содержании детей", callback_data="doc_children_agreement")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    elif category == "subsidies":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Заявление на субсидию по ЖКУ", callback_data="doc_subsidy_request")],
                [InlineKeyboardButton(text="Жалоба на задержку выплаты по субсидии", callback_data="doc_subsidy_complaint")],
                [InlineKeyboardButton(text="Образец искового заявления на отказ в субсидии", callback_data="doc_subsidy_denial_complaint")],
                [InlineKeyboardButton(text="Заявление на продление выплат ежемесячного пособия на детей", callback_data="doc_payment_extension")],
                [InlineKeyboardButton(text="Запрос на информацию по субсидии", callback_data="doc_subsidy_info_request")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    elif category == "pension":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Запрос о назначении пенсии", callback_data="doc_pension_request")],
                [InlineKeyboardButton(text="Жалоба в ПФР", callback_data="doc_pfr_complaint")],
                [InlineKeyboardButton(text="Заявление о перерасчёте пенсии", callback_data="doc_pension_recalculation")],
                [InlineKeyboardButton(text="Заявление о выплате начисленных сумм пенсии", callback_data="doc_pension_missing_claim")],
                [InlineKeyboardButton(text="Жалоба на отказ в пенсии", callback_data="doc_pension_denial_complaint")],
                [InlineKeyboardButton(text="Заявление на восстановление пенсии", callback_data="doc_pension_restoration")],
                [InlineKeyboardButton(text="Перевод пенсии в другой регион", callback_data="doc_pension_transfer_region")],
                [InlineKeyboardButton(text="Досрочная пенсия", callback_data="doc_early_pension_request")],
                [InlineKeyboardButton(text="Иск о неправомерном уменьшении пенсии", callback_data="doc_pension_reduction_claim")],
                [InlineKeyboardButton(text="Получение пенсии за умершего родственника", callback_data="doc_relative_pension_request")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    elif category == "loans":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Договор займа", callback_data="doc_credit_contract")],
                [InlineKeyboardButton(text="Жалоба на банк", callback_data="doc_bank_complaint")],
                [InlineKeyboardButton(text="Заявление о снижении ставки по кредиту (Ипотеке)", callback_data="doc_interest_rate_reduction")],
                [InlineKeyboardButton(text="Реструктуризация задолженности", callback_data="doc_debt_restructuring")],
                [InlineKeyboardButton(text="Жалоба на штрафы", callback_data="doc_penalty_complaint")],
                [InlineKeyboardButton(text="Досрочное погашение кредита", callback_data="doc_early_repayment_request")],
                [InlineKeyboardButton(text="Отмена страховки по кредиту", callback_data="doc_credit_insurance_cancellation")],
                [InlineKeyboardButton(text="Иск о возврате комиссии", callback_data="doc_credit_fee_refund")],
                [InlineKeyboardButton(text="Жалоба на навязанные услуги", callback_data="doc_forced_services_complaint")],
                [InlineKeyboardButton(text="Иск о признании договора недействительным", callback_data="doc_credit_contract_invalid")],
                [InlineKeyboardButton(text="Возврат страховки после погашения", callback_data="doc_credit_insurance_refund")],
                [InlineKeyboardButton(text="Жалоба на коллекторов", callback_data="doc_collector_complaint")],
                [InlineKeyboardButton(text="Заявление на реструктуризацию кредита", callback_data="doc_restructure")],
                [InlineKeyboardButton(text="Заявление о возврате страховки по кредиту", callback_data="doc_insurance_refund")],
                [InlineKeyboardButton(text="Заявление о перерасчёте задолженности", callback_data="doc_debt_recalculation")],
                [InlineKeyboardButton(text="Запрос справки о закрытии кредита", callback_data="doc_credit_closure_certificate")],
                [InlineKeyboardButton(text="Заявление о рефинансировании кредита", callback_data="doc_credit_refinance")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )


    elif category == "employment":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Заявление на увольнение", callback_data="doc_dismissal")],
                [InlineKeyboardButton(text="Заявление на отпуск", callback_data="doc_leave_request")],
                [InlineKeyboardButton(text="Заявление о переводе на другую должность", callback_data="doc_position_transfer")],
                [InlineKeyboardButton(text="Иск о восстановлении на работе", callback_data="doc_job_reinstatement_claim")],
                [InlineKeyboardButton(text="Жалоба на нарушение трудового договора", callback_data="doc_employment_violation_complaint")],
                [InlineKeyboardButton(text="Заявление о компенсации за задержку зарплаты", callback_data="doc_salary_delay_compensation")],
                [InlineKeyboardButton(text="Заявление на изменение условий трудового договора", callback_data="doc_employment_conditions_change")],
                [InlineKeyboardButton(text="Иск о взыскании зарплаты", callback_data="doc_salary_claim")],
                [InlineKeyboardButton(text="Жалоба на незаконное увольнение", callback_data="doc_unlawful_dismissal_complaint")],
                [InlineKeyboardButton(text="Заявление о переводе на дистанционную работу", callback_data="doc_remote_work_transfer")],
                [InlineKeyboardButton(text="Заявление о предоставлении справки о доходах", callback_data="doc_income_statement")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )
    elif category == "inheritance":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Завещание в простой письменной форме", callback_data="doc_will")],
                [InlineKeyboardButton(text="Заявление на отказ от наследства", callback_data="doc_refusal")],
                [InlineKeyboardButton(text="Заявление о принятии наследства", callback_data="doc_inheritance_accept")],
                [InlineKeyboardButton(text="Иск о разделе наследства", callback_data="doc_inheritance_division")],
                [InlineKeyboardButton(text="Жалоба на нотариуса", callback_data="doc_notary_complaint")],
                [InlineKeyboardButton(text="Заявление о восстановлении срока принятия наследства", callback_data="doc_inheritance_deadline_restore")],
                [InlineKeyboardButton(text="Завещание об изменении ранее составленного завещания", callback_data="doc_will_change")],
                [InlineKeyboardButton(text="Исковое заявление о недействительности завещания", callback_data="doc_will_invalid")],
                [InlineKeyboardButton(text="Иск об исключении имущества из наследства", callback_data="doc_exclude_property")],
                [InlineKeyboardButton(text="Исковое заявление о признании наследника недостойным", callback_data="doc_unworthy_inheritance")],
                [InlineKeyboardButton(text="Заявление о предоставлении выписки из реестра наследства", callback_data="doc_inheritance_registry_extract")],
                [InlineKeyboardButton(text="Договор о разделе наследства", callback_data="doc_inheritance_division_agreement")],
                [InlineKeyboardButton(text="Заявление о выдаче дубликата свидетельства о праве на наследство", callback_data="doc_inheritance_certificate_duplicate")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )
    elif category == "housing":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Договор аренды(найма жилого помещения)", callback_data="doc_rental")],
                [InlineKeyboardButton(text="Заявление о приватизации жилого помещения", callback_data="doc_privatisation")],
                [InlineKeyboardButton(text="Договор купли-продажи квартиры", callback_data="doc_property_sale")],
                [InlineKeyboardButton(text="Договор дарения", callback_data="doc_property_gift")],
                [InlineKeyboardButton(text="Заявление на улучшение жилищных условий", callback_data="doc_housing_improvement_request")],
                [InlineKeyboardButton(text="Иск о выселении", callback_data="doc_eviction_claim")],
                [InlineKeyboardButton(text="Заявление о признании утраты права пользования жилым помещением", callback_data="doc_usage_rights_termination")],
                [InlineKeyboardButton(text="Иск о недействительности приватизации", callback_data="doc_privatisation_invalid")],
                [InlineKeyboardButton(text="Договор продажи доли жилого помещения", callback_data="doc_property_share_sale")],
                [InlineKeyboardButton(text="Заявление на перерасчёт коммунальных платежей", callback_data="doc_utility_payment_recalculation")],
                [InlineKeyboardButton(text="Иск о восстановлении права пользования", callback_data="doc_housing_rights_restore")],
                [InlineKeyboardButton(text="Иск о признании договора аренды недействительным", callback_data="doc_rent_invalid")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    elif category == "administrative":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Жалоба на постановление об административном правонарушении", callback_data="doc_admin_complaint")],
                [InlineKeyboardButton(text="Иск о признании акта должностного лица незаконным", callback_data="doc_admin_act_illegal_claim")],
                [InlineKeyboardButton(text="Запрос копии административного дела", callback_data="doc_admin_case_copy_request")],
                [InlineKeyboardButton(text="Жалоба на задержание", callback_data="doc_admin_detention_complaint")],
                [InlineKeyboardButton(text="Заявление на отмену административного штрафа", callback_data="doc_admin_fine_cancellation")],
                [InlineKeyboardButton(text="Запрос копии протокола о правонарушении", callback_data="doc_admin_protocol_copy")],
                [InlineKeyboardButton(text="Иск о бездействии должностного лица", callback_data="doc_officer_inaction_claim")],
                [InlineKeyboardButton(text="Ходатайство о восстановлении срока обжалования", callback_data="doc_admin_appeal_deadline_restore")],
                [InlineKeyboardButton(text="Жалоба на действия/бездействие полиции", callback_data="doc_police_complaint")],
                [InlineKeyboardButton(text="Отзыв жалобы на действия/бездействие полиции", callback_data="doc_admin_complaint_withdrawal")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    elif category == "consumer":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Претензия на возмещение убытков причиненных товаром ненадлежащего качества", callback_data="doc_product_complaint")],
                [InlineKeyboardButton(text="Заявление на возврат товара ненадлежащего качества", callback_data="doc_return_defective_product")],
                [InlineKeyboardButton(text="Иск о защите прав потребителей", callback_data="doc_consumer_protection_claim")],
                [InlineKeyboardButton(text="Претензия на задержку доставки", callback_data="doc_delivery_delay_complaint")],
                [InlineKeyboardButton(text="Заявление на обмен товара ненадлежащего качества", callback_data="doc_exchange_defective_product")],
                [InlineKeyboardButton(text="Жалоба на услуги ненадлежащего качества", callback_data="doc_service_quality_complaint")],
                [InlineKeyboardButton(text="Заявление на возврат средств за неоказанную услугу", callback_data="doc_refund_for_unprovided_service")],
                [InlineKeyboardButton(text="Претензия на устранение недостатков товара", callback_data="doc_fix_defective_product")],
                [InlineKeyboardButton(text="Иск о возврате предоплаты", callback_data="doc_advance_payment_claim")],
                [InlineKeyboardButton(text="Претензия на сроки оказания услуг", callback_data="doc_service_deadline_complaint")],
                [InlineKeyboardButton(text="Заявление о расторжение договора купли-продажи", callback_data="doc_purchase_contract_termination")],
                [InlineKeyboardButton(text="Иск об оспаривании навязанной услуги", callback_data="doc_forced_service_dispute")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    elif category == "tax":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Жалоба на налоговый орган", callback_data="doc_tax_complaint")],
                [InlineKeyboardButton(text="Заявление на возврат переплаты по налогам", callback_data="doc_tax_overpayment_return")],
                [InlineKeyboardButton(text="Заявление о рассрочке уплаты налогов", callback_data="doc_tax_payment_installment")],
                [InlineKeyboardButton(text="Заявление о перерасчёте налогов", callback_data="doc_tax_recalculation")],
                [InlineKeyboardButton(text="Заявление на налоговый вычет", callback_data="doc_tax_deduction")],
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )

    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="document_categories_menu")],
            ]
        )


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

    # Обработка категорий
    if data.startswith("category_"):
        category = data.split("_", 1)[1]
        category_mapping = {
            "family": "Семейное право",
            # Добавьте остальные категории...
        }
        category_name = category_mapping.get(category)

        if category_name:
            bot.editMessageText(
                (msg['message']['chat']['id'], msg['message']['message_id']),
                f"Вы выбрали: {category_name}. Вот список доступных документов:",
                reply_markup=document_list_menu(category_name)
            )
        else:
            bot.editMessageText(
                (msg['message']['chat']['id'], msg['message']['message_id']),
                "Неизвестная категория. Попробуйте снова."
            )


# Основная функция для обработки сообщений
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        # Пример обработки обычного текста, если нужно
        bot.sendMessage(chat_id, "Выберите категорию документов.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Семейное право", callback_data="category_family")],
            [InlineKeyboardButton(text="Назад", callback_data="category_back")]
        ]))


