from pylib import Parser, LogEntry


def test_parse_valid_info_log():
    line = "[2023-10-27 14:30:05] INFO: User logged in."
    expected = LogEntry(
        timestamp="2023-10-27 14:30:05",
        level="INFO",
        message="User logged in.",
    )
    parser = Parser()
    assert parser.parse_log_line(line) == expected


def test_parse_valid_warn_log():
    line = "[2024-01-15 08:00:10] WARN: Disk space low."
    expected = LogEntry(
        timestamp="2024-01-15 08:00:10",
        level="WARN",
        message="Disk space low.",
    )
    parser = Parser()
    assert parser.parse_log_line(line) == expected


def test_parse_valid_error_log():
    line = "[2025-05-22 09:14:52] ERROR: Database connection failed. Retrying..."
    expected = LogEntry(
        timestamp="2025-05-22 09:14:52",
        level="ERROR",
        message="Database connection failed. Retrying...",
    )
    parser = Parser()
    assert parser.parse_log_line(line) == expected


def test_parse_invalid_format():
    parser = Parser()
    assert (parser.parse_log_line("Invalid log line")) is None
    assert (parser.parse_log_line("[2023-10-27] INFO: Missing time")) is None
    assert parser.parse_log_line("2023-10-27 14:30:05 INFO: No brackets") is None
    assert (
        parser.parse_log_line("[2023-10-27 14:30:05] HELLO: Unknown level") is None
    )  # HELLO is not in regex


def test_parse_empty_line():
    parser = Parser()
    assert parser.parse_log_line("   ") == None
    assert parser.parse_log_line("") == None


def test_estimate_pi():
    parser = Parser()
    pi_estimate = parser.estimate_pi(100000)
    assert 3.1 < pi_estimate < 3.16, f"Estimated pi is out of range: {pi_estimate}"


def test_estimate_pi_parallel():
    parser = Parser()
    pi_estimate = parser.estimate_pi_parallel(100000)
    assert 3.1 < pi_estimate < 3.16, f"Estimated pi is out of range: {pi_estimate}"
