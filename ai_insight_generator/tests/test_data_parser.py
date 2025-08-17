import pytest
import os
import sys

# Add the project root to the Python path to solve import issues
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_parser import parse_book_from_readme

@pytest.fixture
def sample_readme_file(tmp_path):
    """Creates a temporary README file for testing."""
    # The content is designed to mimic the structure of the actual README.md
    content = """# Reskilling for the AI Economy
How Organizations and Individuals Can Thrive Through Learning, Unlearning, and Relearning

Some introductory text.

# FOREWORD
## The AI Workforce Revolution

Some foreword text.

[Image Placeholder: AI Impact Timeline Graph - showing acceleration of AI adoption from 2020-2030 with key milestones and workforce impact predictions]*

More foreword text.
"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(content, encoding="utf-8")
    return str(readme_path)

def test_parse_book_from_readme_structure(sample_readme_file):
    """Tests that the parser correctly identifies the number of H1 sections."""
    parsed_data = parse_book_from_readme(sample_readme_file)
    assert len(parsed_data) == 2, "Should parse two distinct H1 sections"

def test_parse_book_from_readme_titles(sample_readme_file):
    """Tests that the titles of the sections are correctly extracted."""
    parsed_data = parse_book_from_readme(sample_readme_file)
    assert parsed_data[0]['title'] == 'Reskilling for the AI Economy'
    assert parsed_data[1]['title'] == 'FOREWORD'

def test_parse_book_from_readme_content(sample_readme_file):
    """Tests that the content is correctly aggregated for each section."""
    parsed_data = parse_book_from_readme(sample_readme_file)
    # Test content of the first section
    assert "How Organizations and Individuals" in parsed_data[0]['content']
    assert "Some introductory text." in parsed_data[0]['content']

    # Test content of the second section
    assert "## The AI Workforce Revolution" in parsed_data[1]['content']
    assert "Some foreword text." in parsed_data[1]['content']
    assert "More foreword text." in parsed_data[1]['content']

    # Ensure the placeholder text itself is not in the main content
    assert "[Image Placeholder:" not in parsed_data[1]['content']

def test_parse_book_from_readme_visualizations(sample_readme_file):
    """Tests that visualization placeholders are correctly extracted."""
    parsed_data = parse_book_from_readme(sample_readme_file)
    assert len(parsed_data[0]['visualizations']) == 0, "The first section should have no visualizations"
    assert len(parsed_data[1]['visualizations']) == 1, "The second section should have one visualization"
    expected_viz_text = "AI Impact Timeline Graph - showing acceleration of AI adoption from 2020-2030 with key milestones and workforce impact predictions*"
    assert parsed_data[1]['visualizations'][0] == expected_viz_text

def test_parse_book_from_readme_file_not_found():
    """Tests that a FileNotFoundError is raised for a non-existent file."""
    with pytest.raises(FileNotFoundError):
        parse_book_from_readme("a/path/that/does/not/exist.md")
