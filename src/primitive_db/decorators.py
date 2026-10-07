import time


def handle_db_errors(func):
    """Handle errors raised by a database operation."""

    def wrapper(*args, **kwargs):
        """Call the function and report an error if one occurs."""
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        except Exception as error:
            print(f"Произошла непредвиденная ошибка: {error}")

    return wrapper


def confirm_action(action_name):
    """Ask the user to confirm an operation."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if answer != "y":
                print("Действие отменено.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Print the execution time of a function."""

    def wrapper(*args, **kwargs):
        """Call the function and measure its execution time."""
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start

        print(
            f"Функция {func.__name__} выполнилась "
            f"за {elapsed:.3f} секунд"
        )
        return result

    return wrapper


def create_cacher():
    """Create a function that caches results by key."""
    cache = {}

    def cache_result(key, value_func):
        """Return a saved result or calculate and save it."""
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result
        return result

    return cache_result
