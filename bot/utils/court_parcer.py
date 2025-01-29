from bot.utils.court_guide import get_regions, get_courts_for_region  # Импорт функции
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3

def parse_and_fill_database():
    """Выполняет парсинг данных и заполняет таблицы regions и courts."""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        # Получаем регионы
        regions = get_regions(driver)
        print(f"Найдено регионов: {len(regions)}")

        conn = sqlite3.connect("courts.db")
        cursor = conn.cursor()

        # Сохраняем регионы в таблицу regions
        for region in regions:
            region_id = int(region["id"])
            cursor.execute(
                "INSERT OR IGNORE INTO regions (id, name) VALUES (?, ?)",
                (region_id, region["name"]),
            )

            # Получаем суды для региона
            courts = get_courts_for_region(driver, region_id)
            for court in courts:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO courts (region_id, name, address, phone, email, url)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        region_id,
                        court["name"],
                        court["address"],
                        court["phone"],
                        court["email"],
                        court["url"],
                    ),
                )

        conn.commit()
        conn.close()

    finally:
        driver.quit()
