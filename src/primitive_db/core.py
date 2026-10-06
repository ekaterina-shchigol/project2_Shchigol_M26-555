from primitive_db.constants import ID_COLUMN, VALID_TYPES


def is_valid_table_name(table_name: str) -> bool:
    """Check whether a table name contains only allowed characters."""
    return bool(table_name) and all(
        char.isascii() and (char.isalnum() or char == "_")
        for char in table_name
    )


def create_table(
    metadata: dict,
    table_name: str,
    columns: list[str],
) -> dict:
    """Create a table description in metadata."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    if not is_valid_table_name(table_name):
        print(f"Некорректное значение: {table_name}. Попробуйте снова.")
        return metadata

    table_columns = {ID_COLUMN: "int"}

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = column.split(":", 1)

        if not column_name or column_type not in VALID_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        if column_name in table_columns:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        table_columns[column_name] = column_type

    metadata[table_name] = table_columns

    columns_text = ", ".join(
        f"{name}:{data_type}"
        for name, data_type in table_columns.items()
    )
    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {columns_text}"
    )

    return metadata


def list_tables(metadata: dict) -> list[str]:
    """Return the names of all existing tables."""
    return list(metadata)


def drop_table(metadata: dict, table_name: str) -> dict:
    """Remove a table description from metadata."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata
