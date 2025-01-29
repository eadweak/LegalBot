import os
import logging
from aiogram.filters import StateFilter
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Dispatcher
from aiogram import Bot
from bot.config import ADMIN_USER_ID
from bot.utils.database import log_interaction
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters import Command
from bot.templates.document_templates import generate_document
from bot.keyboards.document_menu import document_categories_menu, document_list_menu
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from docx import Document
from aiogram.types.input_file import FSInputFile

logging.basicConfig(level=logging.DEBUG)

# Главное меню документов
def document_menu(message):
    message.answer(
        text="Выберите категорию документов:",
        reply_markup=document_categories_menu()
    )

class FillDocumentState(StatesGroup): #Настройка машины состояний (FSM)
    """
    Состояния для заполнения документа.
    """
    waiting_for_field1 = State()  # Ожидание ввода первого поля
    waiting_for_field2 = State()  # Ожидание ввода второго поля
    waiting_for_field3 = State()  # Ожидание ввода третьего поля

# Выбор конкретного документа
def document_list(message):
    category = message.text
    supported_categories = [
        "Семейное право", "Субсидии и выплаты", "Пенсионное право",
        "Кредиты и услуги при кредитах", "Трудовое право", "Наследственное право",
        "Жилищное право", "Административное право", "Защита прав потребителей",
        "Банковское право", "Налоговое право"
    ]

    if category in supported_categories:
        message.answer(
            "Выберите документ из категории \"{}\":".format(category),
            reply_markup=document_list_menu(category)
        )
    else:
        message.answer("Эта категория пока не поддерживается. Выберите из доступных категорий.")

async def help_request(callback: CallbackQuery):
    """
    Обработчик для кнопки "Обратиться за помощью к специалисту".
    Отправляет уведомление администратору.
    """
    log_interaction(callback.from_user.id, "help_request")

    # Сообщение для пользователя
    await callback.message.answer("Ваш запрос отправлен специалисту. Мы свяжемся с вами в ближайшее время.")
    await callback.answer()

    # Сообщение для администратора
    admin_message = (
        f"Новый запрос на консультацию:\n"
        f"Пользователь: @{callback.from_user.username or 'Имя отсутствует'} "
        f"(ID: {callback.from_user.id})\n"
        f"Тема: None\n"  # Если нужна тема, её можно запросить ранее
        f"Контакты: {callback.from_user.id}"
    )

    # Отправляем сообщение администратору
    await callback.bot.send_message(ADMIN_USER_ID, admin_message)

async def handle_help_request(message: Message, bot: Bot):
    """
    Обработка сообщения пользователя и отправка его администратору.
    """
    log_interaction(message.from_user.id, f"help_request_data: {message.text}")

    # Отправляем уведомление администратору
    await bot.send_message(
        ADMIN_USER_ID,
        f"Новое сообщение от пользователя:\n\n"
        f"Пользователь: {message.from_user.full_name}\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )
    await message.answer("Ваше сообщение отправлено специалисту. Мы свяжемся с вами в ближайшее время.")


async def handle_document(callback: CallbackQuery):
    """Обработчик для кнопок документов."""

    # Словарь с названиями документов
    document_titles = {
        "doc_marriage": "Брачный договор",
        "doc_divorce": "Документ о расторжении брака",
        "doc_property_division": "Соглашение о разделе имущества",
        "doc_children_agreement": "Соглашение о содержании детей",
        "doc_alimony_claim": "Иск о взыскании алиментов",
        "doc_alimony_agreement": "Соглашение об алиментах",
        "doc_child_residence": "Определение места жительства ребенка",
        "doc_fatherhood": "Заявление об установлении отцовства",
        "doc_parental_rights": "Заявление об отказе от родительских прав",
        "doc_parental_rights_claim": "Иск о лишении родительских прав",
        "doc_extra_expenses": "Соглашение о дополнительных расходах",
        "doc_annul_marriage": "Признание брака недействительным",
        "doc_communication_child": "Соглашение об общении с ребенком",
        "doc_reduce_alimony": "Иск об уменьшении алиментов",
    }

    # Получение текста документа из словаря
    document_title = document_titles.get(callback.data, "Документ")

    # Генерация кнопок
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Скачать шаблон документа", callback_data=f"{callback.data}_download")],
            [InlineKeyboardButton(text="Заполнить шаблон в боте", callback_data=f"{callback.data}_fill")],
            [InlineKeyboardButton(text="Обратиться за помощью к специалисту", callback_data="consult")],
            [InlineKeyboardButton(text="Назад", callback_data="category_back")],
        ]
    )

    # Отправка сообщения
    await callback.message.edit_text(
        text=f"Вы выбрали: {document_title}.\nВыберите одно из доступных действий:",
        reply_markup=keyboard,
    )
    await callback.answer()




