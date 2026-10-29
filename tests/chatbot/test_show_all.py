import unittest

from hw04.chatbot.commands.show_all import show_all


class TestShowAll(unittest.TestCase):
    def test_returns_every_contact(self):
        contacts = {"Alex": "1234567890", "Vasya": "0987654321"}
        self.assertEqual(show_all(contacts), "Alex: 1234567890\nVasya: 0987654321")

    def test_returns_a_single_contact(self):
        self.assertEqual(show_all({"Alex": "1234567890"}), "Alex: 1234567890")

    def test_empty_contacts_return_a_notice(self):
        self.assertEqual(show_all({}), "No contacts found.")

    def test_contacts_are_sorted_by_name(self):
        contacts = {"Vasya": "1", "Alex": "2", "Barsik": "3"}
        self.assertEqual(show_all(contacts).splitlines(), ["Alex: 2", "Barsik: 3", "Vasya: 1"])

    def test_result_has_no_trailing_newline(self):
        self.assertFalse(show_all({"Alex": "1234567890"}).endswith("\n"))

    def test_contacts_are_not_modified(self):
        contacts = {"Alex": "1234567890"}
        show_all(contacts)
        self.assertEqual(contacts, {"Alex": "1234567890"})


if __name__ == "__main__":
    unittest.main()
