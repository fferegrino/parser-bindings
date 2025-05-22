import re


def parse_log_line(line: str) -> dict | None:
    match = re.match(
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|WARN|ERROR|DEBUG): (.*)", line
    )
    if match:
        timestamp, level, message = match.groups()
        return {"timestamp": timestamp, "level": level, "message": message}
    return None
