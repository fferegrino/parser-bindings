from concurrent.futures import ThreadPoolExecutor
import re
from dataclasses import dataclass
import random
import multiprocessing as mp


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

    ## PI ESTIMATION METHODS

    def estimate_pi(self, num_samples: int) -> float:
        inside_circle = 0
        for _ in range(num_samples):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            distance = x**2 + y**2
            if distance <= 1:
                inside_circle += 1
        return (inside_circle / num_samples) * 4

    def estimate_pi_parallel(
        self, num_samples: int, num_processes: int = None
    ) -> float:
        if num_processes is None:
            num_processes = mp.cpu_count()

        samples_per_process = num_samples // num_processes
        remaining_samples = num_samples % num_processes

        process_samples = [samples_per_process] * num_processes
        if remaining_samples > 0:
            process_samples[-1] += remaining_samples

        total_inside_circle = 0
        with ThreadPoolExecutor(max_workers=num_processes) as executor:
            futures = [
                executor.submit(self._estimate_pi_chunk, samples_per_process)
                for _ in range(num_processes)
            ]
            for future in futures:
                total_inside_circle += future.result()
        pi_estimate_mt = (total_inside_circle / num_samples) * 4
        return pi_estimate_mt

    def _estimate_pi_chunk(self, num_samples: int) -> int:
        """Helper method to estimate pi for a chunk of samples"""
        inside_circle = 0
        for _ in range(num_samples):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            distance = x**2 + y**2
            if distance <= 1:
                inside_circle += 1
        return inside_circle
