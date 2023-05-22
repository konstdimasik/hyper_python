import string
import re


class User:
    all_users = []
    all_emails = set()
    ID = 10000

    def __init__(self, first=None, last=None, email=None):
        self.id = User.ID
        self.firstname = first
        self.lastname = last
        self.email = email
        self.python = 0
        self.dsa = 0
        self.database = 0
        self.flask = 0

        User.ID += 1
        User.all_emails.add(self.email)
        User.all_users.append(self)

    def print_user(self):
        print(f"{self.id} points: Python={self.python}; DSA={self.dsa}; Databases={self.database}; Flask={self.flask}")

    def update_points(self, one, two, three, four):
        self.python += one
        self.dsa += two
        self.database += three
        self.flask += four


def find_user_by_id(some_id):
    for user in User.all_users:
        if user.id == some_id:
            return user
    return None


def verify_email(email):
    email_parts = email.split("@")
    if len(email_parts) != 2:
        return False
    tail_parts = email_parts[1].split('.')
    if len(tail_parts) != 2:
        return False
    return True


def verify_email_uniqueness(email):
    return email in User.all_emails


def verity_name(first):
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


def verify_lastname(second):
    for word in second:
        if not verity_name(word):
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
    if not verity_name(first):
        first = "Incorrect first name"

    second = command_parts[1:-1]
    if not verify_lastname(second):
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
        if verify_email_uniqueness(credentials[-1]):
            print("This email is already taken.")
            continue
        if j == 3:
            User(*credentials)
            counter += 1
            print("The student has been added.")


def add_points():
    while True:
        entry_points = input()
        if entry_points == "back":
            break
        id_vs_points = entry_points.split(" ")
        try:
            user_id = int(id_vs_points[0])
            user_by_id = find_user_by_id(user_id)
        except ValueError:
            print(f"No student is found for id={id_vs_points[0]}.")
            continue
        if user_by_id is None:
            print(f"No student is found for id={id_vs_points[0]}.")
            continue
        points = id_vs_points[1:]
        if len(points) != 4:
            print("Incorrect points format.")
            continue
        try:
            points = list(map(int, points))
        except ValueError:
            print("Incorrect points format.")
            continue
        points_check = True
        for point in points:
            if point < 0:
                print("Incorrect points format.")
                points_check = False
        if points_check:
            user_by_id.update_points(*points)
            print("Points updated.")


def find():
    while True:
        entry_id = input()
        if entry_id == "00000":
            print(f"No student is found for id={entry_id}.")
            continue
        if entry_id == "back":
            break
        try:
            user_id = int(entry_id)
            user_by_id = find_user_by_id(user_id)
        except ValueError:
            print(f"No student is found for id={entry_id}.")
            continue
        if user_by_id is None:
            print(f"No student is found for id={user_id}.")
            continue
        user_by_id.print_user()


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
        elif entry == "list":
            if len(User.all_users) == 0:
                print("No students found.")
                continue
            else:
                print("Students:")
            for student in User.all_users:
                print(f"{student.id}")
        elif entry == "add points":
            print("Enter an id and points or 'back' to return:")
            add_points()
        elif entry == "find":
            print("Enter an id or 'back' to return:")
            find()
        else:
            print("Unknown command!")
            continue


if __name__ == '__main__':
    main()