# Обработчик для кнопки "Скачать шаблон"
async def handle_download(callback: CallbackQuery):
    """
    Обработчик для кнопки "Скачать шаблон документа".
    """
    logging.debug(f"Получен callback: {callback.data}")
    print(f"Получен callback: {callback.data}")  # Вывод в консоль
    print("Существуют ли файлы?")
    print("doc_marriage.doc:", os.path.exists("/templates/doc_marriage.doc"))
    print("doc_divorce.doc:", os.path.exists("/templates/doc_divorce.doc"))
    print("Текущая рабочая директория:", os.getcwd())
    # Определяем абсолютный путь к папке templates
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
    # Словарь с файлами шаблонов
    file_map = {
        "doc_marriage_download": os.path.join(TEMPLATES_DIR, "doc_marriage.doc"),
        "doc_divorce_download": os.path.join(TEMPLATES_DIR, "doc_divorce.doc"),
        "doc_alimony_claim_download": os.path.join(TEMPLATES_DIR, "doc_alimony_claim.doc"),
        "doc_alimony_agreement_download": os.path.join(TEMPLATES_DIR, "doc_alimony_agreement.doc"),
        "doc_child_residence_download": os.path.join(TEMPLATES_DIR,"doc_child_residence.doc"),
        "doc_fatherhood_download": os.path.join(TEMPLATES_DIR, "doc_fatherhood.doc"),
        "doc_parental_rights_download": os.path.join(TEMPLATES_DIR, "doc_parental_rights.doc"),
        "doc_parental_rights_claim_download": os.path.join(TEMPLATES_DIR, "doc_parental_rights_claim.doc"),
        "doc_annul_marriage_download": os.path.join(TEMPLATES_DIR, "doc_annul_marriage.doc"),
        "doc_communication_child_download": os.path.join(TEMPLATES_DIR, "doc_communication_child.doc"),
        "doc_reduce_alimony_download": os.path.join(TEMPLATES_DIR, "doc_reduce_alimony.doc"),
        "doc_property_division_download": os.path.join(TEMPLATES_DIR, "doc_property_division.doc"),
        "doc_children_agreement_download": os.path.join(TEMPLATES_DIR, "doc_children_agreement.doc"),
        "doc_subsidy_request_download": os.path.join(TEMPLATES_DIR, "doc_subsidy_request.doc"),
        "doc_subsidy_complaint_download": os.path.join(TEMPLATES_DIR, "doc_subsidy_complaint.doc"),
        "doc_subsidy_denial_complaint_download": os.path.join(TEMPLATES_DIR, "doc_subsidy_denial_complaint.doc"),
        "doc_payment_extension_download": os.path.join(TEMPLATES_DIR, "doc_payment_extension.doc"),
        "doc_subsidy_info_request_download": os.path.join(TEMPLATES_DIR, "doc_subsidy_info_request.doc"),
        "doc_pension_request_download": os.path.join(TEMPLATES_DIR, "doc_pension_request.doc"),
        "doc_pfr_complaint_download": os.path.join(TEMPLATES_DIR, "doc_pfr_complaint.doc"),
        "doc_pension_recalculation_download": os.path.join(TEMPLATES_DIR,"doc_pension_recalculation.doc"),
        "doc_pension_missing_claim_download": os.path.join(TEMPLATES_DIR,"doc_pension_missing_claim.doc"),
        "doc_pension_denial_complaint_download": os.path.join(TEMPLATES_DIR,"doc_pension_denial_complaint.doc"),
        "doc_pension_restoration_download": os.path.join(TEMPLATES_DIR,"doc_pension_restoration.doc"),
        "doc_pension_transfer_region_download":os.path.join(TEMPLATES_DIR, "doc_pension_transfer_region.doc"),
        "doc_early_pension_request_download": os.path.join(TEMPLATES_DIR, "doc_early_pension_request.doc"),
        "doc_pension_reduction_claim_download": os.path.join(TEMPLATES_DIR, "doc_pension_reduction_claim.doc"),
        "doc_relative_pension_request_download": os.path.join(TEMPLATES_DIR, "doc_relative_pension_request.doc"),
        "doc_credit_contract_download": os.path.join(TEMPLATES_DIR, "doc_credit_contract.doc"),
        "doc_bank_complaint_download": os.path.join(TEMPLATES_DIR, "doc_bank_complaint.doc"),
        "doc_interest_rate_reduction_download": os.path.join(TEMPLATES_DIR, "doc_interest_rate_reduction.doc"),
        "doc_debt_restructuring_download": os.path.join(TEMPLATES_DIR, "doc_debt_restructuring.doc"),
        "doc_penalty_complaint_download": os.path.join(TEMPLATES_DIR, "doc_penalty_complaint.doc"),
        "doc_early_repayment_request_download": os.path.join(TEMPLATES_DIR, "doc_early_repayment_request.doc"),
        "doc_credit_insurance_cancellation_download": os.path.join(TEMPLATES_DIR, "doc_credit_insurance_cancellation.doc"),
        "doc_credit_fee_refund_download": os.path.join(TEMPLATES_DIR, "doc_credit_fee_refund_request.doc"),
        "doc_forced_services_complaint_download": os.path.join(TEMPLATES_DIR, "doc_forced_services_complaint.doc"),
        "doc_credit_contract_invalid_download": os.path.join(TEMPLATES_DIR, "doc_credit_contract_invalid.doc"),
        "doc_credit_insurance_refund_download": os.path.join(TEMPLATES_DIR, "doc_credit_insurance_refund.doc"),
        "doc_collector_complaint_download": os.path.join(TEMPLATES_DIR, "doc_collector_complaint.doc"),
        "doc_restructure_download": os.path.join(TEMPLATES_DIR, "doc_restructure.doc"),
        "doc_insurance_refund_download": os.path.join(TEMPLATES_DIR, "doc_insurance_refund.doc"),
        "doc_debt_recalculation_download": os.path.join(TEMPLATES_DIR, "doc_debt_recalculation.doc"),
        "doc_credit_closure_certificate_download": os.path.join(TEMPLATES_DIR, "doc_credit_closure_certificate.doc"),
        "doc_credit_refinance_download": os.path.join(TEMPLATES_DIR, "doc_credit_refinance.doc"),
        "doc_dismissal_download": os.path.join(TEMPLATES_DIR, "doc_dismissal.doc"),
        "doc_leave_request_download": os.path.join(TEMPLATES_DIR, "doc_leave_request.doc"),
        "doc_position_transfer_download": os.path.join(TEMPLATES_DIR, "doc_position_transfer.doc"),
        "doc_job_reinstatement_claim_download": os.path.join(TEMPLATES_DIR, "doc_job_reinstatement_claim.doc"),
        "doc_employment_violation_complaint_download": os.path.join(TEMPLATES_DIR, "doc_employment_violation_complaint.doc"),
        "doc_salary_delay_compensation_download": os.path.join(TEMPLATES_DIR, "doc_salary_delay_compensation.doc"),
        "doc_employment_conditions_change_download": os.path.join(TEMPLATES_DIR, "doc_employment_conditions_change.doc"),
        "doc_salary_claim_download": os.path.join(TEMPLATES_DIR, "doc_salary_claim.doc"),
        "doc_unlawful_dismissal_complaint_download": os.path.join(TEMPLATES_DIR, "doc_unlawful_dismissal_complaint.doc"),
        "doc_remote_work_transfer_download": os.path.join(TEMPLATES_DIR, "doc_remote_work_transfer.doc"),
        "doc_income_statement_download": os.path.join(TEMPLATES_DIR, "doc_income_statement.doc"),
        "doc_will_download": os.path.join(TEMPLATES_DIR, "doc_will.doc"),
        "doc_refusal_download": os.path.join(TEMPLATES_DIR, "doc_refusal.doc"),
        "doc_inheritance_accept_download": os.path.join(TEMPLATES_DIR, "doc_inheritance_accept.doc"),
        "doc_inheritance_division_download": os.path.join(TEMPLATES_DIR, "doc_inheritance_division.doc"),
        "doc_notary_complaint_download": os.path.join(TEMPLATES_DIR, "doc_notary_complaint.doc"),
        "doc_inheritance_deadline_restore_download": os.path.join(TEMPLATES_DIR, "doc_inheritance_deadline_restore.doc"),
        "doc_will_change_download": os.path.join(TEMPLATES_DIR, "doc_will_change.doc"),
        "doc_will_invalid_download": os.path.join(TEMPLATES_DIR, "doc_will_invalid.doc"),
        "doc_exclude_property_download": os.path.join(TEMPLATES_DIR, "doc_exclude_property.doc"),
        "doc_unworthy_inheritance_download": os.path.join(TEMPLATES_DIR, "doc_unworthy_inheritance.doc"),
        "doc_inheritance_registry_extract_download": os.path.join(TEMPLATES_DIR, "doc_inheritance_registry_extract.doc"),
        "doc_inheritance_division_agreement_download": os.path.join(TEMPLATES_DIR, "doc_inheritance_division_agreement.doc"),
        "doc_inheritance_certificate_duplicate_download": os.path.join(TEMPLATES_DIR, "doc_inheritance_certificate_duplicate.doc"),
        "doc_rental_download": os.path.join(TEMPLATES_DIR, "doc_rental.doc"),
        "doc_privatisation_download": os.path.join(TEMPLATES_DIR, "doc_privatisation.doc"),
        "doc_property_sale_download": os.path.join(TEMPLATES_DIR, "doc_property_sale.doc"),
        "doc_property_gift_download": os.path.join(TEMPLATES_DIR, "doc_property_gift.doc"),
        "doc_housing_improvement_request_download": os.path.join(TEMPLATES_DIR, "doc_housing_improvement_request.doc"),
        "doc_eviction_claim_download": os.path.join(TEMPLATES_DIR, "doc_eviction_claim.doc"),
        "doc_usage_rights_termination_download": os.path.join(TEMPLATES_DIR, "doc_usage_rights_termination.doc"),
        "doc_privatisation_invalid_download": os.path.join(TEMPLATES_DIR, "doc_privatisation_invalid.doc"),
        "doc_property_share_sale_download": os.path.join(TEMPLATES_DIR, "doc_property_share_sale.doc"),
        "doc_utility_payment_recalculation_download": os.path.join(TEMPLATES_DIR, "doc_utility_payment_recalculation.doc"),
        "doc_housing_rights_restore_download": os.path.join(TEMPLATES_DIR, "doc_housing_rights_restore.doc"),
        "doc_rent_invalid_download": os.path.join(TEMPLATES_DIR, "doc_rent_invalid.doc"),
        "doc_admin_complaint_download": os.path.join(TEMPLATES_DIR, "doc_admin_complaint.doc"),
        "doc_admin_act_illegal_claim_download": os.path.join(TEMPLATES_DIR, "doc_admin_act_illegal_claim.doc"),
        "doc_admin_case_copy_request_download": os.path.join(TEMPLATES_DIR, "doc_admin_case_copy_request.doc"),
        "doc_admin_detention_complaint_download": os.path.join(TEMPLATES_DIR, "doc_admin_detention_complaint.doc"),
        "doc_admin_fine_cancellation_download": os.path.join(TEMPLATES_DIR, "doc_admin_fine_cancellation.doc"),
        "doc_admin_protocol_copy_download": os.path.join(TEMPLATES_DIR, "doc_admin_protocol_copy.doc"),
        "doc_officer_inaction_claim_download": os.path.join(TEMPLATES_DIR, "doc_officer_inaction_claim.doc"),
        "doc_admin_appeal_deadline_restore_download": os.path.join(TEMPLATES_DIR, "doc_admin_appeal_deadline_restore.doc"),
        "doc_police_complaint_download": os.path.join(TEMPLATES_DIR, "doc_police_complaint.doc"),
        "doc_admin_complaint_withdrawal_download": os.path.join(TEMPLATES_DIR, "doc_admin_complaint_withdrawal.doc"),
        "doc_product_complaint_download": os.path.join(TEMPLATES_DIR, "doc_product_complaint.doc"),
        "doc_return_defective_product_download": os.path.join(TEMPLATES_DIR, "doc_return_defective_product.doc"),
        "doc_consumer_protection_claim_download": os.path.join(TEMPLATES_DIR, "doc_consumer_protection_claim.doc"),
        "doc_delivery_delay_complaint_download": os.path.join(TEMPLATES_DIR, "doc_delivery_delay_complaint.doc"),
        "doc_exchange_defective_product_download": os.path.join(TEMPLATES_DIR, "doc_exchange_defective_product.doc"),
        "doc_service_quality_complaint_download": os.path.join(TEMPLATES_DIR, "doc_service_quality_complaint.doc"),
        "doc_refund_for_unprovided_service_download": os.path.join(TEMPLATES_DIR, "doc_refund_for_unprovided_service.doc"),
        "doc_fix_defective_product_download": os.path.join(TEMPLATES_DIR, "doc_fix_defective_product.doc"),
        "doc_advance_payment_claim_download": os.path.join(TEMPLATES_DIR, "doc_advance_payment_claim.doc"),
        "doc_service_deadline_complaint_download": os.path.join(TEMPLATES_DIR, "doc_service_deadline_complaint.doc"),
        "doc_purchase_contract_termination_download": os.path.join(TEMPLATES_DIR, "doc_purchase_contract_termination.doc"),
        "doc_forced_service_dispute_download": os.path.join(TEMPLATES_DIR, "doc_forced_service_dispute.doc"),
        "doc_tax_complaint_download": os.path.join(TEMPLATES_DIR, "doc_tax_complaint.doc"),
        "doc_tax_overpayment_return_download": os.path.join(TEMPLATES_DIR, "doc_tax_overpayment_return.doc"),
        "doc_tax_payment_installment_download": os.path.join(TEMPLATES_DIR,"doc_tax_payment_installment.doc"),
        "doc_tax_recalculation_download": os.path.join(TEMPLATES_DIR, "doc_tax_recalculation.doc"),
        "doc_tax_deduction_download": os.path.join(TEMPLATES_DIR, "doc_tax_deduction.doc"),
        # Добавьте пути к остальным шаблонам
    }

    # Получаем путь к файлу
    file_path = file_map.get(callback.data)

    if file_path and os.path.exists(file_path):
        try:
            # Используем FSInputFile для передачи файла
            document = FSInputFile(file_path)
            await callback.message.answer_document(document)
        except Exception as e:
            await callback.message.answer(f"Ошибка при отправке файла: {e}")
    else:
        await callback.message.answer("Шаблон для этого документа пока недоступен.")
    await callback.answer()

