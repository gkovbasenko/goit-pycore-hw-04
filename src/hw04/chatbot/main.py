from hw04.chatbot.data import parse_input
from hw04.chatbot.commands.add_contact import add_contact
from hw04.chatbot.commands.change_contact import change_contact
from hw04.chatbot.commands.show_phone import show_phone
from hw04.chatbot.commands.show_all import show_phone as show_all_contacts

COMMANDS = [
    ("hello", "greet the bot"),
    ("add <name> <phone>", "add a new contact"),
    ("change <name> <phone>", "update an existing contact"),
    ("show <name>", "show the phone number of a contact"),
    ("all", "list all contacts"),
    ("close | exit", "quit the assistant"),
]


def print_commands():
    width = max(len(usage) for usage, _ in COMMANDS)
    print("Available commands:")
    for usage, description in COMMANDS:
        print(f"  {usage.ljust(width)}  - {description}")


def main():
    contacts = {}

    print("Welcome to the assistant bot!")
    print_commands()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
                print(change_contact(args, contacts))
        elif command == "show":
            print(show_phone(args, contacts))
        elif command == "all":
            show_all_contacts(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()