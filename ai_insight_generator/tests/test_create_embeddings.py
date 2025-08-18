import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import os
import sys

# Add project root to path for consistent imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the main script we want to test
from src import create_embeddings

@pytest.fixture
def mock_db_chapters():
    """Fixture for sample data returned from the mocked database."""
    return [
        {'id': 1, 'title': 'Chapter 1', 'content': 'This is the first chapter.'},
        {'id': 2, 'title': 'Chapter 2', 'content': 'This is the second chapter.'}
    ]

@patch('src.create_embeddings.get_db_connection')
def test_fetch_chapters_from_db(mock_get_conn, mock_db_chapters):
    """Tests that the database fetch function processes data correctly."""
    # Setup mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = mock_db_chapters

    # Because the function uses its own row_factory, we need to mock that too
    # This is a bit of a quirk of testing code that configures its own connection

    chapters = create_embeddings.fetch_chapters_from_db()

    mock_get_conn.assert_called_once()
    mock_cursor.execute.assert_called_with("SELECT id, title, content FROM chapters ORDER BY id")
    assert len(chapters) == 2
    assert chapters[0]['title'] == 'Chapter 1'

@patch.dict(os.environ, {"PINECONE_API_KEY": "fake-api-key"})
@patch('src.create_embeddings.fetch_chapters_from_db')
@patch('src.create_embeddings.SentenceTransformer')
@patch('src.create_embeddings.Pinecone')
def test_main_pipeline_logic(mock_pinecone, mock_sent_transformer, mock_fetch_chapters, mock_db_chapters):
    """Tests the main embedding pipeline logic with mocked external services."""
    # --- Setup Mocks ---
    mock_fetch_chapters.return_value = mock_db_chapters

    mock_model = MagicMock()
    mock_model.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])
    mock_model.get_sentence_embedding_dimension.return_value = 2
    mock_sent_transformer.return_value = mock_model

    mock_pc_client = MagicMock()
    mock_pinecone.return_value = mock_pc_client
    # Simulate the index not existing initially
    mock_pc_client.list_indexes.return_value.names.return_value = ["some-other-index"]
    mock_index = MagicMock()
    mock_pc_client.Index.return_value = mock_index

    # --- Run the main function ---
    create_embeddings.main()

    # --- Assertions ---
    mock_fetch_chapters.assert_called_once()
    mock_sent_transformer.assert_called_with('all-MiniLM-L6-v2')
    mock_pinecone.assert_called_with(api_key="fake-api-key")

    # Assert that a new index was created
    mock_pc_client.create_index.assert_called_once()

    # Assert that the upsert was called
    mock_index.upsert.assert_called_once()

    # Check the content of the upsert call
    upsert_args = mock_index.upsert.call_args[1]
    assert 'vectors' in upsert_args
    vectors = upsert_args['vectors']
    assert len(vectors) == 2
    assert vectors[0]['id'] == '1'
    assert vectors[1]['metadata']['title'] == 'Chapter 2'
    assert np.array_equal(vectors[0]['values'], [0.1, 0.2])

def test_main_no_api_key(capsys):
    """Tests that the script exits gracefully if the API key is not set."""
    # Temporarily remove the key if it exists from a previous test run
    if "PINECONE_API_KEY" in os.environ:
        del os.environ["PINECONE_API_KEY"]

    create_embeddings.main()
    captured = capsys.readouterr()
    assert "Error: PINECONE_API_KEY environment variable not set" in captured.out

@patch.dict(os.environ, {"PINECONE_API_KEY": "fake-api-key"})
def test_main_no_chapters(capsys, mock_db_chapters):
    """Tests graceful exit when no chapters are in the database."""
    with patch('src.create_embeddings.fetch_chapters_from_db') as mock_fetch:
        mock_fetch.return_value = [] # Simulate empty database
        create_embeddings.main()
        captured = capsys.readouterr()
        assert "No chapters found" in captured.out