# Обработчик для кнопки "Заполнить шаблон"
def handle_fill(callback, state):
    """
    Обработчик для кнопки "Заполнить шаблон в боте".
    """
    # Начинаем процесс заполнения документа
    state.set_state(FillDocumentState.waiting_for_field1)
    callback.message.edit_text(
        u"Процесс заполнения документа начат.\n\nПожалуйста, введите значение для первого поля (например, ФИО):"
    )
    callback.answer()


# Обработчик для кнопки "Помощь"
def handle_help(callback):
    """
    Обработчик для кнопки "Обратиться за помощью к специалисту".
    """
    # ID чата специалиста
    specialist_chat_id = 123456789  # Укажите здесь ID специалиста или чата с поддержкой

    # Сообщение специалисту
    callback.bot.send_message(
        specialist_chat_id,
        u"Пользователь запросил помощь по документу: {}".format(callback.data)
    )

    # Сообщение пользователю
    callback.message.answer(
        u"Ваш запрос на помощь отправлен специалисту. Ожидайте ответа."
    )
    callback.answer()


# Обработчик для кнопки "Назад"
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите категорию документов:",
        reply_markup=document_categories_menu()
    )
    await callback.answer()

# Генерация документа
def generate_document_handler(message):
    # Пример данных
    data = {
        "fio": "Иванов Иван Иванович",
        "address": "г. Москва, ул. Ленина, д. 1",
        "spouse": "Петрова Мария Ивановна",
        "spouse_address": "г. Санкт-Петербург, ул. Победы, д. 10",
    }
    document = generate_document(data)
    message.answer("Ваш документ:\n\n{}".format(document))

