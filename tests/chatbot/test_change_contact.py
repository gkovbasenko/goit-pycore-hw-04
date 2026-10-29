import unittest

from hw04.chatbot.commands.change_contact import change_contact


class TestChangeContact(unittest.TestCase):
    def test_updates_an_existing_contact(self):
        contacts = {"Alex": "1234567890"}
        self.assertEqual(change_contact(["Alex", "0987654321"], contacts), "Contact updated.")
        self.assertEqual(contacts["Alex"], "0987654321")

    def test_other_contacts_are_untouched(self):
        contacts = {"Alex": "1234567890", "Vasya": "1111111111"}
        change_contact(["Alex", "0987654321"], contacts)
        self.assertEqual(contacts["Vasya"], "1111111111")

    def test_unknown_name_is_reported(self):
        contacts = {"Alex": "1234567890"}
        self.assertEqual(change_contact(["Vasya", "0987654321"], contacts), "Contact not found.")

    def test_unknown_name_is_not_added(self):
        contacts = {"Alex": "1234567890"}
        change_contact(["Vasya", "0987654321"], contacts)
        self.assertNotIn("Vasya", contacts)

    def test_empty_contacts_report_not_found(self):
        self.assertEqual(change_contact(["Alex", "0987654321"], {}), "Contact not found.")

    def test_names_are_case_sensitive(self):
        contacts = {"Alex": "1234567890"}
        self.assertEqual(change_contact(["alex", "0987654321"], contacts), "Contact not found.")

    def test_too_few_arguments_raise_value_error(self):
        with self.assertRaises(ValueError):
            change_contact(["Alex"], {"Alex": "1234567890"})

    def test_too_many_arguments_raise_value_error(self):
        with self.assertRaises(ValueError):
            change_contact(["Alex", "1234567890", "extra"], {})


if __name__ == "__main__":
    unittest.main()
