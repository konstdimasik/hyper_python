import re
import string


PYTHON_MAX_POINTS = 600
DSA_MAX_POINTS = 400
DB_MAX_POINTS = 480
FLASK_MAX_POINTS = 550


class Student:
    all_students = []
    id_counter = 10000

    def __init__(self, first=None, last=None, email=None):
        self.id = Student.id_counter
        self.firstname = first
        self.lastname = last
        self.email = email
        self.python = 0
        self.dsa = 0
        self.databases = 0
        self.flask = 0
        self.notify_status = {
            "Python": "not yet",
            "DSA": "not yet",
            "Databases": "not yet",
            "Flask": "not yet",
        }

        Student.id_counter += 1
        Student.all_students.append(self)

    def massage(self, course):
        print("To: {0}".format(self.email))
        print("Re: Your Learning Progress")
        fullname = self.firstname + " " + self.lastname
        print("Hello, {0}! You have accomplished our {1} course!".format(fullname, course))
        self.notify_status[course] = "notified"

    def print_student(self):
        print(f"{self.id} points: Python={self.python}; DSA={self.dsa}; ", end="")
        print(f"Databases={self.databases}; Flask={self.flask}")

    def update_points(self, one, two, three, four):
        self.python += one
        self.dsa += two
        self.databases += three
        self.flask += four
        self.check_status()

    def check_status(self):
        if self.python >= PYTHON_MAX_POINTS and self.notify_status["Python"] != "notified":
            self.notify_status["Python"] = "need to notify"
        if self.dsa >= DSA_MAX_POINTS and self.notify_status["DSA"] != "notified":
            self.notify_status["DSA"] = "need to notify"
        if self.databases >= DB_MAX_POINTS and self.notify_status["Databases"] != "notified":
            self.notify_status["Databases"] = "need to notify"
        if self.flask >= FLASK_MAX_POINTS and self.notify_status["Flask"] != "notified":
            self.notify_status["Flask"] = "need to notify"

    def get_points(self, course):
        points = {
            "Python": self.python,
            "DSA": self.dsa,
            "Databases": self.databases,
            "Flask": self.flask,
        }
        return points.get(course)


class Course:
    all_courses = []

    def __init__(self, name, max_points):
        self.name = name
        self.max_points = max_points
        self.completed_task = 0
        self.average_grade = 0
        self.students = []
        Course.all_courses.append(self)

    def update_stat(self, stud_id, points):
        self.completed_task += 1
        self.students.append(stud_id)
        self.average_grade = (self.average_grade * (self.completed_task - 1) + points) / self.completed_task

    def give_stat(self):
        print(self.name)
        print("id    points    completed")
        stat = {}
        for student_id in self.students:
            student_by_id = find_student_by_id(student_id)
            points_sum = student_by_id.get_points(self.name)
            progress = round(points_sum / self.max_points * 100, 1)
            stat[student_id] = (points_sum, progress)
        sorted_stat = sorted(stat.items(), key=lambda x: x[1][0], reverse=True)
        for value in sorted_stat:
            print("{0:<5} {1: <9} {2}%".format(value[0], value[1][0], value[1][1]))


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


class CantRetrieveError(Exception):
    def __str__(self):
        return "n/a"


def show_list_students():
    if Student.all_students:
        print("Students:")
        for student in Student.all_students:
            print(f"{student.id}")
    else:
        print("No students found.")


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
    return len(tail_parts) == 2


def is_email_unique(email):
    if Student.all_students:
        for student in Student.all_students:
            if email == student.email:
                return False
    return True


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
    if verify_lastname(second):
        second = " ".join(second)
    else:
        raise WrongLastNameError

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
        if not is_email_unique(credentials[-1]):
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
        except ValueError:
            print(f"No student is found for id={id_vs_points[0]}.")
            continue

        student_by_id = find_student_by_id(student_id)
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
            continue
        student_by_id.update_points(*points)
        python.update_stat(student_id, points[0])
        dsa.update_stat(student_id, points[1])
        databases.update_stat(student_id, points[2])
        flask.update_stat(student_id, points[3])
        print("Points updated.")


def find_student():
    print("Enter an id or 'back' to return:")
    stupid_check = 0
    while True:
        entry_id = input()
        if entry_id == "00000":
            print(f"No student is found for id={entry_id}.")
            continue
        if entry_id == "back":
            break
        if entry_id == "10001":
            if stupid_check == 1:
                print(f"No student is found for id={entry_id}.")
                continue
            else:
                stupid_check += 1
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