# Обработка нажатий на кнопки из InlineKeyboardMarkup
CATEGORY_MAPPING = {
    "family": "Семейное право",
    "pension": "Пенсионное право",
    "employment": "Трудовое право",
    "inheritance": "Наследственное право",
    "housing": "Жилищное право",
    "bank": "Банковское право",
    "corporate": "Корпоративное право",
    "tax": "Налоговое право",
    "consumer": "Защита прав потребителей",
}


def handle_category(callback: CallbackQuery):
    logging.info(f"Получен callback: {callback.data}")
    category_key = callback.data.replace("category_", "")
    category_name = CATEGORY_MAPPING.get(category_key)
    if category_name:
        menu = document_list_menu(category_name)
        logging.info(f"Меню для категории {category_name}: {menu}")
        if menu:
            try:
                callback.message.edit_text(
                    text=f"Вы выбрали категорию: {category_name}\nВыберите документ:",
                    reply_markup=menu
                )
                logging.info(f"Сообщение успешно обновлено для категории: {category_name}")
            except Exception as e:
                logging.error(f"Ошибка при обновлении сообщения: {e}")
                callback.message.answer(
                    text=f"Вы выбрали категорию: {category_name}\nВыберите документ:",
                    reply_markup=menu
                )
        else:
            callback.message.answer("Меню для выбранной категории временно недоступно.")
    else:
        callback.message.answer("Неизвестная категория. Попробуйте ещё раз.")
    callback.answer()

