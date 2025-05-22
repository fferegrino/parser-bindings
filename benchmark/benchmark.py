import timeit

N_RUNS = 1000

time = timeit.timeit(
    "parse_log_line_rust('[2023-10-27 14:30:05] INFO: User logged in.')",
    number=N_RUNS,
    setup="from rslib import parse_log_line as parse_log_line_rust",
)
print(f"Rust time:\t{time * 1000:f}ms")

time = timeit.timeit(
    "parse_log_line_py('[2023-10-27 14:30:05] INFO: User logged in.')",
    number=N_RUNS,
    setup="from pylib import parse_log_line as parse_log_line_py",
)
print(f"Python time:\t{time * 1000:f}ms")
