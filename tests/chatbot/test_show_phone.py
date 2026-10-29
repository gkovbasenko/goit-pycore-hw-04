import unittest

from hw04.chatbot.commands.show_phone import show_phone


class TestShowPhone(unittest.TestCase):
    def test_returns_the_phone_of_a_known_contact(self):
        self.assertEqual(show_phone(["Alex"], {"Alex": "1234567890"}), "1234567890")

    def test_picks_the_right_contact(self):
        contacts = {"Alex": "1234567890", "Vasya": "0987654321"}
        self.assertEqual(show_phone(["Vasya"], contacts), "0987654321")

    def test_unknown_name_is_reported(self):
        self.assertEqual(show_phone(["Vasya"], {"Alex": "1234567890"}), "Contact not found.")

    def test_empty_contacts_report_not_found(self):
        self.assertEqual(show_phone(["Alex"], {}), "Contact not found.")

    def test_names_are_case_sensitive(self):
        self.assertEqual(show_phone(["alex"], {"Alex": "1234567890"}), "Contact not found.")

    def test_contacts_are_not_modified(self):
        contacts = {"Alex": "1234567890"}
        show_phone(["Alex"], contacts)
        self.assertEqual(contacts, {"Alex": "1234567890"})

    def test_missing_argument_raises_value_error(self):
        with self.assertRaises(ValueError):
            show_phone([], {})

    def test_too_many_arguments_raise_value_error(self):
        with self.assertRaises(ValueError):
            show_phone(["Alex", "extra"], {"Alex": "1234567890"})


if __name__ == "__main__":
    unittest.main()