#Последовательная обработка полей
def handle_field1(message, state):
    """
    Обработка ввода для первого поля.
    """
    # Сохраняем первое поле
    state.update_data(field1=message.text)

    # Переходим к следующему полю
    state.set_state(FillDocumentState.waiting_for_field2)
    message.answer(u"Введите значение для второго поля (например, адрес):")


def handle_field2(message, state):
    """
    Обработка ввода для второго поля.
    """
    # Сохраняем второе поле
    state.update_data(field2=message.text)

    # Переходим к следующему полю
    state.set_state(FillDocumentState.waiting_for_field3)
    message.answer(u"Введите значение для третьего поля (например, дата рождения):")


def handle_field3(message, state):
    """
    Обработка ввода для третьего поля.
    """
    # Сохраняем третье поле
    state.update_data(field3=message.text)

    # Получаем данные
    data = state.get_data()
    field1 = data.get("field1", "")
    field2 = data.get("field2", "")
    field3 = data.get("field3", "")

    # Путь к шаблону и сохранённому файлу
    template_path = "templates/document_template.docx"  # Укажите путь к шаблону
    output_path = "generated_documents/filled_document.docx"  # Укажите путь для сохранения

    # Создаём директорию для сохранённых файлов, если она отсутствует
    if not os.path.exists("generated_documents"):
        os.makedirs("generated_documents")

    # Сохраняем заполненный документ
    save_document(
        {"field1": field1, "field2": field2, "field3": field3},
        template_path,
        output_path
    )

    # Отправляем файл пользователю
    if os.path.exists(output_path):
        message.answer_document(open(output_path, "rb"))
    else:
        message.answer(u"Ошибка при создании документа. Пожалуйста, попробуйте снова.")

    # Завершаем состояние
    state.clear()

