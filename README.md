# Primitive DB

Консольное приложение на Python, имитирующее работу примитивной базы данных.

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