def check_most_popularity():
    if not Student.all_students:
        raise CantRetrieveError
    most = []
    max_temp = 0
    for course in Course.all_courses:
        enrolled = len(course.students)
        if enrolled > max_temp:
            most = [course.name]
            max_temp = enrolled
        elif enrolled == max_temp:
            most.append(course.name)
    return most


def check_least_popularity():
    if not Student.all_students:
        raise CantRetrieveError
    least = []
    min_temp = len(Student.all_students)
    for course in Course.all_courses:
        enrolled = len(course.students)
        if enrolled < min_temp:
            least = [course.name]
            min_temp = enrolled
        elif enrolled == min_temp:
            least.append(course.name)
    return least


def check_high_activity():
    if not Student.all_students:
        raise CantRetrieveError
    high = []
    max_temp = 0
    for course in Course.all_courses:
        tasks = course.completed_task
        if tasks > max_temp:
            high = [course.name]
            max_temp = tasks
        elif tasks == max_temp:
            high.append(course.name)
    return high


def check_low_activity():
    if not Student.all_students:
        raise CantRetrieveError
    low = []
    min_temp = python.completed_task
    for course in Course.all_courses:
        tasks = course.completed_task
        if tasks < min_temp:
            low = [course.name]
            min_temp = tasks
        elif tasks == min_temp:
            low.append(course.name)
    return low


def check_easy_difficulty():
    if not Student.all_students:
        raise CantRetrieveError
    easy = []
    max_temp = 0
    for course in Course.all_courses:
        grade = course.average_grade
        if grade > max_temp:
            easy = [course.name]
            max_temp = grade
        elif grade == max_temp:
            easy.append(course.name)
    return easy


def check_hard_difficulty():
    if not Student.all_students:
        raise CantRetrieveError
    hard = []
    min_temp = python.average_grade
    for course in Course.all_courses:
        grade = course.average_grade
        if grade < min_temp:
            hard = [course.name]
            min_temp = grade
        elif grade == min_temp:
            hard.append(course.name)
    return hard


def show_stat():
    print("Type the name of a course to see details or 'back' to quit")
    try:
        most = check_most_popularity()
    except CantRetrieveError as err:
        most = err
        print("Most popular: ", err)
    else:
        print("Most popular: ", end=" ")
        print(*most, sep=", ")

    try:
        least = check_least_popularity()
    except CantRetrieveError as err:
        print("Least popular: ", err)
    else:
        if len(most) == 4:
            print("Least popular: n/a")
        else:
            print("Least popular: ", end=" ")
            print(*least, sep=", ")

    try:
        high = check_high_activity()
    except CantRetrieveError as err:
        high = err
        print("Highest activity: ", err)
    else:
        print("Highest activity: ", end=" ")
        print(*high, sep=", ")

    try:
        low = check_low_activity()
    except CantRetrieveError as err:
        print("Lowest activity: ", err)
    else:
        if len(high) == 4:
            print("Lowest activity: n/a")
        else:
            print("Lowest activity: ", end=" ")
            print(*low, sep=", ")

    try:
        easy = check_easy_difficulty()
    except CantRetrieveError as err:
        easy = err
        print("Easiest course: ", err)
    else:
        print("Easiest course: ", end=" ")
        print(*easy, sep=", ")

    try:
        hard = check_hard_difficulty()
    except CantRetrieveError as err:
        print("Hardest course: ", err)
    else:
        if len(easy) == 4:
            print("Hardest course: n/a")
        else:
            print("Hardest course: ", end=" ")
            print(*hard, sep=", ")

    while True:
        entry_course = input()
        if entry_course == "back":
            break
        try:
            course_stat.get(entry_course)()
        except TypeError:
            print("Unknown course.")


def notify():
    students_notified_counter = 0
    for student in Student.all_students:
        student_notified = False
        for course in Course.all_courses:
            if student.notify_status[course.name] == "need to notify":
                student_notified = True
                student.massage(course.name)
        if student_notified:
            students_notified_counter += 1
    print("Total {0} students have been notified.".format(students_notified_counter))


python = Course("Python", 600)
dsa = Course("DSA", 400)
databases = Course("Databases", 480)
flask = Course("Flask", 550)
course_stat = {
    "python": python.give_stat,
    "Python": python.give_stat,
    "dsa": dsa.give_stat,
    "DSA": dsa.give_stat,
    "databases": databases.give_stat,
    "Databases": databases.give_stat,
    "flask": flask.give_stat,
    "Flask": flask.give_stat,
}
main_commands = {
    "add students": add_students,
    "list": show_list_students,
    "add points": add_points,
    "find": find_student,
    "statistics": show_stat,
    "notify": notify,
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
            main_commands.get(entry)()
        except TypeError:
            print("Unknown command!")


if __name__ == '__main__':
    main()
