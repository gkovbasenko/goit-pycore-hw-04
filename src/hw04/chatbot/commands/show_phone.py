def show_phone(args, contacts):
    name, = args
    if name not in contacts:
        return "Contact not found."
    return contacts[name]