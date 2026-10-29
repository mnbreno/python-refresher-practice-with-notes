"""Run headless tests and record reproducible arithmetic timing data."""

import argparse
import csv
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "test-results"

sys.path.insert(0, str(ROOT))
from calculator import calculate  # noqa: E402


def run_tests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def collect_measurements(iterations_per_operator: int) -> list[dict[str, object]]:
    cases = ((7, "+", 5, 12), (9, "-", 4, 5), (6, "*", 7, 42), (8, "/", 2, 4))
    measurements = []
    for left, operator, right, expected in cases:
        start = time.perf_counter()
        for _ in range(iterations_per_operator):
            result = calculate(left, operator, right)
            if result != expected:
                raise AssertionError(f"{left} {operator} {right}: got {result}, expected {expected}")
        elapsed = time.perf_counter() - start
        measurements.append({
            "operation": operator,
            "iterations": iterations_per_operator,
            "elapsed_seconds": f"{elapsed:.9f}",
            "operations_per_second": f"{iterations_per_operator / elapsed:.2f}",
        })
    return measurements


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=10_000,
                        help="repetitions per operator (minimum 10,000; default 10,000)")
    arguments = parser.parse_args()
    if arguments.iterations < 10_000:
        parser.error("--iterations must be at least 10000")

    if not run_tests():
        return 1

    measurements = collect_measurements(arguments.iterations)
    RESULTS_DIR.mkdir(exist_ok=True)
    result_file = RESULTS_DIR / "python-benchmark.csv"
    with result_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=measurements[0].keys())
        writer.writeheader()
        writer.writerows(measurements)

    total = sum(int(row["iterations"]) for row in measurements)
    print(f"\nMeasured {total:,} calculations; results saved to {result_file}")
    for row in measurements:
        print(f"{row['operation']}: {row['elapsed_seconds']} s, {row['operations_per_second']} ops/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
