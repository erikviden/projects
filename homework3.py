class Student:
    def __init__(self, name, surname, class_name):
        self.first_name = name
        self.last_name = surname
        self.class_name = class_name


class Teacher:
    def __init__(self, name, surname, subject):
        self.first_name = name
        self.last_name = surname
        self.teaching_subject = subject
        self.teaching_classes = []

    def add_teaching_class(self, teaching_class):
        self.teaching_classes.append(teaching_class)


class Tutor:
    def __init__(self, name, surname, class_lead):
        self.first_name = name
        self.last_name = surname
        self.class_lead = class_lead


def create_student():
    name = input("Enter student's name: ")
    surname = input("Enter student's surname: ")
    class_name = input("Enter student's class name:")
    return Student(name, surname, class_name)


def create_teacher():
    name = input("Enter teacher's name: ")
    surname = input("Enter teacher's surname: ")
    subject = input("Enter the subject the teacher teaches: ")
    teacher = Teacher(name, surname, subject)

    while True:
        teaching_class = input("Enter the class the teacher teaches (leave blank to stop): ")
        if not teaching_class:
            break
        teacher.add_teaching_class(teaching_class)

    return teacher


def create_tutor():
    name = input("Enter tutor's first name: ")
    surname = input("Enter tutor's last name: ")
    class_lead = input("Enter the class the tutor leads: ")
    return Tutor(name, surname, class_lead)


def manage_student(students, teachers):
    first_name = input("Enter student's first name: ")
    last_name = input("Enter student's last name: ")
    for student in students:
        if student.first_name == first_name and student.last_name == last_name:
            print(f"Student: {first_name} {last_name}")
            print(f"Class: {student.class_name}")
            print("Teachers:")
            for teacher in teachers:
                if student.class_name in teacher.teaching_classes:
                    print(f"{teacher.first_name} {teacher.last_name}")


def manage_class(students, tutors):
    class_name = input("Enter the name of the class:")
    print("Students in this class:")
    for student in students:
        if student.class_name == class_name:
            print(f"{student.first_name} {student.last_name}")
    print(f"Tutor of class {class_name}:")
    for tutor in tutors:
        if tutor.class_lead == class_name:
            print(f"{tutor.first_name} {tutor.last_name}")


def manage_teacher(teachers):
    first_name = input("Enter teacher's first name: ")
    last_name = input("Enter teacher's last name: ")
    print(f"Teacher {first_name} {last_name} teaches:")
    for teacher in teachers:
        if teacher.first_name == first_name and teacher.last_name == last_name:
            for teaching_class in teacher.teaching_classes:
                print(teaching_class)


def manage_tutor(tutors, students):
    first_name = input("Enter tutor's first name: ")
    last_name = input("Enter tutor's last name: ")
    print(f"Tutor {first_name} {last_name} leads:")
    for tutor in tutors:
        if tutor.first_name == first_name and tutor.last_name == last_name:
            for student in students:
                if student.class_name == tutor.class_lead:
                    print(f"{student.first_name} {student.last_name}")


students = []
teachers = []
tutors = []
classes = []

while True:
    print("Available commands:\n"
          "- 'create' - Starts the user creation process. \n"
          "- 'manage' - Starts the user management process.\n"
          "- 'end' - Terminates the program.\n")

    command = input("Enter the command you want to perform:")

    print("")

    if command == "create":
        create = input("Are you a 'student','teacher' or 'tutor'('end' to end this operation):")
        if create == "student":
            student = create_student()
            students.append(student)

        elif create == "teacher":
            teacher = create_teacher()
            teachers.append(teacher)

        elif create == "tutor":
            tutor = create_tutor()
            tutors.append(tutor)

        elif create == "end":
            continue
        else:
            print("Invalid user type.\n")

    elif command == "manage":
        print("\nManagement options:")
        print("- 'class' - Manages class.")
        print("- 'student' - Manages student.")
        print("- 'teacher' - Manages teacher.")
        print("- 'tutor' - Manages tutor.")
        print("- 'end' - Returns to start.\n")

        option = input("Enter option to manage: ")

        if option == "class":
            manage_class(students, tutors)
        elif option == "student":
            manage_student(students, teachers)
        elif option == "teacher":
            manage_teacher(teachers, )
        elif option == "tutor":
            manage_tutor(tutors, students)
        elif option == "end":
            continue
        else:
            print("Invalid option.\n")

    elif command == "end":
        print("Terminating program...")
        break

    else:
        print("Invalid command.\n")
