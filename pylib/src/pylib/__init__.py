import re
from dataclasses import dataclass

PATTERN = re.compile(
    r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|WARN|ERROR|DEBUG): (.*)"
)


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str


class Parser:
    def __init__(self):
        self.pattern = re.compile(
            r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|WARN|ERROR|DEBUG): (.*)"
        )

    def parse_log_line(self, line: str) -> LogEntry | None:
        match = self.pattern.match(line)
        if match:
            timestamp, level, message = match.groups()
            return LogEntry(timestamp, level, message)
        return None

    def parse_log_file(self, file_path: str) -> list[LogEntry]:
        with open(file_path, "r") as file:
            return [self.parse_log_line(line) for line in file]

    def parse_log_lines_no_return(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            for line in file:
                value = self.parse_log_line(line)
