import os
import tempfile
import unittest

from hw04.task2.cats import get_cats_info


class TestGetCatsInfo(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._directory.cleanup)

    def write_file(self, content):
        path = os.path.join(self._directory.name, "cats_file.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return path

    def test_returns_one_dictionary_per_record(self):
        path = self.write_file(
            "60b90c1c13067a15887e1ae1,Tayson,3\n"
            "60b90c2413067a15887e1ae2,Vasya,2\n"
            "60b90c2e13067a15887e1ae3,Barsik,1\n"
        )
        self.assertEqual(
            get_cats_info(path),
            [
                {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": 3},
                {"id": "60b90c2413067a15887e1ae2", "name": "Vasya", "age": 2},
                {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": 1},
            ],
        )

    def test_preserves_file_order(self):
        path = self.write_file("2,Vasya,2\n1,Tayson,3\n")
        self.assertEqual([cat["name"] for cat in get_cats_info(path)], ["Vasya", "Tayson"])

    def test_id_stays_a_string_and_age_becomes_an_int(self):
        path = self.write_file("007,Tayson,3\n")
        cat = get_cats_info(path)[0]
        self.assertEqual(cat["id"], "007")
        self.assertIsInstance(cat["age"], int)

    def test_missing_trailing_newline(self):
        path = self.write_file("1,Tayson,3")
        self.assertEqual(get_cats_info(path), [{"id": "1", "name": "Tayson", "age": 3}])

    def test_blank_lines_are_ignored(self):
        path = self.write_file("1,Tayson,3\n\n   \n2,Vasya,2\n")
        self.assertEqual(len(get_cats_info(path)), 2)

    def test_surrounding_whitespace_is_trimmed(self):
        path = self.write_file("  1 , Tayson , 3 \n")
        self.assertEqual(get_cats_info(path), [{"id": "1", "name": "Tayson", "age": 3}])

    def test_empty_file_returns_empty_list(self):
        path = self.write_file("")
        self.assertEqual(get_cats_info(path), [])

    def test_file_of_blank_lines_returns_empty_list(self):
        path = self.write_file("\n\n\n")
        self.assertEqual(get_cats_info(path), [])

    def test_zero_age_is_accepted(self):
        path = self.write_file("1,Tayson,0\n")
        self.assertEqual(get_cats_info(path), [{"id": "1", "name": "Tayson", "age": 0}])

    def test_non_ascii_names_are_read(self):
        path = self.write_file("1,Мурчик,3\n")
        self.assertEqual(get_cats_info(path)[0]["name"], "Мурчик")

    def test_missing_file_raises_file_not_found(self):
        path = os.path.join(self._directory.name, "does_not_exist.txt")
        with self.assertRaises(FileNotFoundError):
            get_cats_info(path)

    def test_too_few_fields_are_rejected(self):
        path = self.write_file("1,Tayson\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(
            str(context.exception),
            "Line 1: expected 'id,name,age' — '1,Tayson'",
        )

    def test_too_many_fields_are_rejected(self):
        path = self.write_file("1,Tayson,3,extra\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(
            str(context.exception),
            "Line 1: expected 'id,name,age' — '1,Tayson,3,extra'",
        )

    def test_empty_id_is_rejected(self):
        path = self.write_file(",Tayson,3\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(str(context.exception), "Line 1: empty id")

    def test_empty_name_is_rejected(self):
        path = self.write_file("1,,3\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(str(context.exception), "Line 1: empty name")

    def test_empty_age_is_rejected(self):
        path = self.write_file("1,Tayson,\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(str(context.exception), "Line 1: empty age")

    def test_non_numeric_age_is_rejected(self):
        path = self.write_file("1,Tayson,three\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(str(context.exception), "Line 1: invalid age 'three'")

    def test_negative_age_is_rejected(self):
        path = self.write_file("1,Tayson,-3\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(str(context.exception), "Line 1: negative age -3")

    def test_error_reports_the_original_line_number(self):
        path = self.write_file("1,Tayson,3\n\n2,Vasya,oops\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertEqual(str(context.exception), "Line 3: invalid age 'oops'")

    def test_age_error_is_not_chained_to_the_int_failure(self):
        path = self.write_file("1,Tayson,oops\n")
        with self.assertRaises(ValueError) as context:
            get_cats_info(path)
        self.assertIsNone(context.exception.__cause__)

    def test_nothing_is_returned_when_a_later_line_is_invalid(self):
        path = self.write_file("1,Tayson,3\n2,Vasya,oops\n")
        with self.assertRaises(ValueError):
            get_cats_info(path)


if __name__ == "__main__":
    unittest.main()
