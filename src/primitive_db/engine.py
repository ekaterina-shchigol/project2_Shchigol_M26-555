import prompt


def print_help() -> None:
    """Print available commands."""
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def welcome() -> None:
    """Run the first interactive command loop."""
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print_help()

    while True:
        command = prompt.string("Введите команду: ")

        if command == "exit":
            break

        if command == "help":
            print_help()
            continue

        print(f"Функции {command} нет. Попробуйте снова.")
