from pyparser import parse_log_line, validate_config


def test_parse_valid_info_log():
    line = "[2023-10-27 14:30:05] INFO: User logged in."
    expected = {
        "timestamp": "2023-10-27 14:30:05",
        "level": "INFO",
        "message": "User logged in.",
    }
    assert parse_log_line(line) == expected


def test_parse_valid_warn_log():
    line = "[2024-01-15 08:00:10] WARN: Disk space low."
    expected = {
        "timestamp": "2024-01-15 08:00:10",
        "level": "WARN",
        "message": "Disk space low.",
    }
    assert parse_log_line(line) == expected


def test_parse_valid_error_log():
    line = "[2025-05-22 09:14:52] ERROR: Database connection failed. Retrying..."
    expected = {
        "timestamp": "2025-05-22 09:14:52",
        "level": "ERROR",
        "message": "Database connection failed. Retrying...",
    }
    assert parse_log_line(line) == expected


def test_parse_invalid_format():
    assert (parse_log_line("Invalid log line")) is None
    assert (parse_log_line("[2023-10-27] INFO: Missing time")) is None
    assert parse_log_line("2023-10-27 14:30:05 INFO: No brackets") is None
    assert (
        parse_log_line("[2023-10-27 14:30:05] DEBUG: Unknown level") is None
    )  # DEBUG is not in regex


def test_parse_empty_line():
    assert parse_log_line("   ") == None
    assert parse_log_line("") == None


def test_validate_valid_config():
    config = """
    # This is a comment
    setting1 = value1
    key_name = another value with spaces
    number = 123
    """
    assert validate_config(config) == True


def test_validate_empty_config():
    assert validate_config("") == True
    assert validate_config("   \n# Only comments") == True


def test_validate_config_with_invalid_line():
    config = """
    setting1 = value1
    invalid line without equals
    key = value
    """
    assert validate_config(config) == False


def test_validate_config_with_empty_key():
    config = """
    = value
    setting = 123
    """
    assert validate_config(config) == False


def test_validate_config_with_only_key_no_value():
    config = """
    my_key =
    """
    assert validate_config(config) == True  # Our current validation allows this


def test_validate_config_with_leading_trailing_spaces():
    config = """
        key1 = valueA
    key2   =   valueB
    """
    assert validate_config(config) == True
