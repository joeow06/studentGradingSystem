
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

def add_student():
    print(BLUE + "\n****** Adding new student ******" + RESET)
    info = []
    while True:
        userInput = input("Enter Student ID: ")
        # Prevent the user from duplicating the student ID
        students=load_students()
        if userInput in students:
            print(RED + "Error" + RESET + ": This student ID has been recorded")
            continue
        if len(userInput) == 8 and userInput.isdigit():
            info.append(userInput)
            break
        else:
            print(RED + "Error" + RESET + ": Invalid format")
    while True:
        userInput = input("Enter Student Name: ")
        if any(i.isdigit() for i in userInput):
            print(RED + "Error" + RESET + ": No numbers allowed")
            continue
        info.append(userInput.upper())
        break
    while True:
        userInput = input("Enter Student Email: ")
        if not userInput.endswith("@imail.sunway.edu.my") or userInput[0] == '@':
            print(RED + "Error" + RESET + ": Must end with @imail.sunway.edu.my")
            continue
        info.append(userInput)
        break
    studentLine = ",".join(info)
    with open("students.txt", "a") as a:
        a.write(studentLine)
        a.write("\n")
    print(GREEN + "****** Action Succesful ******" + RESET)

#function to add a new course
def add_course():
    print(BLUE + "\n****** Adding new course ******" + RESET)
    info = []
    while True:
        userInput = input("Enter Course ID: ").upper()
        courses=load_courses()
        # To prevent the user from duplicate the course id
        if userInput in courses:
            print(RED + "Error" + RESET + ": This course ID has been recorded")
            continue
        if len(userInput) == 7 and userInput[0:2].isalpha() and userInput[3:6].isdigit():
            info.append(userInput.upper())
            break
        else:
            print(RED + "Error" + RESET + ": Invalid format")
    while True:
        userInput = input("Enter Course Name: ").upper()
        if userInput in courses.values():
            print(RED + "Error" + RESET + ": This course name has been recorded")
        if any(i.isdigit() for i in userInput):
            print(RED + "Error" + RESET + ": No numbers allowed")
            continue
        info.append(userInput.upper())
        break
    courseLine = ",".join(info)
    with open("courses.txt", "a") as a:
        a.write(courseLine)
        a.write("\n")
    print(GREEN + "****** Action Succesful ******" + RESET)

# funciton to return recorded students in dict form
def load_students():
    students = {}
    with open("students.txt", "r") as s:
        for line in s:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                # make sure the line has at east 3 parts (prevent empty lines or incomplete record)
                # only then assign id,name accordingly
                student_id = parts[0]
                name = parts[1]
                students[student_id] = name
    return students


#function to return recorded courses in dict form
def load_courses():
    courses = {}
    with open("courses.txt","r") as c:
        for line in c:
            parts = line.strip().split(",")
            if len(parts) >=2:
                course_id = parts[0]
                course_name = parts[1]
                courses[course_id] =course_name
    return courses

# function to return only student id and course name in dict form
def check_grades():
    records = {}
    with open("grades.txt", "r") as g:
        for line in g:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                student_id = parts[0]
                course_name = parts[1]

                # initialize list if first time
                if student_id not in records:
                    records[student_id] = []

                # add course
                records[student_id].append(course_name)
    return records

