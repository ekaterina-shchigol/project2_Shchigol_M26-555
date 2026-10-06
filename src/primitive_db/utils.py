import json
import os


def load_metadata(filepath: str) -> dict:
    """Load database metadata from a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """Save database metadata to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def delete_table_data(table_name: str) -> None:
    """Delete a table data file if it exists."""
    from primitive_db.constants import DATA_DIR

    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
