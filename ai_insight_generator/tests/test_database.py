import pytest
import sqlite3
import os
import sys

# Add the project root to the Python path to solve import issues
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database import create_tables, insert_book_data, get_db_connection

@pytest.fixture
def db_connection():
    """Fixture to set up an in-memory SQLite database for testing."""
    # Using an in-memory DB for test isolation
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

@pytest.fixture
def sample_data():
    """Fixture to provide sample parsed data."""
    return [
        {
            "title": "Chapter 1",
            "content": "Content for chapter 1.",
            "visualizations": ["Viz 1A", "Viz 1B"]
        },
        {
            "title": "Chapter 2",
            "content": "Content for chapter 2.",
            "visualizations": ["Viz 2A"]
        }
    ]

def test_create_tables(db_connection):
    """Tests that the tables are created correctly."""
    create_tables(db_connection)
    cursor = db_connection.cursor()

    # Check if chapters table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chapters'")
    assert cursor.fetchone() is not None, "chapters table should be created"

    # Check if visualizations table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='visualizations'")
    assert cursor.fetchone() is not None, "visualizations table should be created"

def test_insert_book_data(db_connection, sample_data):
    """Tests that data is inserted into the database correctly."""
    create_tables(db_connection)
    insert_book_data(db_connection, sample_data)

    cursor = db_connection.cursor()

    # Verify chapters table content
    cursor.execute("SELECT * FROM chapters ORDER BY id")
    chapters = cursor.fetchall()
    assert len(chapters) == 2
    assert chapters[0][1] == "Chapter 1"
    assert chapters[1][2] == "Content for chapter 2."

    # Verify visualizations table content
    cursor.execute("SELECT * FROM visualizations")
    visualizations = cursor.fetchall()
    assert len(visualizations) == 3

    # Check a specific visualization to ensure FK is correct
    cursor.execute("""
        SELECT v.description FROM visualizations v
        JOIN chapters c ON v.chapter_id = c.id
        WHERE c.title = ?
        ORDER BY v.description
    """, ("Chapter 1",))
    chapter_1_viz = [row[0] for row in cursor.fetchall()]
    assert chapter_1_viz == ["Viz 1A", "Viz 1B"]
