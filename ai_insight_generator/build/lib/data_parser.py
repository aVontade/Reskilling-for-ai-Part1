import os
from typing import List, Dict, Any

def parse_book_from_readme(filepath: str) -> List[Dict[str, Any]]:
    """
    Parses the book content from the README.md file into a structured format.

    Args:
        filepath: The path to the README.md file.

    Returns:
        A list of dictionaries, where each dictionary represents a section
        (e.g., a chapter) with its title, content, and any image placeholders.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file was not found at: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    sections = []

    # Split the book into major H1 sections
    chapters = markdown_text.split('\n# ')
    chapters = [chapters[0]] + ['# ' + c for c in chapters[1:]] # Add back the delimiter

    for chapter_text in chapters:
        if not chapter_text.strip():
            continue

        lines = chapter_text.strip().split('\n')
        title = lines[0].replace('#', '').strip()

        current_section = {
            "title": title,
            "content": "",
            "visualizations": []
        }

        content_lines = []
        for line in lines[1:]:
            if "[Image Placeholder:" in line:
                placeholder_text = line.replace('[Image Placeholder:', '').replace(']', '').strip()
                current_section['visualizations'].append(placeholder_text)
            else:
                content_lines.append(line)

        current_section['content'] = '\n'.join(content_lines).strip()
        sections.append(current_section)

    return sections

if __name__ == '__main__':
    # Example usage:
    # Assumes the script is run from the root of the repository
    readme_path = './README.md'
    try:
        book_data = parse_book_from_readme(readme_path)
        import json
        print(json.dumps(book_data, indent=2))
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
