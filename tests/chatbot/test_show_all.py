import contextlib
import io
import unittest

from hw04.chatbot.commands.show_all import show_phone as show_all_contacts


def capture(contacts):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = show_all_contacts(contacts)
    return result, buffer.getvalue()


class TestShowAllContacts(unittest.TestCase):
    def test_prints_every_contact(self):
        _, output = capture({"Alex": "1234567890", "Vasya": "0987654321"})
        self.assertEqual(output, "Alex: 1234567890\nVasya: 0987654321\n")

    def test_prints_a_single_contact(self):
        _, output = capture({"Alex": "1234567890"})
        self.assertEqual(output, "Alex: 1234567890\n")

    def test_empty_contacts_print_a_notice(self):
        _, output = capture({})
        self.assertEqual(output, "No contacts found.\n")

    def test_returns_none(self):
        result, _ = capture({"Alex": "1234567890"})
        self.assertIsNone(result)

    def test_insertion_order_is_preserved(self):
        _, output = capture({"Vasya": "1", "Alex": "2"})
        self.assertEqual(output.splitlines(), ["Vasya: 1", "Alex: 2"])

    def test_contacts_are_not_modified(self):
        contacts = {"Alex": "1234567890"}
        capture(contacts)
        self.assertEqual(contacts, {"Alex": "1234567890"})


if __name__ == "__main__":
    unittest.main()
