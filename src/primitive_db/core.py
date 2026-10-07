from primitive_db.constants import ID_COLUMN, VALID_TYPES


def is_valid_table_name(table_name: str) -> bool:
    """Check whether a table name contains only allowed characters."""
    if not table_name:
        return False

    for char in table_name:
        if not char.isascii():
            return False

        if not (char.isalnum() or char == "_"):
            return False

    return True


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

    columns_parts = []

    for name, data_type in table_columns.items():
        columns_parts.append(f"{name}:{data_type}")

    columns_text = ", ".join(columns_parts)
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


def is_valid_value(value, data_type: str) -> bool:
    """Check whether a value matches the declared column type."""
    if data_type == "int":
        return type(value) is int

    if data_type == "str":
        return type(value) is str

    if data_type == "bool":
        return type(value) is bool

    return False


def insert(
    metadata: dict,
    table_name: str,
    table_data: list,
    values: list,
) -> list:
    """Add a new record to a table and return updated table data."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = list(metadata[table_name].items())[1:]

    if len(values) != len(columns):
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return table_data

    for value, (_, data_type) in zip(values, columns):
        if not is_valid_value(value, data_type):
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return table_data

    new_id = 1

    for record in table_data:
        if record["ID"] >= new_id:
            new_id = record["ID"] + 1

    new_record = {"ID": new_id}

    for (column_name, _), value in zip(columns, values):
        new_record[column_name] = value

    updated_data = table_data.copy()
    updated_data.append(new_record)

    return updated_data


def select(table_data: list, where_clause=None) -> list:
    """Return all records or records matching a condition."""
    if where_clause is None:
        return table_data

    column_name = list(where_clause.keys())[0]
    value = where_clause[column_name]
    result = []

    for record in table_data:
        if record[column_name] == value:
            result.append(record)

    return result
