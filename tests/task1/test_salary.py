import os
import tempfile
import unittest

from hw04.task1.salary import calculate_average, total_salary


class SalaryFileTestCase(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._directory.cleanup)

    def write_file(self, content):
        path = os.path.join(self._directory.name, "salary_file.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return path


class TestCalculateAverage(SalaryFileTestCase):
    def test_divides_total_by_count(self):
        self.assertEqual(calculate_average(6000, 3), 2000)

    def test_zero_count_returns_zero(self):
        self.assertEqual(calculate_average(0, 0), 0)

    def test_result_is_a_float_when_not_divisible(self):
        self.assertAlmostEqual(calculate_average(10, 3), 10 / 3)


class TestTotalSalary(SalaryFileTestCase):
    def test_returns_total_and_average(self):
        path = self.write_file("Alex Korp,3000\nNikita Borisenko,2000\nSitarama Raju,1000\n")
        self.assertEqual(total_salary(path), (6000, 2000))

    def test_single_record(self):
        path = self.write_file("Alex Korp,3000\n")
        self.assertEqual(total_salary(path), (3000, 3000))

    def test_missing_trailing_newline(self):
        path = self.write_file("Alex Korp,3000\nNikita Borisenko,2000")
        self.assertEqual(total_salary(path), (5000, 2500))

    def test_blank_lines_are_ignored(self):
        path = self.write_file("Alex Korp,3000\n\n   \nNikita Borisenko,2000\n")
        self.assertEqual(total_salary(path), (5000, 2500))

    def test_surrounding_whitespace_is_trimmed(self):
        path = self.write_file("  Alex Korp , 3000 \n")
        self.assertEqual(total_salary(path), (3000, 3000))

    def test_name_containing_a_comma_is_rejected(self):
        path = self.write_file("Raju, Jr.,1000\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(
            str(context.exception),
            "Line 1: expected 'name,salary' — 'Raju, Jr.,1000'",
        )

    def test_empty_file_returns_zeros(self):
        path = self.write_file("")
        self.assertEqual(total_salary(path), (0, 0))

    def test_file_of_blank_lines_returns_zeros(self):
        path = self.write_file("\n\n\n")
        self.assertEqual(total_salary(path), (0, 0))

    def test_zero_salary_is_accepted(self):
        path = self.write_file("Alex Korp,0\n")
        self.assertEqual(total_salary(path), (0, 0))

    def test_non_ascii_names_are_read(self):
        path = self.write_file("Олександр Корп,3000\n")
        self.assertEqual(total_salary(path), (3000, 3000))

    def test_missing_file_raises_file_not_found(self):
        path = os.path.join(self._directory.name, "does_not_exist.txt")
        with self.assertRaises(FileNotFoundError):
            total_salary(path)

    def test_line_without_a_comma_is_rejected(self):
        path = self.write_file("Alex Korp 3000\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(
            str(context.exception),
            "Line 1: expected 'name,salary' — 'Alex Korp 3000'",
        )

    def test_empty_name_is_rejected(self):
        path = self.write_file(",3000\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(str(context.exception), "Line 1: empty name")

    def test_non_numeric_salary_is_rejected(self):
        path = self.write_file("Alex Korp,three thousand\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(
            str(context.exception),
            "Line 1: invalid salary 'three thousand'",
        )

    def test_empty_salary_is_rejected(self):
        path = self.write_file("Alex Korp,\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(str(context.exception), "Line 1: invalid salary ''")

    def test_negative_salary_is_rejected(self):
        path = self.write_file("Alex Korp,-500\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(str(context.exception), "Line 1: negative salary -500")

    def test_error_reports_the_original_line_number(self):
        path = self.write_file("Alex Korp,3000\n\nNikita Borisenko,oops\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertEqual(str(context.exception), "Line 3: invalid salary 'oops'")

    def test_salary_error_is_not_chained_to_the_int_failure(self):
        path = self.write_file("Alex Korp,oops\n")
        with self.assertRaises(ValueError) as context:
            total_salary(path)
        self.assertIsNone(context.exception.__cause__)


if __name__ == "__main__":
    unittest.main()
