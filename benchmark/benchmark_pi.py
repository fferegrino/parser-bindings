import timeit

N_RUNS = 100
N_SAMPLES = 100000

time = timeit.timeit(
    f"parser.estimate_pi({N_SAMPLES})",
    number=N_RUNS,
    setup="from rslib import Parser; parser = Parser()",
)
print(f"Rust time:\t{time * 1000:f}ms")

time = timeit.timeit(
    f"parser.estimate_pi({N_SAMPLES})",
    number=N_RUNS,
    setup="from pylib import Parser; parser = Parser()",
)
print(f"Python time:\t{time * 1000:f}ms")
