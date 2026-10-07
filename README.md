# Primitive DB

Консольное приложение на Python, имитирующее работу примитивной базы данных.

## Установка

Для установки зависимостей выполните в каталоге проекта:

```bash
uv sync

```

## Управление таблицами

Запуск приложения:

```bash
uv run database
```

Доступные команды:

```text
create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...
list_tables
drop_table <имя_таблицы>
help
exit
```

Поддерживаемые типы данных:

```text
int
str
bool
```

Пример:

```text
create_table users name:str age:int is_active:bool
list_tables
drop_table users
```

Столбец `ID:int` добавляется при создании таблицы автоматически.

## CRUD-операции

Для работы с записями таблиц запустите приложение:

```bash
uv run database
```

Доступные команды:

```text
insert into <имя_таблицы> values (<значение1>, <значение2>, ...)
select from <имя_таблицы>
select from <имя_таблицы> where <столбец> = <значение>
update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение>
delete from <имя_таблицы> where <столбец> = <значение>
info <имя_таблицы>
```

Пример работы:

```text
insert into users values ("Anna", 25, true)
select from users
select from users where age = 25
update users set age = 26 where name = "Anna"
delete from users where ID = 1
info users
```

Строковые значения вводятся в кавычках. Числа и логические значения вводятся без кавычек. Логические значения принимаются в любом регистре, например `true`, `True` или `TRUE`.

Столбец `ID:int` создаётся автоматически и не передаётся в команде `insert`.

## Демонстрация работы

[![asciicast](https://asciinema.org/a/bJnrqd2oUNtGN3V3.svg)](https://asciinema.org/a/bJnrqd2oUNtGN3V3)

### Демонстрация CRUD-операций

[![asciicast](https://asciinema.org/a/CEbLEcF8F10BADtT.svg)](https://asciinema.org/a/CEbLEcF8F10BADtT)

## Декораторы и кэширование

`handle_db_errors` выводит понятное сообщение при ошибке операции. Перед `delete` и `drop_table` декоратор `confirm_action` запрашивает подтверждение: `y` выполняет действие, `n` отменяет его. Декоратор `log_time` показывает время работы `insert` и `select`.

Результаты `select` сохраняются в кэше по имени таблицы и условию `where`. Повторный одинаковый запрос берёт результат из кэша. После успешных `insert`, `update`, `delete` и `drop_table` кэш очищается.

## Финальная демонстрация

[Открыть запись полного сценария](https://asciinema.org/a/CMk74euEeACVOJW8)

[![Запись полного сценария](https://asciinema.org/a/CMk74euEeACVOJW8.svg)](https://asciinema.org/a/CMk74euEeACVOJW8)
