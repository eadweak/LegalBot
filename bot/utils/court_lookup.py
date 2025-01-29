def find_court_by_address(address: str):
    """Ищет суд в базе данных по адресу."""
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()

    # Поиск суда по адресу
    query = """
    SELECT name, address, phone, email, url
    FROM courts
    WHERE ? LIKE '%' || address || '%'
    LIMIT 1
    """
    cursor.execute(query, (address,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "name": result[0],
            "address": result[1],
            "phone": result[2],
            "email": result[3],
            "url": result[4],
        }
    return None
