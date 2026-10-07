import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import META_FILE
from primitive_db.core import create_table, drop_table, insert, list_tables, select
from primitive_db.parser import parse_insert_command, parse_select_command
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
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")


def run() -> None:
    """Run the main database command loop."""
    print_help()

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
            selected_data = select(table_data, where_clause)

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

            if len(updated_data) == old_count + 1:
                save_table_data(table_name, updated_data)
                new_id = updated_data[-1]["ID"]
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

            if not table_existed and table_name in updated_metadata:
                save_metadata(META_FILE, updated_metadata)

            continue

        if command == "drop_table":
            if len(args) != 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue

            table_name = args[1]
            table_existed = table_name in metadata
            updated_metadata = drop_table(metadata, table_name)

            if table_existed:
                save_metadata(META_FILE, updated_metadata)
                delete_table_data(table_name)

            continue

        print(f"Функции {command} нет. Попробуйте снова.")
