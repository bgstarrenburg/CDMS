import input_handling
import advisor
'''
1. Update own password
2. Check the list of users and their roles.
3. Define and add a new advisor to the system
4. Modify or update an existing advisor's account and profile
5. Delete an exisiting advisor's account
6. Reset an advisor's password (temporary password)
7. Make a backup of the system
8. See the log file of the syste,
9. Add a new client to the system
10. Modify or update the information of a client in the system.
11. Delete a cleint's record from the database (advisor can only modify or update)
12. Search and retreive information of a client
'''


class Systemadmin:
    def username(usernames):
        print('''
            The username must contain:
            at least 5 characters,
            at most 20 characters,
            letters (a-z), numbers (0-9), dashes (-), underscores(_), apostophes(') and periods (.)'''
              )
        username = input("please enter a username: ").lower()
        while (not input_handling.correctUsername(username) or username in usernames):
            username = input(
                "invalid input (username might already exist), please enter a username: ")
        return username

    def password():
        password = advisor.Advisor.updatePassword()
        return password

    def fullname():
        fullname = advisor.Advisor.fullname()
        return fullname

    def addAdvisor(usernames):
        username = Systemadmin.username(usernames)
        password = Systemadmin.password()
        fullname = Systemadmin.fullname()
        return username, password, fullname

    def modifyAdvisorChoice():
        options = ["1", "2", "0"]
        optionDesc = ["change advisor's username",
                      "change advisor's full name"]
        for i in range(1, len(optionDesc) + 1):
            print(f"[{options[i-1]}] {optionDesc[i-1]}")
        choice = input(
            "please select the number of the option you would like to perform (enter [0] to exit): ")
        while (choice not in options):
            choice = input(
                "invalid input, please select the number of the option you would like to perform (enter [0] to exit): ")
        return int(choice)
