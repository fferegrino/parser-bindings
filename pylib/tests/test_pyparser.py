from pylib import parse_log_line


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
        parse_log_line("[2023-10-27 14:30:05] HELLO: Unknown level") is None
    )  # HELLO is not in regex


def test_parse_empty_line():
    assert parse_log_line("   ") == None
    assert parse_log_line("") == None
