
def add_course():
    info = []
    while True:
        userInput = input("Enter Course ID: ")
        if len(userInput) == 7 and userInput[0:2].isalpha() and userInput[3:6].isdigit():
            info.append(userInput.upper())
            break
        else:
            print("Error: Invalid format")
    while True:
        userInput = input("Enter Course Name: ")
        if any(i.isdigit() for i in userInput):
            print("Error: No numbers allowed")
            continue
        info.append(userInput)
        break
    courseLine = ",".join(info)
    with open("courses.txt", "a") as a:
        a.write(courseLine)
        a.write('\n')
    print("\nAction successful!\n--------------------")

def add_student():
    info = []
    while True:
        userInput = input("Enter Student ID: ")
        if len(userInput) == 8 and userInput.isdigit():
            info.append(userInput)
            break
        else:
            print("Error: Invalid format")
    while True:
        userInput = input("Enter Student Name: ")
        if any(i.isdigit() for i in userInput):
            print("Error: No numbers allowed")
            continue
        info.append(userInput)
        break
    while True:
        userInput = input("Enter Student Email: ")
        if not userInput.endswith("@imail.sunway.edu.my") or userInput[0] == '@':
            print("Error: must end with @imail.sunway.edu.my")
            continue
        info.append(userInput)
        break
    studentLine = ",".join(info)
    with open("students.txt", "a") as a:
        a.write(studentLine)
        a.write('\n')
    print("\nAction successful!\n--------------------")

def print_option():
        print("> 1 Add a new student")
        print("> 2 Add a new course")
        print("> 3 Record student marks")
        print("> 4 Display individual student performance")
        print("> 5 Display course performance summary")
        print("> 6 Export performance report")
        print("> 0 Exit")

def parse_files():
    try:
        with open("students.txt") as a:
            pass
        with open("grades.txt") as b:
            pass
        with open("grades.txt") as c:
            pass

    except FileNotFoundError:
        print("Error: Unable to open files")
        exit()

def main():
    print("Welcome to the Ultimate Python-Powered Student Grading System!")
    parse_files()
    while True:
        print_option()
        userInput = input("Please select an action: ")
        match userInput:
            case '1':
                add_student()
            case '2':
                add_course()
            case '3':
                print("3")
            case '4':
                print("4")
            case '5':
                print("5")
            case '6':
                print("6")
            case '0':
                print("Exiting program...")
                break
            case _ :
                print("Invalid option!")



if __name__ == "__main__":
    main()
