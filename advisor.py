'''
1. Update own password
2. Add a new client
3. Modify or ipdate the information of a client in the system
4. Search and retreive the information of a client
'''
import input_handling


class Advisor:
    def updatePassword() -> str:
        print('''
            your password must contain:
            at least 8 characters,
            at most 30 characters,
            letters (a-z) (A-Z), number (0-9), special characters such as (~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/),
            a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character.
        ''')

        newPassword = input("please enter a password: ")
        while (not input_handling.correctPassword(newPassword)):
            newPassword = input("invalid input, please enter a password: ")
        return newPassword

    def fullname() -> str:
        fullname = input("please enter the full name: ")
        while (not fullname.replace(' ', '')):
            fullname = input(
                "invalid input, please enter the full name: ")
        return fullname

    def address() -> str:
        streetnameandnumber = input(
            "please enter the client's street name and house number: ")
        while (not streetnameandnumber.replace(' ', '')):
            streetnameandnumber = input(
                "invalid input, please enter the client's street name and house number: ")
        zipcode = input("please enter the client's ZipCode (DDDDXX): ")
        while (not input_handling.correctZipCode(zipcode)):
            zipcode = input(
                "invalid input, please enter the client's ZipCode (DDDDXX): ")
        city = Advisor.city()
        address = streetnameandnumber + " " + zipcode + " " + city
        return address

    def city() -> str:
        cityList = ["Amsterdam", "Rotterdam", "Den Haag", "Utrecht",
                    "Eindhoven", "Tilburg", "Groningen", "Almere", "Breda", "Nijmegen"]
        choiselist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        for i in range(1, len(cityList) + 1):
            print(f"[{i}] {cityList[i - 1]}")
        choice = input(
            "please enter the number of the city the client is from: ")
        while (choice not in choiselist):
            choice = input(
                "invalid input, please enter the number of the city the client is from: ")
        city = cityList[int(choice) - 1]
        return city

    def email() -> str:
        email = input("please enter the client's email: ")
        while (not input_handling.correctEmail(email)):
            email = input("invalid input, please enter the client's email: ")
        return email

    def phoneNumber() -> str:
        phoneNumber = input(
            "please enter the client's phone number (+31-6-DDDDDDDD), only enter the missing digits (D): ")
        while (not input_handling.correctPhoneNumber(phoneNumber)):
            phoneNumber = input(
                "invalid input, please enter the client's phone number (+31-6-DDDDDDDD), only enter the missing digits (D): ")
        phoneNumber = "+31-6-" + phoneNumber
        return phoneNumber

    def addClient(db):
        return Advisor.fullname(), Advisor.address(), Advisor.email(), Advisor.phoneNumber()

    def modifyClient(client):
        options = ["1", "2", "3", "4", "0"]
        optionDesc = [f"change full name - {client[1]}", f"change address - {client[2]}",
                      f"change email - {client[3]}", f"change phone number - {client[4]}", "exit"]
        for i in range(1, len(optionDesc) + 1):
            print(f"[{options[i-1]}] {optionDesc[i-1]}")
        choice = input(
            "please select the number of the option you would like to perform: ")
        while (choice not in options):
            choice = input(
                "invalid input, please select the number of the option you would like to perform: ")
        choice = int(choice)
        while choice != 0:
            if (choice == 1):
                client[1] = Advisor.fullname()
                print("full name has been changed\n")
            elif (choice == 2):
                client[2] = Advisor.address()
                print("address has been changed\n")
            elif (choice == 3):
                client[3] = Advisor.email()
                print("email has been changed\n")
            elif (choice == 4):
                client[4] = Advisor.phoneNumber()
                print("phone number has been changed\n")

            for i in range(1, len(optionDesc) + 1):
                print(f"[{options[i-1]}] {optionDesc[i-1]}")
            choice = input(
                "please select the number of the option you would like to perform: ")
            while (choice not in options):
                choice = input(
                    "invalid input, please select the number of the option you would like to perform: ")
            return client

    def searchClient():
        return
