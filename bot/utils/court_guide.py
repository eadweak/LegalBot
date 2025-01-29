import logging
import sqlite3
from typing import List, Dict

from aiofiles import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Константа URL
BASE_URL = "https://sudrf.ru/index.php?id=300"

# ---------- Настройка WebDriver ----------
def setup_driver(headless: bool = True, log_level: int = 3) -> webdriver.Chrome:
    """
    Создаёт и настраивает WebDriver.
    :param headless: Указывает, должен ли браузер работать в headless-режиме.
    :param log_level: Уровень логирования драйвера (0-3, где 0 - максимум).
    :return: Настроенный экземпляр WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=" + str(log_level))
    if headless:
        chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)



# ---------- Функции для парсинга данных ----------
def get_regions(driver):
    """Получение данных о регионах с сайта sudrf.ru."""
    url = "https://sudrf.ru/index.php?id=300"
    driver.get(url)

    try:
        # Ожидание загрузки элемента <select> с ID "court_subj"
        region_select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "court_subj"))
        )
        print("Элемент найден: court_subj")

        # Вывод содержимого элемента для диагностики
        print("Содержимое court_subj:")
        print(region_select.get_attribute("outerHTML"))

        # Извлекаем данные регионов
        regions = region_select.find_elements(By.TAG_NAME, "option")
        region_data = []
        for region in regions:
            region_id = region.get_attribute("value")
            region_name = region.get_attribute("textContent").strip()  # Используем textContent

            # Диагностический вывод для каждого региона
            print(f"Проверяем регион: ID={region_id}, Name={region_name}")

            if region_id and region_id.isdigit() and region_name:  # Проверяем данные
                print(f"Добавляем регион: ID={region_id}, Name={region_name}")
                region_data.append({"id": int(region_id), "name": region_name})

        print(f"Найдено регионов: {len(region_data)}")
        return region_data

    except Exception as e:
        print(f"Ошибка при парсинге регионов: {e}")
        return []


def get_courts_for_region(driver, region_id):
    """
    Загружает федеральные суды для региона и возвращает их данные.

    :param driver: Selenium WebDriver.
    :param region_id: ID региона для загрузки федеральных судов.
    :return: Список словарей с данными о федеральных судах.
    """
    url = f"https://sudrf.ru/index.php?id=300&court_subj={region_id}"
    logging.info(f"Загрузка URL: {url}")
    driver.get(url)

    try:
        # Ожидание загрузки кнопки "Найти"
        search_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Найти']"))
        )
        logging.info("Кнопка 'Найти' найдена.")

        # Эмуляция полного нажатия кнопки
        click_button_with_events(driver, search_button)

        # Ожидание изменения DOM
        WebDriverWait(driver, 20).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "ul.search-results > li")) > 0
        )
        logging.info("Данные успешно загружены.")

        # Парсинг результатов
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        courts_data = []
        court_items = soup.select("ul.search-results > li")
        for item in court_items:
            try:
                court_name = item.select_one("a.court-result").text.strip()
                court_info = item.select_one("div.courtInfoCont")

                address_element = court_info.find("b", text="Адрес:")
                address = address_element.next_sibling.strip() if address_element else "Не указано"

                phone_element = court_info.find("b", text="Телефон:")
                phone = phone_element.next_sibling.strip() if phone_element else "Не указано"

                email_element = court_info.find("a", href=lambda href: href and href.startswith("mailto:"))
                email = email_element.text.strip() if email_element else "Не указано"

                url_element = court_info.find("a", href=lambda href: href and href.startswith("http"))
                court_url = url_element["href"].strip() if url_element else "Не указано"

                courts_data.append({
                    "name": court_name,
                    "address": address,
                    "phone": phone,
                    "email": email,
                    "url": court_url,
                })
            except Exception as e:
                logging.error(f"Ошибка при парсинге элемента: {e}")

        return courts_data
    except Exception as e:
        logging.error(f"Не удалось загрузить данные для региона {region_id}: {e}")
        return []


# ---------- Функции для работы с базой данных ----------

def save_regions_to_db(regions: List[Dict[str, str]]):
    """
    Сохраняет список регионов в базу данных SQLite.
    :param regions: Список регионов.
    """
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()
    for region in regions:
        cursor.execute(
            "INSERT OR IGNORE INTO regions (id, name) VALUES (?, ?)", (region["id"], region["name"])
        )
    conn.commit()
    conn.close()


def save_courts_to_db(region_id: str, courts: List[Dict[str, str]], court_type: str = "районный"):
    """
    Сохраняет список судов для региона в базу данных SQLite.
    :param region_id: ID региона.
    :param courts: Список судов.
    :param court_type: Тип суда (районный или мировой).
    """
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()
    for court in courts:
        cursor.execute(
            """
            INSERT INTO courts (region_id, name, address, phone, email, url, court_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (region_id, court["name"], court["address"], court["phone"], court["email"], court["url"], court_type),
        )
    conn.commit()
    conn.close()

