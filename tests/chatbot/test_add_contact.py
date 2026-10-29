import unittest

from hw04.chatbot.commands.add_contact import add_contact


class TestAddContact(unittest.TestCase):
    def test_adds_a_new_contact(self):
        contacts = {}
        self.assertEqual(add_contact(["Alex", "1234567890"], contacts), "Contact added.")
        self.assertEqual(contacts, {"Alex": "1234567890"})

    def test_adds_to_an_existing_dictionary(self):
        contacts = {"Alex": "1234567890"}
        add_contact(["Vasya", "0987654321"], contacts)
        self.assertEqual(contacts, {"Alex": "1234567890", "Vasya": "0987654321"})

    def test_duplicate_name_is_rejected(self):
        contacts = {"Alex": "1234567890"}
        self.assertEqual(add_contact(["Alex", "0000000000"], contacts), "Contact already exists.")

    def test_duplicate_name_leaves_the_phone_untouched(self):
        contacts = {"Alex": "1234567890"}
        add_contact(["Alex", "0000000000"], contacts)
        self.assertEqual(contacts["Alex"], "1234567890")

    def test_names_are_case_sensitive(self):
        contacts = {"Alex": "1234567890"}
        self.assertEqual(add_contact(["alex", "0987654321"], contacts), "Contact added.")
        self.assertEqual(len(contacts), 2)

    def test_too_few_arguments_raise_value_error(self):
        with self.assertRaises(ValueError):
            add_contact(["Alex"], {})

    def test_too_many_arguments_raise_value_error(self):
        with self.assertRaises(ValueError):
            add_contact(["Alex", "1234567890", "extra"], {})


if __name__ == "__main__":
    unittest.main()