#function to record the results
def record():
    print(BLUE + "\n****** Recording marks ******" + RESET)
    info = []
    students = load_students()
    student_grades = load_grades()
    courses = load_courses()
    # Initialize change for later use (to overwrite the marks)
    change = 0

    if not students:
        # if there is no recorded student, stop function early
        print(RED + "Error" + RESET + ": No student found. Please add a student first.")
        return
    if not courses:
        # if there is no recorded course, stop function early
        print(RED + "Error" + RESET + ": No course found. Please add a course first.")
        return
    print("Available students:")
    for student_id, name in students.items():
        print(f"{student_id} - {name}")
    print()
    while True:
        userInput = input("Enter Student ID: ")
        if userInput in students:
            print(f"\nStudent found: {students[userInput]}")
            info.append(userInput)
            break
        else:
            print(RED + "Error" + RESET + ": Student not found")
            continue
    records = check_grades()
    student_id = info[0]
    # The line to prevent error if no student ID recorded yet
    if student_id in records:
        choice = input("[1]  Add grades \n[2]  Change marks \n[0]  Exit \nSelect an action: ")
        match choice:
            case '1':
                course_list=list(courses.values())
                course_list.sort()
                # make all the graded course as a list and sort it in ascending order
                graded_list = list(records[student_id])
                graded_list.sort()
                # Compare all the courses with all the graded courses
                if course_list != graded_list:
                    print('\nCourse(s) available: ')
                    # Only display the ungraded course(s)
                    for course_id, course_name in courses.items():
                        if course_name not in records[student_id]:
                            print(f'{course_id}: {course_name}')
                else:
                    print(YELLOW + "Warning" + RESET + ": Every course has been graded.\n") #if every course is graded
                    return
            case '2':
                # update the change with the data 1, later the code can be executed accordingly
                change = 1
                print('\nCourse(s) available:')
                # display only the graded course(s)
                for course_id, course_name in courses.items():
                    if course_name in records[student_id]:
                        print(f'{course_id}: {course_name}')
            case '0':
                print(GREEN + '****** Exiting *******' + RESET)
                return
            case _:
                print(RED + "Error" + RESET + ": Invalid input")
                return
    else:
        # If no recorded student, just display all the courses
        print("Course(s) available:")
        for course_id, course_name in courses.items():
            print(f'{course_id}: {course_name}')
    print()
    while True:
        # To prevent error when there is a new student id to be recorded
        if student_id not in records:
            records[student_id] = []
        userInput = input("Enter Course ID: ").upper()
        if userInput not in courses:
            print(RED + "Error" + RESET + ": Course not found")
            continue
        # when change == 1, execute the codes for changing the marks
        if change == 1:
            if courses[userInput] in records[student_id]:
                print(f"Courses found: {courses[userInput]}\n")
                course_name = courses[userInput]
                print(f'Current marks : {student_grades[student_id][course_name][1]}')
                print(f'Current grade : {student_grades[student_id][course_name][0]}')
                info.append(course_name)
                break
            else:
                print(RED + "Error" + RESET + ": Course not found")
                continue
        # if the user input program is the same as the program has been recorded, an error will occur
        else:
            if courses[userInput] not in records[student_id]:
                print(f"Courses found: {courses[userInput]}\n")
                course_name = courses[userInput]
                info.append(course_name)
                break
            else:
                print(RED + "Error" + RESET + ": Course not found")
                continue

    while True:
        try:
            userInput = float(input("Enter marks(%): "))
            if userInput<0 or userInput>100:
                print(RED + "Error" + RESET + ": Invalid range! 0 - 100 only")
                continue
            marks = str(f"{userInput:.2f}")
            info.append(f"{marks}")
            if userInput >= 80:
                grade='A+'
            elif userInput >= 75:
                grade='A'
            elif userInput >= 70:
                grade='A-'
            elif userInput >= 65:
                grade='B+'
            elif userInput >= 60:
                grade='B'
            elif userInput >= 55:
                grade='B-'
            elif userInput >= 50:
                grade='C'
            elif userInput >= 45:
                grade='C-'
            elif userInput >= 40:
                grade='D'
            else:
                grade='F'
            print(f"Grade : {grade}")
            info.append(grade)
            break
        except ValueError:
            print(RED + "Error" + RESET + ": Only numbers allowed")
    gradeLine = ",".join(info)
    # if change == 1 then executes the codes for replacing a particular line
    if change == 1:
        with open("grades.txt","r") as g:
            data = g.read()
        origrade, orimarks=student_grades[student_id][course_name]
        updated = data.replace((f'{student_id},{course_name},{orimarks},{origrade}'),(gradeLine))
        with open("grades.txt","w") as g:
            g.write(updated)
            g.write("\n")
    else:
        with open("grades.txt", "a") as g:
            g.write(gradeLine)
            g.write("\n")
    print(GREEN + "****** Action Succesful ******" + RESET)

def load_grades():
    student_grades = {}
    with open("grades.txt","r") as g:
        for line in g:
            parts = line.strip().split(",")
            if len(parts) >= 4:
                student_id = parts[0]
                course_name = parts[1]
                marks = parts[2]
                grade = parts[3]
                if student_id not in student_grades:
                    student_grades[student_id] = {}

                # add course: grade
                student_grades[student_id][course_name] = grade, marks

    return student_grades


