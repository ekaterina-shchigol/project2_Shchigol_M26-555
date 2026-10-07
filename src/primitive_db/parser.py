import shlex


def parse_value(value_text: str):
    """Convert a text value to a Python value."""
    value_text = value_text.strip()

    if (
        len(value_text) >= 2
        and value_text[0] == '"'
        and value_text[-1] == '"'
    ):
        return value_text[1:-1]

    if value_text.lower() == "true":
        return True

    if value_text.lower() == "false":
        return False

    try:
        return int(value_text)
    except ValueError:
        raise ValueError(value_text)


def parse_values(values_text: str) -> list:
    """Parse comma-separated values."""
    lexer = shlex.shlex(values_text, posix=False)
    lexer.whitespace = ","
    lexer.whitespace_split = True
    lexer.commenters = ""

    raw_values = list(lexer)
    values = []

    for raw_value in raw_values:
        values.append(parse_value(raw_value))

    return values


def parse_insert_command(user_input: str):
    """Parse an insert command and return table name and values."""
    prefix = "insert into "

    if not user_input.startswith(prefix):
        raise ValueError(user_input)

    command_part = user_input[len(prefix):]
    parts = command_part.split(" values ", 1)

    if len(parts) != 2:
        raise ValueError(user_input)

    table_name = parts[0].strip()
    values_text = parts[1].strip()

    if not table_name or " " in table_name:
        raise ValueError(user_input)

    for char in table_name:
        if not char.isascii():
            raise ValueError(user_input)

        if not (char.isalnum() or char == "_"):
            raise ValueError(user_input)

    if not values_text.startswith("(") or not values_text.endswith(")"):
        raise ValueError(user_input)

    values_text = values_text[1:-1]
    values = parse_values(values_text)

    return table_name, values


def parse_select_command(user_input: str):
    """Parse a select command."""
    args = shlex.split(user_input, posix=False)

    if len(args) == 3:
        if args[0] != "select" or args[1] != "from":
            raise ValueError(user_input)

        return args[2], None

    if len(args) == 7:
        if (
            args[0] != "select"
            or args[1] != "from"
            or args[3] != "where"
            or args[5] != "="
        ):
            raise ValueError(user_input)

        table_name = args[2]
        column_name = args[4]
        value = parse_value(args[6])

        return table_name, {column_name: value}

    raise ValueError(user_input)


def parse_update_command(user_input: str):
    """Parse an update command."""
    args = shlex.split(user_input, posix=False)

    if len(args) != 10:
        raise ValueError(user_input)

    if (
        args[0] != "update"
        or args[2] != "set"
        or args[4] != "="
        or args[6] != "where"
        or args[8] != "="
    ):
        raise ValueError(user_input)

    table_name = args[1]

    set_column = args[3]
    set_value = parse_value(args[5])

    where_column = args[7]
    where_value = parse_value(args[9])

    set_clause = {set_column: set_value}
    where_clause = {where_column: where_value}

    return table_name, set_clause, where_clause


def parse_delete_command(user_input: str):
    """Parse a delete command."""
    args = shlex.split(user_input, posix=False)

    if len(args) != 7:
        raise ValueError(user_input)

    if (
        args[0] != "delete"
        or args[1] != "from"
        or args[3] != "where"
        or args[5] != "="
    ):
        raise ValueError(user_input)

    table_name = args[2]
    column_name = args[4]
    value = parse_value(args[6])

    where_clause = {column_name: value}

    return table_name, where_clause
