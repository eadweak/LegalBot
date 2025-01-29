import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.subscription_menu import subscription_menu

# Конфигурация
PAYMENT_TOKEN = "YOUR_PAYMENT_TOKEN"  # Замените на ваш токен платежного провайдера
DB_PATH = "users.db"  # Путь к базе данных пользователей
LICENSE_DB_PATH = "license_keys.db"  # Путь к базе данных лицензионных ключей

# Цены на подписку
PRICES = [
    LabeledPrice(label="Подписка на 1 неделю", amount=10000),  # 100.00 RUB (в копейках)
    LabeledPrice(label="Подписка на 1 месяц", amount=50000),  # 500.00 RUB (в копейках)
    LabeledPrice(label="Подписка на 3 месяца", amount=130000),  # 1300.00 RUB (в копейках)
    LabeledPrice(label="Годовая подписка", amount=500000),  # 5000.00 RUB (в копейках)
]

# Состояния для FSM
class LicenseKeyState(StatesGroup):
    waiting_for_key = State()  # Состояние ожидания ввода лицензионного ключа

# Обработка нажатия на кнопку "Управление подпиской".
async def handle_subscriptions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите категорию:", reply_markup=subscription_menu())
    await callback.answer()

# Обработчик кнопки "Узнать статус моей подписки"
async def subscription_status(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT subscription_expiry FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()

    if result:
        subscription_expiry = result[0]
        await callback.message.edit_text(f"Ваш статус подписки: Активна до {subscription_expiry}")
    else:
        await callback.message.edit_text("У вас нет активной подписки. Зарегистрируйтесь или оформите подписку.")

    conn.close()
    await callback.answer()


# Обработчик кнопки "Оплатить подписку"
async def pay_subscription(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Подписка на сервис",
        description="Оплата подписки на использование сервиса",
        payload="subscription_payload",
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=PRICES,
        start_parameter="subscription-payment",
    )
    await callback.answer()


# Обработчик успешной оплаты
async def successful_payment(message: Message):
    payment_info = message.successful_payment.to_python()
    print(f"Платёж успешен: {payment_info}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Определяем срок подписки
    if payment_info["invoice_payload"] == "subscription_payload_monthly":
        new_expiry_date = datetime.now() + timedelta(days=30)
    elif payment_info["invoice_payload"] == "subscription_payload_yearly":
        new_expiry_date = datetime.now() + timedelta(days=365)
    else:
        await message.answer("Неизвестный тип подписки.")
        conn.close()
        return

    expiry_date_str = new_expiry_date.strftime("%Y-%m-%d %H:%M:%S")
    telegram_id = message.from_user.id

    cursor.execute(
        "UPDATE users SET subscription_expiry = ? WHERE telegram_id = ?",
        (expiry_date_str, telegram_id)
    )
    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO users (telegram_id, subscription_expiry) VALUES (?, ?)",
            (telegram_id, expiry_date_str)
        )

    conn.commit()
    conn.close()
    await message.answer(f"Спасибо за оплату! Ваша подписка активирована до {expiry_date_str}.")


# Обработчик кнопки "Пригласить друга"
async def invite_friend(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    invite_link = f"https://t.me/your_bot?start=ref_{telegram_id}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Исправленное создание таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            subscription_expiry INTEGER
        )
    ''')

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (telegram_id, subscription_expiry) VALUES (?, ?)",
            (telegram_id, None)
        )

    conn.commit()
    conn.close()

    await callback.message.edit_text(
        f"Пригласите друга, отправив ему эту ссылку: {invite_link}\n\n"
        f"Если друг зарегистрируется и оплатит подписку, вы получите бонус!"
    )
    await callback.answer()


# Обработчик реферальной ссылки
async def process_referral(message: types.Message):
    # Проверяем, содержит ли сообщение реферальную ссылку
    if message.text.startswith("/start ref_"):
        # Извлекаем ID реферера из ссылки
        referrer_id = int(message.text.split("_")[1])
        user_id = message.from_user.id

        # Подключаемся к базе данных
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Создаем таблицу, если она еще не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                subscription_expiry INTEGER,
                referrals INTEGER DEFAULT 0
            )
        ''')

        # Проверяем, зарегистрирован ли пользователь
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
        if cursor.fetchone() is None:
            # Если пользователь не зарегистрирован, добавляем его в базу
            cursor.execute(
                "INSERT INTO users (telegram_id, subscription_expiry) VALUES (?, ?)",
                (user_id, None)
            )

            # Увеличиваем счетчик рефералов у реферера
            cursor.execute(
                "UPDATE users SET referrals = COALESCE(referrals, 0) + 1 WHERE telegram_id = ?",
                (referrer_id,)
            )

            await message.answer("Вы зарегистрировались по реферальной ссылке. Спасибо!")
        else:
            # Если пользователь уже зарегистрирован
            await message.answer("Вы уже зарегистрированы.")

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()



# Обработчик кнопки "Ввести лицензионный ключ"
async def enter_license_key(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, введите ваш лицензионный ключ:")
    await state.set_state(LicenseKeyState.waiting_for_key)
    await callback.answer()


# Обработка введённого лицензионного ключа
async def process_license_key(message: Message, state: FSMContext):
    license_key = message.text.strip()

    conn = sqlite3.connect(LICENSE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT subscription_duration FROM license_keys WHERE key = ? AND is_used = 0", (license_key,))
    result = cursor.fetchone()

    if result:
        subscription_duration = result[0]
        new_expiry_date = datetime.now() + timedelta(days=subscription_duration)
        expiry_date_str = new_expiry_date.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("UPDATE license_keys SET is_used = 1 WHERE key = ?", (license_key,))

        telegram_id = message.from_user.id
        cursor.execute(
            "UPDATE users SET subscription_expiry = ? WHERE telegram_id = ?",
            (expiry_date_str, telegram_id)
        )
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO users (telegram_id, subscription_expiry) VALUES (?, ?)",
                (telegram_id, expiry_date_str)
            )

        conn.commit()
        conn.close()

        await message.answer(f"Ключ принят! Ваша подписка активирована до {expiry_date_str}.")
    else:
        await message.answer("Ключ недействителен или уже использован. Попробуйте снова.")

    await state.clear()


# Обработчик кнопки "Купить лицензионный ключ"
async def buy_license_key(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Лицензионный ключ подписки",
        description="Ключ для активации подписки на 30 или 365 дней.",
        payload="license_key_purchase",
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=PRICES,
        start_parameter="license-key-payment"
    )
    await callback.answer()


# Регистрация обработчиков
def register_subscription_handlers(dp: Dispatcher):
    dp.callback_query.register(handle_subscriptions, lambda c: c.data == "subscriptions")
    dp.callback_query.register(subscription_status, lambda c: c.data == "subscription_status")
    dp.callback_query.register(pay_subscription, lambda c: c.data == "pay_subscription")
    dp.callback_query.register(invite_friend, lambda c: c.data == "invite_friend")
    dp.callback_query.register(enter_license_key, lambda c: c.data == "enter_license_key")
    dp.callback_query.register(buy_license_key, lambda c: c.data == "buy_license_key")
    dp.message.register(process_license_key, LicenseKeyState.waiting_for_key)
    dp.message.register(process_referral, lambda m: m.text.startswith("/start ref_"))
    dp.message.register(successful_payment, lambda m: m.successful_payment)