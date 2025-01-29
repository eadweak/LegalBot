import sqlite3
from datetime import datetime, timedelta




# Инициализация базы данных
def initialize_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Создание таблицы users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            free_access_until TIMESTAMP,
            referral_code TEXT,
            referred_by INTEGER
        )
    ''')

    # Создание таблицы для логирования взаимодействий (опционально)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            interaction TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Создание таблицы для запросов на консультации
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consult_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            consultation_topic TEXT NOT NULL,
            contact_info TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()


# Сохранение запроса на консультацию
def save_consult_request(telegram_id, consultation_topic, contact_info=None):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO consult_requests (telegram_id, consultation_topic, contact_info)
        VALUES (?, ?, ?)
    ''', (telegram_id, consultation_topic, contact_info))

    connection.commit()
    connection.close()


# Проверка бесплатного доступа
def check_free_access(telegram_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT free_access_until FROM users WHERE telegram_id = ?
    ''', (telegram_id,))
    result = cursor.fetchone()

    connection.close()

    if not result:
        return False

    free_access_until = result[0]
    if free_access_until and datetime.strptime(free_access_until, "%Y-%m-%d %H:%M:%S") > datetime.now():
        return True
    return False


# Регистрация пользователя
def register_user(telegram_id, name, referral_code=None):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()

    if user is None:
        free_access_until = datetime.now() + timedelta(days=30)

        cursor.execute('''
            INSERT INTO users (telegram_id, name, free_access_until, referral_code, referred_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, name, free_access_until, referral_code, None))

    connection.commit()
    connection.close()


# Генерация реферального кода
def generate_referral_code(telegram_id):
    return f"REF-{telegram_id}"


# Логирование взаимодействий
def log_interaction(telegram_id, interaction):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO interactions (telegram_id, interaction)
        VALUES (?, ?)
    ''', (telegram_id, interaction))

    connection.commit()
    connection.close()