def display_individual(flag):
    if not flag:
        print(BLUE + "\n****** Display Student Performance ******" + RESET)
    student_grades = load_grades()
    if not student_grades:
        print(RED + "Error" + RESET + ": No grades record found. Add a record first.")
        return
    students=load_students()
    print("Available students:")
    for student_id, name in students.items():
        print(f"{student_id} - {name}")
    print()
    while True:
        userInput = input("Enter Student ID: ")
        if userInput in students:
            print(f"Student found: {students[userInput]}")
            break
        else:
            print(RED + "Error" + RESET + ": Student not found")
            continue
    if not flag:
        print(f'\n{userInput} - {students[userInput]}')
        if userInput in student_grades:
            for program_name, grade in student_grades[userInput].items():
                print(f'{program_name.ljust(25)} : {grade[0].ljust(2)} | {grade[1].ljust(2)}')
        else:
            print("No records available")
    else:
        print(f"\nExporting {userInput}_grades.txt ...")

        with open(f"{userInput}_grades.txt", "w") as f:
            f.write("========================================\n")
            f.write(f"        {userInput} Performance Report\n")
            f.write("========================================\n\n")

            # Student info header
            f.write(f"Student ID : {userInput}\nName       : {students[userInput]}\n\n")

            f.write("COURSE RESULTS\n")
            f.write("----------------------------------------------------\n")
            f.write("| Course Name             | Marks | Grade          |\n")
            f.write("----------------------------------------------------\n")

            if userInput in student_grades:
                for course_name, (grade, marks) in student_grades[userInput].items():
                    f.write(
                        f"| {course_name.ljust(28)}"
                        f"| {str(marks).ljust(6)}"
                        f"| {grade.ljust(11)}|\n"
                    )
            else:
                f.write("| No course records found                          |\n")

            f.write("----------------------------------------------------\n")

    print(GREEN + "****** Action Succesful ******" + RESET)

def display_course(flag):
    if not flag:
        print(BLUE + "\n****** Display Course Summary ******" + RESET)
    courses = load_courses()
    grades = load_grades()
    students = load_students()
    marks_list = []
    students_list = []

    print("Available courses:")
    for course_id, course_name in courses.items():
        print(f"{course_id} - {course_name}")
    print()
    while True:
        userInput = input("Enter course ID: ").upper()
        if userInput in courses:
            break
        else:
            print(RED + "Error" + RESET + ": Course not found!")
    target_course = courses[userInput]
    for student_id, course_dict in grades.items():
        if target_course in course_dict:
            grade, mark = course_dict[target_course]
            marks_list.append(float(mark))
            students_list.append(student_id + " - " + students[student_id])

    average = sum(marks_list) / len(marks_list)
    if not flag:
        print(f"\n==== {target_course} ====")
        print("Students:")
        i = 1
        for x in students_list:
            print(f"{i}) {x}")
            i += 1
        print("\nStatistics: ")
        print(f"- Average: {average}%\n- Highest: {max(marks_list)}%\n- Lowest: {min(marks_list)}%")
    else:
        print(f"\nExporting {userInput}_summary.txt ...")
        with open(f"{userInput}_summary.txt", "w") as f:
            f.write("========================================\n")
            f.write(f"         {userInput} Summary Report\n")
            f.write("========================================\n\n")
            f.write("STUDENTS\n")
            f.write("----------------------------------------\n")
            f.write("| No | Student ID | Name               |\n")
            f.write("----------------------------------------\n")
            i = 1
            for x in students_list:
                f.write(f"| {str(i).ljust(2)} | {x.split(' - ')[0].ljust(10)} | {x.split(' - ')[1].ljust(18)} |\n")
                i += 1
            f.write("----------------------------------------\n\n")

            avg = sum(marks_list) / len(marks_list)
            highest = max(marks_list)
            lowest = min(marks_list)

            f.write("STATISTICS\n")
            f.write("----------------------------------------\n")
            f.write(f"Average : {avg:.2f}%\n")
            f.write(f"Highest : {highest}%\n")
            f.write(f"Lowest  : {lowest}%\n")
            f.write("----------------------------------------\n")
    print(GREEN + "****** Action Successful ******" + RESET)

def export():
    print(BLUE + "\n****** Exporting ******" + RESET)
    print("[1] Export course summary\n[2] Export student report")
    userInput = input("Select an action: ")
    match userInput:
        case '1':
            display_course(True)
        case '2':
            display_individual(True)
        case _ :
            print(RED + "Error" + RESET + ": Invalid input")

#function to show the options
def print_option():
    print("\n[1]   Add a new student")
    print("[2]   Add a new course")
    print("[3]   Record student marks")
    print("[4]   Display individual student performance")
    print("[5]   Display course performance summary")
    print("[6]   Export performance report")
    print("[0]   Exit")


#function to check if the files exist
def parse_files():
    try:
        with open("students.txt") as _:
            pass
        with open("grades.txt") as _:
            pass
        with open("courses.txt") as _:
            pass

    except FileNotFoundError:
        print(RED + "Error" + RESET + ": Unable to open files")
        exit()


def main():
    parse_files()
    print(BLUE + "\nWelcome to the Ultimate Python-Powered Student Grading System" + RESET)
    while True:
        print_option()
        userInput = input("Select an action: ")
        match userInput:
            case '1':
                add_student()
            case '2':
                add_course()
            case '3':
                record()
            case '4':
                display_individual(False)
            case '5':
                display_course(False)
            case '6':
                export()
            case '0':
                print(RED + "Exiting program..." + RESET)
                break
            case _ :
                print("Invalid option!")

# Program starts here
main()
