import string
import re


class Student:
    all_students = []
    all_emails = set()
    ID = 10000

    def __init__(self, first=None, last=None, email=None):
        self.id = Student.ID
        self.firstname = first
        self.lastname = last
        self.email = email
        self.python = 0
        self.dsa = 0
        self.database = 0
        self.flask = 0

        Student.ID += 1
        Student.all_emails.add(self.email)
        Student.all_students.append(self)

    def print_student(self):
        print(f"{self.id} points: Python={self.python}; DSA={self.dsa}; Databases={self.database}; Flask={self.flask}")

    def update_points(self, one, two, three, four):
        self.python += one
        self.dsa += two
        self.database += three
        self.flask += four


class WrongNameError(Exception):
    def __str__(self):
        return "Incorrect first name"


class WrongLastNameError(Exception):
    def __str__(self):
        return "Incorrect last name"


class WrongEmailError(Exception):
    def __str__(self):
        return "Incorrect email"


class WrongCredentialsError(Exception):
    def __str__(self):
        return "Incorrect credentials."


class NegativePointError(Exception):
    def __str__(self):
        return "Incorrect points format."


def show_list_students():
    if len(Student.all_students) == 0:
        print("No students found.")
    else:
        print("Students:")
        for student in Student.all_students:
            print(f"{student.id}")


def find_student_by_id(some_id):
    for student in Student.all_students:
        if student.id == some_id:
            return student
    return None


def verify_email(email):
    email_parts = email.split("@")
    if len(email_parts) != 2:
        return False
    tail_parts = email_parts[1].split('.')
    if len(tail_parts) != 2:
        return False
    return True


def is_email_unique(email):
    return email in Student.all_emails


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
    command_parts = command.split(" ")
    if len(command_parts) < 3:
        raise WrongCredentialsError

    email = command_parts[-1]
    if not verify_email(email):
        raise WrongEmailError

    first = command_parts[0]
    if not verity_name(first):
        raise WrongNameError

    second = command_parts[1:-1]
    if not verify_lastname(second):
        raise WrongLastNameError
    else:
        second = " ".join(second)

    return first, second, email


def add_students():
    print("Enter student credentials or 'back' to return:")
    counter = 0
    while True:
        command = input()
        if command == 'back':
            print(f"Total {counter} students have been added.")
            break
        try:
            credentials = verify(command)
        except WrongEmailError as err:
            print(err)
            continue
        except WrongNameError as err:
            print(err)
            continue
        except WrongLastNameError as err:
            print(err)
            continue
        except WrongCredentialsError as err:
            print(err)
            continue
        else:
            if is_email_unique(credentials[-1]):
                print("This email is already taken.")
                continue
            Student(*credentials)
            counter += 1
            print("The student has been added.")


def add_points():
    print("Enter an id and points or 'back' to return:")
    while True:
        entry_points = input()
        if entry_points == "back":
            break
        id_vs_points = entry_points.split(" ")
        try:
            student_id = int(id_vs_points[0])
            student_by_id = find_student_by_id(student_id)
        except ValueError:
            print(f"No student is found for id={id_vs_points[0]}.")
            continue
        if student_by_id is None:
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
        try:
            for point in points:
                if point < 0:
                    raise NegativePointError
        except NegativePointError as err:
            print(err)
        else:
            student_by_id.update_points(*points)
            print("Points updated.")


def find():
    print("Enter an id or 'back' to return:")
    while True:
        entry_id = input()
        if entry_id == "00000":
            print(f"No student is found for id={entry_id}.")
            continue
        if entry_id == "back":
            break
        try:
            student_id = int(entry_id)
            student_by_id = find_student_by_id(student_id)
        except ValueError:
            print(f"No student is found for id={entry_id}.")
            continue
        if student_by_id is None:
            print(f"No student is found for id={student_id}.")
            continue
        student_by_id.print_student()


commands = {
    "add students": add_students,
    "list": show_list_students,
    "add points": add_points,
    "find": find,
}


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
            break  # exit() ?
        try:
            commands.get(entry)()
        except TypeError:
            print("Unknown command!")


if __name__ == '__main__':
    main()