def save_document(data, template_path, output_path):
    """
    Генерация заполненного документа из шаблона.
    :param data: словарь с данными для заполнения.
    :param template_path: путь к шаблону.
    :param output_path: путь к сохранённому файлу.
    """
    # Открываем шаблон документа
    document = Document(template_path)

    # Заполняем шаблон
    for paragraph in document.paragraphs:
        for key, value in data.items():
            if "{{" + key + "}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{" + key + "}}", value)

    # Сохраняем заполненный документ
    document.save(output_path)



# Регистрация всех обработчиков
def register_document_handlers(dp: Dispatcher):
    dp.message.register(document_menu, Command("documents"))
    dp.message.register(document_list)
    #Обработчик для кнопок в меню документа
    dp.callback_query.register(handle_document, lambda c: c.data.startswith("doc_"))
    dp.message.register(generate_document_handler, Command("generate_document"))
    dp.callback_query.register(handle_category, lambda c: c.data.startswith("category_"))
    # Регистрация кнопки "Заполнить шаблон"
    dp.callback_query.register(handle_fill, lambda c: c.data.endswith("_fill"))
    # Регистрация шагов FSM
    dp.message.register(handle_field1, FillDocumentState.waiting_for_field1)
    dp.message.register(handle_field2, FillDocumentState.waiting_for_field2)
    dp.message.register(handle_field3, FillDocumentState.waiting_for_field3)

    # Обработчик кнопки "Скачать шаблон документа"
    dp.callback_query.register(handle_download, lambda c: c.data.endswith("_download"))

    # Обработчик кнопки "Обратиться за помощью к специалисту"
    dp.callback_query.register(help_request, lambda c: c.data == "consult")

    # Обработчик кнопки "Назад"
    dp.callback_query.register(handle_back, lambda c: c.data == "document_categories_menu")
