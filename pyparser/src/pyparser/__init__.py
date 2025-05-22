import re


def parse_log_line(line: str) -> dict | None:
    match = re.match(
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|WARN|ERROR): (.*)", line
    )
    if match:
        timestamp, level, message = match.groups()
        return {"timestamp": timestamp, "level": level, "message": message}
    return None


def validate_config(config_str: str) -> bool:
    lines = config_str.split("\n")
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if "=" not in line:
            print(f"Invalid config line: {line}")
            return False
        key, value = line.split("=", 1)
        if not key.strip():
            print(f"Empty key in line: {line}")
            return False
        # Add more specific validation rules here
    return True
