def find_courts_by_region(region_name):
    """Ищет суды по названию региона."""
    conn = sqlite3.connect("db/courts.db")
    cursor = conn.cursor()

    # Ищем регион
    cursor.execute("SELECT id FROM regions WHERE name = ?", (region_name,))
    region = cursor.fetchone()
    if not region:
        conn.close()
        return f"Регион '{region_name}' не найден."

    # Ищем суды в регионе
    region_id = region[0]
    cursor.execute("SELECT name, address, phone FROM courts WHERE region_id = ?", (region_id,))
    courts = cursor.fetchall()
    conn.close()

    if not courts:
        return f"Суды в регионе '{region_name}' не найдены."

    result = f"Суды в регионе '{region_name}':\n"
    for court in courts:
        result += f"• {court[0]}, адрес: {court[1]}, телефон: {court[2]}\n"
    return result


def find_court_by_address(address_part):
    """Ищет суд по частичному адресу."""
    conn = sqlite3.connect("db/courts.db")
    cursor = conn.cursor()

    # Ищем суды по адресу
    cursor.execute("SELECT name, address, phone FROM courts WHERE address LIKE ?", (f"%{address_part}%",))
    courts = cursor.fetchall()
    conn.close()

    if not courts:
        return f"Суды по адресу '{address_part}' не найдены."

    result = f"Суды, найденные по адресу '{address_part}':\n"
    for court in courts:
        result += f"• {court[0]}, адрес: {court[1]}, телефон: {court[2]}\n"
    return result
