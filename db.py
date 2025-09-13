import sqlite3

def init_db():
    conn = sqlite3.connect('aerial_gymnastics.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            Text TEXT,
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price TEXT,
            img TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            text TEXT,
            img TEXT DEFAULT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_or_update_row(table, columns, values, row_id=None):
    """ Опис:
    Додає новий рядок або оновлює існуючий у вказаній таблиці.

    Якщо row_id не заданий, створюється новий рядок.
    Якщо row_id заданий, оновлюється існуючий рядок з цим id.

    Параметри:
        table (str): назва таблиці
        columns (list): список назв колонок
        values (list): список значень для вставки/оновлення
        row_id (int, optional): id рядка для оновлення

    """
    
    conn = sqlite3.connect('aerial_gymnastics.db')
    cursor = conn.cursor()

    if row_id:
        # Оновлення існуючого рядка
        set_clause = ', '.join([f"{col}=?" for col in columns])
        sql = f"UPDATE {table} SET {set_clause} WHERE id=?"
        cursor.execute(sql, values + [row_id])
    else:
        # Додавання нового рядка
        placeholders = ', '.join(['?' for _ in columns])
        columns_str = ', '.join(columns)
        sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        cursor.execute(sql, values)

    conn.commit()
    conn.close()

    """Приклад використання:
    - Додавання нового клієнта
    add_or_update_row(
        table='clients',
        columns=['name', 'email', 'phone'],
        values=['Іван Іванов', 'ivan@example.com', '+380123456789']
    )

    - Оновлення email клієнта з id=1
    add_or_update_row(
        table='clients',
        columns=['email'],
        values=['new_email@example.com'],
        row_id=1
    )"""

def delete_row(table, column, value):
    """ Опис та приклад використання:
    Видаляє рядок з таблиці за заданим значенням у вказаній колонці.

    Параметри:
        table (str): назва таблиці
        column (str): назва колонки
        value: значення для видалення

    Приклад використання:
        delete_row('clients', 'id', 1)
        delete_row('clients', 'email', 'ivan@example.com')
    """
    
    conn = sqlite3.connect('aerial_gymnastics.db')
    cursor = conn.cursor()

    # Перевірка, чи існує колонка в таблиці
    cursor.execute(f"PRAGMA table_info({table})")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info]
    if column not in column_names:
        raise ValueError(f"Таблиця '{table}' не містить колонки '{column}'.")

    sql = f"DELETE FROM {table} WHERE {column}=?"
    cursor.execute(sql, (value,))

    conn.commit()
    conn.close()

def fetch_rows(table, columns=None, where=None, params=None):
    """ Опис та приклад використання:
    Універсальна функція для отримання даних з таблиці.

    Параметри:
        table (str): назва таблиці
        columns (list, optional): список колонок для вибірки (None - всі)
        where (str, optional): умова WHERE (без 'WHERE')
        params (tuple/list, optional): параметри для WHERE

    Повертає:
        list of dict: список рядків у вигляді словників

    Приклад використання:
        fetch_rows('clients')
        fetch_rows('clients', columns=['name', 'email'])
        fetch_rows('clients', where='id=?', params=(1,))
    """

    conn = sqlite3.connect('aerial_gymnastics.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    columns_str = ', '.join(columns) if columns else '*'
    sql = f"SELECT {columns_str} FROM {table}"
    if where:
        sql += f" WHERE {where}"

    cursor.execute(sql, params or ())
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return rows
