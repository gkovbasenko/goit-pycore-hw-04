def show_phone(contacts):
    if (len(contacts) == 0):
        print("No contacts found.")
        return
    for name, phone in contacts.items():
        print(f"{name}: {phone}")