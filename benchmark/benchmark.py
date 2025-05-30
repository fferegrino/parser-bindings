import timeit

N_RUNS = 10

time = timeit.timeit(
    "parser.parse_log_line('[2023-10-27 14:30:05] INFO: User logged in.')",
    number=N_RUNS,
    setup="from rslib import Parser; parser = Parser()",
)
print(f"Rust time:\t{time * 1000:f}ms")

time = timeit.timeit(
    "parser.parse_log_line('[2023-10-27 14:30:05] INFO: User logged in.')",
    number=N_RUNS,
    setup="from pylib import Parser; parser = Parser()",
)
print(f"Python time:\t{time * 1000:f}ms")