from selenium.webdriver.common.action_chains import ActionChains


def get_world_courts_for_region(driver, region_id):
    """
    Загружает мировые суды для региона и возвращает их данные.

    :param driver: Selenium WebDriver.
    :param region_id: ID региона для загрузки мировых судов.
    :return: Список словарей с данными о мировых судах.
    """
    url = f"https://sudrf.ru/index.php?id=300&court_subj={region_id}"
    logging.info(f"Загрузка URL: {url}")
    driver.get(url)

    try:
        # Ожидание загрузки кнопки "Найти"
        search_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Найти']"))
        )
        logging.info("Кнопка 'Найти' найдена.")

        # Эмуляция полного нажатия кнопки
        click_button_with_events(driver, search_button)

        # Ожидание изменения DOM
        WebDriverWait(driver, 20).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "ul.search-results > li")) > 0
        )
        logging.info("Данные успешно загружены.")

        # Парсинг результатов
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        courts_data = []
        court_items = soup.select("ul.search-results > li")
        for item in court_items:
            try:
                court_name = item.select_one("a.court-result").text.strip()
                court_info = item.select_one("div.courtInfoCont")

                address_element = court_info.find("b", text="Адрес:")
                address = address_element.next_sibling.strip() if address_element else "Не указано"

                phone_element = court_info.find("b", text="Телефон:")
                phone = phone_element.next_sibling.strip() if phone_element else "Не указано"

                email_element = court_info.find("a", href=lambda href: href and href.startswith("mailto:"))
                email = email_element.text.strip() if email_element else "Не указано"

                url_element = court_info.find("a", href=lambda href: href and href.startswith("http"))
                court_url = url_element["href"].strip() if url_element else "Не указано"

                courts_data.append({
                    "name": court_name,
                    "address": address,
                    "phone": phone,
                    "email": email,
                    "url": court_url,
                })
            except Exception as e:
                logging.error(f"Ошибка при парсинге элемента: {e}")

        return courts_data
    except Exception as e:
        logging.error(f"Не удалось загрузить данные для региона {region_id}: {e}")
        return []


def click_button_with_events(driver, button):
    """
    Эмулирует полное физическое нажатие на кнопку с использованием событий JavaScript.
    """
    try:
        if not button.is_displayed():
            logging.warning("Кнопка 'Найти' не видима. Прокручиваем страницу.")
            driver.execute_script("arguments[0].scrollIntoView(true);", button)

        # Эмуляция событий мыши
        driver.execute_script("""
            var event = new MouseEvent('mouseover', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);

            event = new MouseEvent('mousedown', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);

            event = new MouseEvent('mouseup', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);

            arguments[0].click();
        """, button)
        logging.info("Кнопка 'Найти' успешно нажата через эмуляцию событий.")
    except Exception as e:
        logging.error(f"Ошибка при эмуляции событий нажатия кнопки: {e}")
        raise

def click_button_with_mouse(driver, button):
    """
    Эмулирует физический клик мышкой по кнопке.
    """
    try:
        if not button.is_displayed():
            logging.warning("Кнопка 'Найти' не видима. Прокручиваем страницу.")
            driver.execute_script("arguments[0].scrollIntoView(true);", button)

        # Попробуем кликнуть физически
        actions = ActionChains(driver)
        actions.move_to_element(button).click().perform()
        logging.info("Кнопка 'Найти' успешно нажата с эмуляцией клика мышкой.")
    except Exception as e:
        logging.error(f"Ошибка при клике мышкой: {e}. Пробуем через JavaScript.")
        driver.execute_script("arguments[0].click();", button)
        logging.info("Кнопка 'Найти' успешно нажата через JavaScript.")



def save_world_courts_to_db(region_id: str, courts: List[Dict[str, str]]):
    """
    Сохраняет список мировых судов для региона в базу данных SQLite.
    :param region_id: ID региона.
    :param courts: Список мировых судов.
    """
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()
    for court in courts:
        cursor.execute(
            """
            INSERT INTO world_courts (region_id, district_name, name, address, phone, email, url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                region_id,
                court.get("district_name", "Не указано"),  # Добавляем район
                court["name"],
                court.get("address", "Не указано"),
                court.get("phone", "Не указано"),
                court.get("email", "Не указано"),
                court.get("url", "Не указано"),
            ),
        )
    conn.commit()
    conn.close()

def add_court_type_to_courts():
    """
    Добавляет поле court_type в таблицу courts, если оно ещё не добавлено.
    """
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()
    cursor.execute("""
        ALTER TABLE courts
        ADD COLUMN court_type TEXT DEFAULT 'районный';
    """)
    conn.commit()
    conn.close()
    print("Поле 'court_type' добавлено в таблицу 'courts'.")

def find_courts_by_region(region_name: str) -> str:
    """
    Поиск судов по названию региона.
    :param region_name: Название региона.
    :return: Текстовый результат.
    """
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name, address, phone, email, url
        FROM courts
        WHERE region_id IN (SELECT id FROM regions WHERE name = ?)
        """,
        (region_name,)
    )
    courts = cursor.fetchall()
    conn.close()

    if not courts:
        return f"Суды для региона '{region_name}' не найдены."

    result = f"Суды в регионе '{region_name}':\n"
    for court in courts:
        result += (
            f"\ud83c\udfdb {court[0]}\n"
            f"\ud83d\udccd Адрес: {court[1]}\n"
            f"\ud83d\udcde Телефон: {court[2]}\n"
            f"\ud83d\udce7 Email: {court[3]}\n"
            f"\ud83c\udf10 Сайт: {court[4]}\n\n"
        )
    return result

