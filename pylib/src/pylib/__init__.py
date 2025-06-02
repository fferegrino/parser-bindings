import re
from dataclasses import dataclass
import random

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

    def estimate_pi(self, num_samples: int) -> float:
        inside_circle = 0
        for _ in range(num_samples):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            distance = x**2 + y**2
            if distance <= 1:
                inside_circle += 1
        return (inside_circle / num_samples) * 4
