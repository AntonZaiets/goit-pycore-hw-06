from collections import UserDict

# base class for record fields
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# contact name. Required field
class Name(Field):
    pass

# phone number with validation (exactly 10 digits)
class Phone(Field):
    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

 # contact record with a name and a list of phones
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # add a new phone to the record
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # remove a phone from the record
    def remove_phone(self, phone):
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    # replace an existing phone with a new one
    def edit_phone(self, old_phone, new_phone):
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.")
        # validate the new number before changing anything
        new = Phone(new_phone)
        self.phones[self.phones.index(found)] = new

    # return the Phone object with the given number, or None
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )

# address book that stores records by contact name
class AddressBook(UserDict):
    # add a record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # return the record with the given name, or None
    def find(self, name):
        return self.data.get(name)

    # delete the record with the given name, if it exists
    def delete(self, name):
        self.data.pop(name, None)


if __name__ == "__main__":
    # create a new address book
    book = AddressBook()

    # create a record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # add John's record to the address book
    book.add_record(john_record)

    # create and add a new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # print all records in the book
    for name, record in book.data.items():
        print(record)

    # find and edit John's phone
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # find a specific phone in John's record
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # delete Jane's record
    book.delete("Jane")