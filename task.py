import string
import re


class User:
    all_users = []

    def __init__(self, first=None, last=None, email=None):
        self.firstname = first
        self.lastname = last
        self.email = email
        User.all_users.append(self)


def verify_email(email):
    email_parts = email.split("@")
    if len(email_parts) == 2:
        tail_parts = email_parts[1].split('.')
        if len(tail_parts) == 2:
            return True
    return False


def verity_first(first):
    if first.startswith('-') or first.startswith("'") or first.endswith("-") or first.endswith("'"):
        return False
    if re.search("--", first) or re.search("-'", first) or re.search("'-", first) or re.search("''", first):
        return False
    if len(first) < 2:
        return False
    for char in first:
        if char not in string.ascii_letters and char != "'" and char != "-":
            return False
    return True


def verify_second(second):
    for word in second:
        if not verity_first((word)):
            return False
    return True


def verify(command):
    first, second, email = (None, None, None)

    command_parts = command.split(" ")
    if len(command_parts) < 3:
        return first, second, email

    email = command_parts[-1]
    if not verify_email(email):
        email = "Incorrect email"

    first = command_parts[0]
    if not verity_first(first):
        first = "Incorrect first name"

    second = command_parts[1:-1]
    if not verify_second(second):
        second = "Incorrect last name"
    else:
        second = " ".join(second)
    return first, second, email


def add_students():
    counter = 0
    while True:
        command = input()
        if command == 'back':
            print(f"Total {counter} students have been added.")
            break
        credentials = verify(command)
        j = 0
        for i in range(3):
            if credentials[i] in ("Incorrect first name", "Incorrect last name", "Incorrect email"):
                print(credentials[i])
                break
            if credentials[i] is None:
                print("Incorrect credentials.")
                break
            j += 1
        if j == 3:
            User(*credentials)
            counter += 1
            print("The student has been added.")


def main():
    print("Learning progress tracker")
    while True:
        entry = input()
        if entry == '' or entry.isspace():
            print("No input.")
            continue
        elif entry == 'back':
            print("Enter 'exit' to exit the program.")
            continue
        elif entry == 'exit':
            print('Bye!')
            break
        elif entry == 'add students':
            print("Enter student credentials or 'back' to return:")
            add_students()
        else:
            print("Unknown command!")
            continue


if __name__ == '__main__':
    main()
