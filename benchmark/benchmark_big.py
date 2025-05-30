import timeit

N_RUNS = 100
N_RECORDS = 10000

records = [f"[2023-10-27 14:30:05] INFO: User logged in." for _ in range(N_RECORDS)]

with open("log.txt", "w") as f:
    for record in records:
        f.write(record + "\n")

time = timeit.timeit(
    "parser.parse_log_lines_no_return('log.txt')",
    number=N_RUNS,
    setup="from rslib import Parser; parser = Parser()",
)
print(f"Rust time:\t{time * 1000:f}ms")

time = timeit.timeit(
    "parser.parse_log_lines_no_return('log.txt')",
    number=N_RUNS,
    setup="from pylib import Parser; parser = Parser()",
)
print(f"Python time:\t{time * 1000:f}ms")
