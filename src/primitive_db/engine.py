import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import ID_COLUMN, META_FILE
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    is_valid_value,
    list_tables,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import (
    parse_delete_command,
    parse_insert_command,
    parse_select_command,
    parse_update_command,
)
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help() -> None:
    """Print available commands."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> <столбец2:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись"
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию"
    )
    print(
        "<command> select from <имя_таблицы> "
        "- прочитать все записи"
    )
    print(
        "<command> update <имя_таблицы> set <столбец1> = "
        "<новое_значение1> where <столбец_условия> = "
        "<значение_условия> - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись"
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")


def run() -> None:
    """Run the main database command loop."""
    print_help()

    cache_result = create_cacher()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string("\nВведите команду: ")

        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue

        command = args[0]

        if command == "exit":
            break

        if command == "help":
            print_help()
            continue

        if command == "list_tables":
            for table_name in list_tables(metadata):
                print(f"- {table_name}")
            continue

        if command == "info":
            if len(args) != 2:
                print(
                    f"Некорректное значение: {user_input}. "
                    "Попробуйте снова."
                )
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)
            columns = []

            for column_name, data_type in metadata[table_name].items():
                columns.append(f"{column_name}:{data_type}")

            columns_text = ", ".join(columns)

            print(f"Таблица: {table_name}")
            print(f"Столбцы: {columns_text}")
            print(f"Количество записей: {len(table_data)}")

            continue

        if command == "delete":
            try:
                table_name, where_clause = parse_delete_command(user_input)
            except ValueError:
                print(
                    f"Некорректное значение: {user_input}. "
                    "Попробуйте снова."
                )
                continue

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            where_column = list(where_clause.keys())[0]
            where_value = where_clause[where_column]

            if where_column not in metadata[table_name]:
                print(
                    f"Некорректное значение: {where_column}. "
                    "Попробуйте снова."
                )
                continue

            where_type = metadata[table_name][where_column]

            if not is_valid_value(where_value, where_type):
                print(
                    f"Некорректное значение: {where_value}. "
                    "Попробуйте снова."
                )
                continue

            table_data = load_table_data(table_name)
            matched_records = select(table_data, where_clause)

            if matched_records is None:
                continue

            if not matched_records:
                print("Записи не найдены.")
                continue

            updated_data = delete(table_data, where_clause)

            if updated_data is None:
                continue

            save_table_data(table_name, updated_data)
            cache_result = create_cacher()

            for record in matched_records:
                print(
                    f'Запись с ID={record[ID_COLUMN]} успешно удалена '
                    f'из таблицы "{table_name}".'
                )

            continue

        if command == "update":
            try:
                table_name, set_clause, where_clause = parse_update_command(
                    user_input
                )
            except ValueError:
                print(
                    f"Некорректное значение: {user_input}. "
                    "Попробуйте снова."
                )
                continue

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            set_column = list(set_clause.keys())[0]
            set_value = set_clause[set_column]
            where_column = list(where_clause.keys())[0]
            where_value = where_clause[where_column]

            if set_column not in metadata[table_name]:
                print(
                    f"Некорректное значение: {set_column}. "
                    "Попробуйте снова."
                )
                continue

            if where_column not in metadata[table_name]:
                print(
                    f"Некорректное значение: {where_column}. "
                    "Попробуйте снова."
                )
                continue

            if set_column == ID_COLUMN:
                print("Некорректное значение: ID. Попробуйте снова.")
                continue

            set_type = metadata[table_name][set_column]

            if not is_valid_value(set_value, set_type):
                print(
                    f"Некорректное значение: {set_value}. "
                    "Попробуйте снова."
                )
                continue

            where_type = metadata[table_name][where_column]

            if not is_valid_value(where_value, where_type):
                print(
                    f"Некорректное значение: {where_value}. "
                    "Попробуйте снова."
                )
                continue

            table_data = load_table_data(table_name)
            matched_records = select(table_data, where_clause)

            if matched_records is None:
                continue

            if not matched_records:
                print("Записи не найдены.")
                continue

            updated_data = update(
                table_data,
                set_clause,
                where_clause,
            )

            if updated_data is None:
                continue

            save_table_data(table_name, updated_data)
            cache_result = create_cacher()

            for record in matched_records:
                print(
                    f'Запись с ID={record[ID_COLUMN]} в таблице '
                    f'"{table_name}" успешно обновлена.'
                )

            continue

        if command == "select":
            try:
                table_name, where_clause = parse_select_command(user_input)
            except ValueError:
                print(
                    f"Некорректное значение: {user_input}. "
                    "Попробуйте снова."
                )
                continue

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            if where_clause is not None:
                column_name = list(where_clause.keys())[0]

                if column_name not in metadata[table_name]:
                    print(
                        f"Некорректное значение: {column_name}. "
                        "Попробуйте снова."
                    )
                    continue

            table_data = load_table_data(table_name)
            cache_key = f"{table_name}:{where_clause!r}"

            def get_selected_data():
                return select(table_data, where_clause)

            selected_data = cache_result(cache_key, get_selected_data)

            if selected_data is None:
                continue

            table = PrettyTable()
            table.field_names = list(metadata[table_name].keys())

            for record in selected_data:
                row = []

                for column_name in table.field_names:
                    row.append(record[column_name])

                table.add_row(row)

            print(table)
            continue

        if command == "insert":
            try:
                table_name, values = parse_insert_command(user_input)
            except ValueError:
                print(
                    f"Некорректное значение: {user_input}. "
                    "Попробуйте снова."
                )
                continue

            table_data = load_table_data(table_name)
            old_count = len(table_data)

            updated_data = insert(
                metadata,
                table_name,
                table_data,
                values,
            )

            if updated_data is None:
                continue

            if len(updated_data) == old_count + 1:
                save_table_data(table_name, updated_data)
                cache_result = create_cacher()
                new_id = updated_data[-1][ID_COLUMN]
                print(
                    f'Запись с ID={new_id} успешно добавлена '
                    f'в таблицу "{table_name}".'
                )

            continue

        if command == "create_table":
            if len(args) < 3:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue

            table_name = args[1]
            table_existed = table_name in metadata

            updated_metadata = create_table(
                metadata,
                table_name,
                args[2:],
            )

            if updated_metadata is None:
                continue

            if not table_existed and table_name in updated_metadata:
                save_metadata(META_FILE, updated_metadata)

            continue

        if command == "drop_table":
            if len(args) != 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            updated_metadata = drop_table(metadata, table_name)

            if updated_metadata is None:
                continue

            save_metadata(META_FILE, updated_metadata)
            delete_table_data(table_name)
            cache_result = create_cacher()

            continue

        print(f"Функции {command} нет. Попробуйте снова.")