def create_world_courts_table():
    """
    Создаёт таблицу world_courts, если она ещё не существует.
    """
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()

    # SQL-запрос для создания таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS world_courts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INTEGER,
            district_name TEXT,
            name TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            url TEXT,
            FOREIGN KEY(region_id) REFERENCES regions(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Таблица world_courts успешно создана (если её не было).")



def find_court_by_address(address_part: str) -> str:
    """
    Ищет суды по части адреса.

    :param address_part: Часть адреса для поиска.
    :return: Список найденных судов в текстовом формате.
    """
    try:
        # Подключение к базе данных
        conn = sqlite3.connect("courts.db")
        cursor = conn.cursor()

        # Поиск судов по адресу
        cursor.execute(
            """
            SELECT name, address, phone, email, url
            FROM courts
            WHERE address LIKE ?
            """,
            (f"%{address_part}%",)
        )
        courts = cursor.fetchall()
        conn.close()

        if not courts:
            return f"Суды, содержащие в адресе '{address_part}', не найдены."

        # Форматирование результата
        result = f"Список судов, содержащих в адресе '{address_part}':\n\n"
        for court in courts:
            result += (
                f"\ud83c\udfdb {court[0]}\n"
                f"\ud83d\udccd Адрес: {court[1]}\n"
                f"\ud83d\udcde Телефон: {court[2]}\n"
                f"\ud83d\udce7 Email: {court[3]}\n"
                f"\ud83c\udf10 Сайт: {court[4]}\n\n"
            )
        return result

    except sqlite3.Error as e:
        return f"Ошибка работы с базой данных: {e}"


# ---------- Основной процесс ----------

def fetch_courts_data():
    progress_file = "progress.log"

    # Читаем этап, на котором остановились
    completed_stage = None
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            completed_stage = f.read().strip()

    logging.info(f"Текущее состояние: {completed_stage}")

    driver = setup_driver(headless=True)
    try:
        # Создаём таблицу для мировых судов
        create_world_courts_table()

        # Загружаем регионы
        regions = []
        if completed_stage != "regions":
            logging.info("Начинается загрузка регионов.")
            regions = get_regions(driver)
            save_regions_to_db(regions)
            logging.info(f"Загрузка регионов завершена. Найдено {len(regions)} регионов.")
            with open(progress_file, "w") as f:
                f.write("regions")
        else:
            # Загружаем регионы из базы, если этап завершён
            conn = sqlite3.connect("courts.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM regions")
            regions = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
            conn.close()

        # Парсинг федеральных судов
        if completed_stage != "federal_courts":
            logging.info("Начинается парсинг федеральных судов.")
            for region in regions:
                logging.info(f"Парсинг федеральных судов для региона: {region['id']} - {region['name']}")
                try:
                    courts = get_courts_for_region(driver, region["id"])
                    save_courts_to_db(region["id"], courts)
                except Exception as e:
                    logging.error(f"Ошибка при обработке региона {region['id']}: {e}")
            logging.info("Парсинг федеральных судов завершён.")
            with open(progress_file, "w") as f:
                f.write("federal_courts")

        # Парсинг мировых судов
        if completed_stage != "world_courts":
            logging.info("Начинается парсинг мировых судов.")
            for region in regions:
                logging.info(f"Парсинг мировых судов для региона: {region['id']} - {region['name']}")
                try:
                    world_courts = get_world_courts_for_region(driver, region["id"])
                    save_world_courts_to_db(region["id"], world_courts)
                except Exception as e:
                    logging.error(f"Ошибка при обработке мировых судов региона {region['id']}: {e}")
            logging.info("Парсинг мировых судов завершён.")
            with open(progress_file, "w") as f:
                f.write("world_courts")
    finally:
        driver.quit()
        if completed_stage == "world_courts":
            logging.info("Парсинг данных завершён.")
            if os.path.exists(progress_file):
                os.remove(progress_file)
