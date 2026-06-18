import sqlite3


def get_conn():
    return sqlite3.connect("chat.db")


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        role TEXT,
        text TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_chat(title):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (title) VALUES (?)",
        (title,)
    )

    conn.commit()
    chat_id = cursor.lastrowid
    conn.close()

    return chat_id


def get_chats():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM chats ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": row[0], "title": row[1]}
        for row in rows
    ]


def delete_chat(chat_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))

    conn.commit()
    conn.close()


def add_message(chat_id, role, text):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (chat_id, role, text) VALUES (?, ?, ?)",
        (chat_id, role, text)
    )

    conn.commit()
    conn.close()


def get_messages(chat_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, text FROM messages WHERE chat_id = ? ORDER BY id ASC",
        (chat_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"role": row[0], "text": row[1]}
        for row in rows
    ]