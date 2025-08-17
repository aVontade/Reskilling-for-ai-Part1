import sqlite3
import os
from typing import List, Dict, Any

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'book_data.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn):
    """Creates the necessary database tables if they don't exist."""
    cursor = conn.cursor()

    # Create chapters table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        UNIQUE(title)
    )
    """)

    # Create visualizations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visualizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (chapter_id) REFERENCES chapters (id)
    )
    """)

    conn.commit()
    print("Tables created successfully.")

def insert_book_data(conn, structured_data: List[Dict[str, Any]]):
    """
    Inserts the parsed book data into the database.
    This function is idempotent, using INSERT OR IGNORE.
    """
    cursor = conn.cursor()

    total_viz = 0
    for section in structured_data:
        # Insert chapter and get its ID
        cursor.execute(
            "INSERT OR IGNORE INTO chapters (title, content) VALUES (?, ?)",
            (section['title'], section['content'])
        )

        # It's safer to commit after each chapter to get the lastrowid reliably
        # although for a single-threaded script, it's not strictly necessary.
        conn.commit()

        # Get the ID of the chapter we just inserted or that already existed
        cursor.execute("SELECT id FROM chapters WHERE title = ?", (section['title'],))
        result = cursor.fetchone()
        if result is None:
            print(f"Warning: Could not retrieve ID for chapter: {section['title']}")
            continue
        chapter_id = result['id']

        # Insert visualizations for the chapter
        for viz_desc in section['visualizations']:
            cursor.execute(
                "INSERT INTO visualizations (chapter_id, description) VALUES (?, ?)",
                (chapter_id, viz_desc)
            )
            total_viz += 1

    conn.commit()
    print(f"{len(structured_data)} sections and {total_viz} visualizations processed.")
