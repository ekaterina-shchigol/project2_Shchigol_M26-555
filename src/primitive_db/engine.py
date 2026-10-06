import shlex

import prompt

from primitive_db.constants import META_FILE
from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    save_metadata,
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
