"""Headless unit and stress tests for the Python calculator's arithmetic core."""

import math
import unittest

from calculator import calculate, format_number


class CalculatorTests(unittest.TestCase):
    def test_supported_operations(self):
        cases = (
            (7, "+", 5, 12),
            (9, "-", 4, 5),
            (6, "*", 7, 42),
            (8, "/", 2, 4),
            (9, "/", 2, 4.5),
        )
        for left, operator, right, expected in cases:
            with self.subTest(left=left, operator=operator, right=right):
                self.assertEqual(calculate(left, operator, right), expected)

    def test_rejects_bad_inputs_and_operations(self):
        cases = (
            ((1, "/", 0), ZeroDivisionError),
            ((math.inf, "+", 1), ValueError),
            ((1, "?", 2), ValueError),
            ((1e308, "*", 1e308), OverflowError),
        )
        for arguments, expected_error in cases:
            with self.subTest(arguments=arguments):
                with self.assertRaises(expected_error):
                    calculate(*arguments)

    def test_formats_results(self):
        self.assertEqual(format_number(8.0), "8")
        self.assertEqual(format_number(4.5), "4.5")
        self.assertEqual(format_number(0.1 + 0.2), "0.3")

    def test_stress_10000_calls_per_operator(self):
        """Repeat every operation enough times to catch recurring regressions."""
        loops_per_operator = 10_000
        cases = ((7, "+", 5, 12), (9, "-", 4, 5), (6, "*", 7, 42), (8, "/", 2, 4))
        for left, operator, right, expected in cases:
            for _ in range(loops_per_operator):
                self.assertEqual(calculate(left, operator, right), expected)


if __name__ == "__main__":
    unittest.main()
