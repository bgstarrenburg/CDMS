import sqlite3
from sqlite3.dbapi2 import OperationalError
import zipfile
import cipher
import systemadmin
import advisor
import datetime
import ui


class db:
    def __init__(self, db_name, client_table_name, users_table_name):
        self.db_name = db_name
        self.client_table_name = client_table_name
        self.users_table_name = users_table_name

        self.loggedin = 0
        self.loggedin_user = None
        self.admin = -1
        self.logAlert = 0

        self.reset()

    def reset(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

        # create client table if it does not exist
        tb_create = "CREATE TABLE client (person_id int, fullname CHAR, address CHAR, email CHAR, phone CHAR)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            self.cur.execute(
                "INSERT INTO client (person_id, fullname) VALUES (1, 'Olol#Dqghuvrq')")
            self.cur.execute(
                "INSERT INTO client (person_id, fullname) VALUES (2, 'Dqqh#Edqzduwk')")
            self.conn.commit()
        except:
            None

        # create user table if it does not exist
        tb_create = "CREATE TABLE users (username TEXT, password TEXT, fullname TEXT, admin INT, temp INT);"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            self.cur.execute(
                "INSERT INTO users (username, password, fullname, admin, temp) VALUES ('superadmin', 'Admin!23', 'super admin', 2, 0)")
            self.cur.execute(
                "INSERT INTO users (username, password, fullname, admin, temp) VALUES ('systemadmin', 'admin456', 'system admin', 1, 0)")
            self.cur.execute(
                "INSERT INTO users (username, password, fullname, admin, temp) VALUES ('advisor', 'advisor1' , 'system advisor', 0, 0)")
            self.conn.commit()
        except:
            None

        # create log table if it does not exist
        tb_create = "CREATE TABLE log (no INT, username TEXT, date TEXT, time TEXT, activity TEXT, information TEXT, suspicious TEXT);"
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except:
            None

    def log(self, activity, information, suspicious, username="None"):
        self.cur.execute("SELECT * FROM log")
        i = len(self.cur.fetchall())
        if (i == 0):
            no = 1
        else:
            no = self.cur.execute(
                "SELECT no FROM log").fetchall()[-1][0] + 1
        dt = datetime.datetime.now()
        date = dt.strftime('%d/%m/%Y')
        time = dt.strftime('%H:%M:%S')
        encr = cipher.Cipher.encrypt
        self.cur.execute(
            f'INSERT INTO log (no, username, date, time, activity, information, suspicious) VALUES ({no}, "{encr(username)}", "{encr(date)}", "{encr(time)}", "{encr(activity)}", "{encr(information)}", "{encr(suspicious)}")')
        self.conn.commit()

    def login(self):
        username = input("please enter username: ").lower()
        password = input("please enter password: ")

        sql_statement = (
            "SELECT * from users WHERE username=? AND password=?")

        try:
            self.cur.execute(sql_statement, (username, password))
        except:
            pass

        loggedin_user = self.cur.fetchone()
        if not loggedin_user:  # An empty result evaluates to False.
            print("Login failed")
            self.log("unsuccesfull login",
                     f"Password: {password} is tried in combinaton with username: {username}", "yes", username)
            self.logAlert = 1
        else:
            self.loggedin = 1
            self.loggedin_user = username
            self.admin = loggedin_user[3]
            self.log("succesfull login", "", "no", username)
            if (loggedin_user[4] == 1):
                self.updatePassword()

        if self.admin == 0:
            # advisor
            header = '''
 ________________________________________
|                                        |
|     you are logged in as an advisor    |
|________________________________________|

'''
            advisor_interface = ui.UI(header, [
                [1, "update password", self.updatePassword],
                [2, "add a client", self.addClient],
                [3, "modify client data", self.modifyClient],
                [4, "search client data", self.searchClient],
                [0, "logout", self.logout]
            ])
            advisor_interface.run()
        elif self.admin == 1:
            # system admin
            if (self.logAlert == 0):
                header = '''
 ________________________________________
|                                        |
|   you are logged in as a system admin  |
|________________________________________|

                '''
            else:
                header = '''
 ________________________________________
|                                        |
|   you are logged in as a system admin  |
|                                        |
|         THERE IS A LOG ALERT           |
|________________________________________|

'''
            systemadmin_interface = ui.UI(header, [
                [1, "update password", self.updatePassword],
                [2, "add a client", self.addClient],
                [3, "modify client data", self.modifyClient],
                [4, "search client data", self.searchClient],
                [5, "delete a cleint", self.deleteClient],
                [6, "search all users", self.searchUsers],
                [7, "add an advisor", self.addAdvisor],
                [8, "modify advisor data", self.modifyAdvisor],
                [9, "delete an advisor", self.deleteAdvisor],
                [10, "reset an avisor's password", self.resetAdvisorPassword],
                [11, "make a backup", self.createBackup],
                [12, "show the logs", self.showLogs],
                [0, "logout", self.logout]
            ])

            systemadmin_interface.run()
        elif self.admin == 2:
            # super admin
            if (self.logAlert == 0):
                header = '''
 ________________________________________
|                                        |
|   you are logged in as a super admin   |
|________________________________________|

                '''
            else:
                header = '''
 ________________________________________
|                                        |
|   you are logged in as a super admin   |
|                                        |
|         THERE IS A LOG ALERT           |
|________________________________________|

'''
            superadmin_interface = ui.UI(header, [
                [1, "update password", self.updatePassword],
                [2, "add a client", self.addClient],
                [3, "modify client data", self.modifyClient],
                [4, "search client data", self.searchClient],
                [5, "delete a cleint", self.deleteClient],
                [6, "search all users", self.searchUsers],
                [7, "add an advisor", self.addAdvisor],
                [8, "modify advisor data", self.modifyAdvisor],
                [9, "delete an advisor", self.deleteAdvisor],
                [10, "reset an avisor's password", self.resetAdvisorPassword],
                [11, "make a backup", self.createBackup],
                [12, "show the logs", self.showLogs],
                [13, "add a system admin", self.addSystemAdmin],
                [14, "modify system admin", self.modifySystemAdmin],
                [15, "delete a system admin", self.deleteSystemAdmin],
                [16, "reset an admin's password", self.resetAdminPassword],
                [0, "logout", self.logout]
            ])
            superadmin_interface.run()

    def updatePassword(self):
        sql_statement = "UPDATE users SET password='%s', temp=0 WHERE username='%s'"
        newPassword = advisor.Advisor.updatePassword()
        try:
            self.cur.execute(sql_statement % (newPassword, self.loggedin_user))
            self.conn.commit()
            print("your password has been changed")
            self.log("updated password", "", "no", self.loggedin_user)
        except OperationalError:
            self.log("unsuccesfull password change",
                     f"password input: {newPassword}", "yes", self.loggedin_user)
            self.logAlert = 1

    def addClient(self):
        fullname, address, email, phoneNumber = advisor.Advisor.addClient(self)
        self.cur.execute("SELECT * FROM client")
        i = len(self.cur.fetchall())
        if (i == 0):
            no = 1
        else:
            no = self.cur.execute(
                "SELECT person_id FROM client").fetchall()[-1][0] + 1
        encr = cipher.Cipher.encrypt
        sql_statement = 'INSERT INTO client (person_id, fullname, address, email, phone) VALUES (%i, "%s", "%s", "%s", "%s")'
        try:
            self.cur.execute(sql_statement %
                             (no, encr(fullname), encr(address), encr(email), encr(phoneNumber)))
            self.conn.commit()
            self.log("added client", str(no) + ": " +
                     fullname, "no", self.loggedin_user)
        except OperationalError:
            self.log("unsuccesfull adding of client",
                     f"fullname: {fullname}, address: {address}, email: {email}, phone number: {phoneNumber}", "yes", self.loggedin_user)
            self.logAlert = 1

    def modifyClient(self):
        ids = self.cur.execute("SELECT person_id FROM client").fetchall()
        ids = [str(row[0]) for row in ids]
        ids.append("0")
        idInput = input("enter the client ID or enter [0] to exit: ")
        decr = cipher.Cipher.decrypt
        encr = cipher.Cipher.encrypt
        while (idInput not in ids):
            idInput = input(
                "invalid input, enter the client ID or enter [0] to exit: ")
        while (True):
            if (idInput != "0"):
                client = list(self.cur.execute(
                    f"SELECT * FROM client WHERE person_id={idInput}").fetchall()[0])
                client[1] = decr(client[1])
                client[2] = decr(client[2])
                client[3] = decr(client[3])
                client[4] = decr(client[4])
                advisor.Advisor.modifyClient(client)

                # put client in db and log
                sql_statement = "UPDATE client SET fullname='%s', address='%s', email='%s', phone='%s' WHERE person_id='%i'"
                try:
                    self.cur.execute(sql_statement % (
                        encr(client[1]), encr(client[2]), encr(client[3]), encr(client[4]), int(idInput)))
                    self.conn.commit()
                    self.log("updated client", "client_no: " +
                             idInput, "no", self.loggedin_user)
                    print("clien will be modified")
                except OperationalError:
                    self.log("unsuccesfull modification of client",
                             f"fullname: {client[1]}, address: {client[2]}, email: {client[3]}, phone number: {client[4]}", "yes", self.loggedin_user)
                    self.logAlert = 1
            elif (idInput == "0"):
                break
            idInput = input("enter the client ID or enter [0] to exit: ")
            while (idInput not in ids):
                idInput = input(
                    "invalid input, enter the client ID or enter [0] to exit: ")

    def searchClient(self):
        clients = self.cur.execute("SELECT * FROM client").fetchall()
        decr = cipher.Cipher.decrypt
        names = [decr(row[1]).lower() for row in clients]
        names.append("0")
        nameInput = input(
            "please enter the client's full name to see its info (enter [0] to exit): ").lower()
        while (nameInput not in names):
            nameInput = input(
                "invalid input, please enter the client's full name to see its info (enter [0] to exit): ").lower()
        while (True):
            if (nameInput == "0"):
                break
            # show data
            index = names.index(nameInput)
            client = list(clients[index])
            client[1] = decr(client[1])
            client[2] = decr(client[2])
            client[3] = decr(client[3])
            client[4] = decr(client[4])
            print(
                f"full name: {client[1]}\naddress: {client[2]}\nemail: {client[3]}\nphone number: {client[4]}")
            nameInput = input(
                "please enter the client's full name to see its info (enter [0] to exit): ").lower()
            while (nameInput != "0" or nameInput not in names):
                nameInput = input(
                    "invalid input, please enter the client's full name to see its info (enter [0] to exit): ").lower()

    def deleteClient(self):
        sql_statement = "DELETE FROM client WHERE person_id='%i'"
        fetch_name = "SELECT fullname FROM client WHERE person_id='%i'"
        clientids = list(self.cur.execute(
            "SELECT person_id FROM client").fetchall())
        ids = [str(row[0]) for row in clientids]
        ids.append("0")
        idInput = input(
            "please enter the client's id (enter [0] to exit): ")
        decr = cipher.Cipher.decrypt
        while (idInput not in ids):
            idInput = input(
                "invalid input, please enter the client's id (enter [0] to exit): ")
        while (True):
            if (idInput == '0'):
                break
            try:
                fullname = fullname = self.cur.execute(
                    fetch_name % (int(idInput))).fetchall()[0][0]
                fullname = decr(fullname)
                self.cur.execute(sql_statement %
                                 (int(idInput)))
                self.conn.commit()
                self.log("reoved client", str(idInput) + ": " +
                         fullname, "no", self.loggedin_user)
                print("Client has been removed")
            except OperationalError:
                self.log("unsuccesfull removing of client",
                         f"person_id: {idInput}", "yes", self.loggedin_user)
                self.logAlert = 1
            idInput = input(
                "please enter the client's id (enter [0] to exit): ")
            while (idInput not in ids):
                idInput = input(
                    "invalid input, please enter the client's id (enter [0] to exit): ")

    def searchUsers(self):
        users = self.cur.execute(
            "SELECT username, fullname FROM users").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the user's username to see its info (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the user's username to see its info (enter [0] to exit): ").lower()
        while (True):
            if (usernameInput == "0"):
                break
            # show data
            index = usernames.index(usernameInput)
            user = users[index]
            print(
                f"username: {user[0]}\nfullname: {user[1]}\n")
            usernameInput = input(
                "please enter the user's username to see its info (enter [0] to exit): ").lower()
            while (usernameInput != "0" or usernameInput not in usernames):
                usernameInput = input(
                    "invalid input, please enter the user's username to see its info (enter [0] to exit): ").lower()

    def addAdvisor(self):
        users = self.cur.execute(
            "SELECT username, fullname FROM users").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        username, password, fullname = systemadmin.Systemadmin.addAdvisor(
            usernames)
        sql_statement = "INSERT INTO users (username, password, fullname, admin, temp) VALUES ('%s', '%s', '%s', 0, 1)"
        try:
            self.cur.execute(sql_statement %
                             (username, password, fullname))
            self.conn.commit()
            self.log("added advisor", username + ": " +
                     fullname, "no", self.loggedin_user)
            print("admin has been added")
        except OperationalError:
            self.log("unsuccesfull adding of advisor",
                     f"username: {username}, full name: {fullname}", "yes", self.loggedin_user)
            self.logAlert = 1

    def modifyAdvisor(self):
        users = self.cur.execute(
            "SELECT username, fullname FROM users WHERE admin=0").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the advisor's username to modify data (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the advisor's username to modify data (enter [0] to exit): ").lower()
        while (True):
            if (usernameInput == "0"):
                break
            advisor = list(self.cur.execute(
                f"SELECT * FROM users WHERE username='{usernameInput}'").fetchall()[0])
            choice = systemadmin.Systemadmin.modifyAdvisorChoice()
            while (True):
                if (choice == 0):
                    break
                elif (choice == 1):
                    advisor[0] = systemadmin.Systemadmin.username(usernames)
                elif (choice == 2):
                    advisor[2] = systemadmin.Systemadmin.fullname()
                choice = systemadmin.Systemadmin.modifyAdvisorChoice()

            # put client in db and log
            sql_statement = "UPDATE users SET username='%s', fullname='%s' WHERE username='%s'"
            try:
                self.cur.execute(sql_statement % (
                    advisor[0], advisor[2], usernameInput))
                self.conn.commit()
                self.log("updated advisor", "old username " +
                         usernameInput, "no", self.loggedin_user)
                print("Advisor will be updated")
            except OperationalError:
                self.log("unsuccesfull modification of advisor",
                         f"username: {advisor[0]}, fullname: {advisor[2]}", "yes", self.loggedin_user)
                self.logAlert = 1
            usernameInput = input(
                "please enter the advisor's username to modify data (enter [0] to exit): ").lower()
            while (usernameInput not in usernames):
                usernameInput = input(
                    "invalid input, please enter the advisor's username to modify data (enter [0] to exit): ").lower()

    def deleteAdvisor(self):
        sql_statement = "DELETE FROM users WHERE username='%s'"
        fetch_name = "SELECT fullname FROM users WHERE username='%s'"
        users = self.cur.execute(
            "SELECT username, fullname FROM users WHERE admin=0").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the username of the advisor you want to delete (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the username of the advisor you want to delete (enter [0] to exit): ").lower()
        while (True):
            if (usernameInput == "0"):
                break
            try:
                fullname = self.cur.execute(
                    fetch_name % (usernameInput)).fetchall()[0][0]
                self.cur.execute(sql_statement %
                                 (usernameInput))
                self.conn.commit()
                self.log("removed advisor", "username: " + usernameInput + " - fullname: " +
                         fullname, "no", self.loggedin_user)
                print("Advisor has been removed")
            except OperationalError:
                self.log("unsuccesfull removing of advisor",
                         f"usernameInput: " + usernameInput, "yes", self.loggedin_user)
                self.logAlert = 1
            usernameInput = input(
                "please enter the username of the advisor you want to delete (enter [0] to exit): ").lower()
            while (usernameInput not in usernames):
                usernameInput = input(
                    "invalid input, please enter the username of the advisor you want to delete (enter [0] to exit): ").lower()

    def resetAdvisorPassword(self):
        sql_statement = "UPDATE users SET password='%s', temp=1 WHERE username='%s'"
        users = self.cur.execute(
            "SELECT username, fullname FROM users WHERE admin=0").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the username of the advisor who's password you want to change (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the username of the advisor who's password you want to change (enter [0] to exit): ").lower()
        newPassword = advisor.Advisor.updatePassword()
        try:
            self.cur.execute(sql_statement %
                             (newPassword, usernameInput))
            self.conn.commit()
            self.log("reset advisor password", "username: " +
                     usernameInput, "no", self.loggedin_user)
            print("Advisor has been removed")
        except OperationalError:
            self.log("unsuccesfull reset of advisor password",
                     f"usernameInput: " + usernameInput + "passwordInput: " + newPassword, "yes", self.loggedin_user)
            self.logAlert = 1

    def addSystemAdmin(self):
        users = self.cur.execute(
            "SELECT username, fullname FROM users").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        username, password, fullname = systemadmin.Systemadmin.addAdvisor(
            usernames)
        sql_statement = "INSERT INTO users (username, password, fullname, admin, temp) VALUES ('%s', '%s', '%s', 1, 1)"
        try:
            self.cur.execute(sql_statement %
                             (username, password, fullname))
            self.conn.commit()
            self.log("added system admin", username + ": " +
                     fullname, "no", self.loggedin_user)
            print("admin has been added")
        except OperationalError:
            self.log("unsuccesfull adding of system admin",
                     f"username: {username}, full name: {fullname}", "yes", self.loggedin_user)
            self.logAlert = 1

    def modifySystemAdmin(self):
        users = self.cur.execute(
            "SELECT username, fullname FROM users WHERE admin=1").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the admin's username to modify data (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the admin's username to modify data (enter [0] to exit): ").lower()
        while (True):
            if (usernameInput == "0"):
                break
            admin = list(self.cur.execute(
                f"SELECT * FROM users WHERE username='{usernameInput}'").fetchall()[0])
            choice = systemadmin.Systemadmin.modifyAdvisorChoice()
            while (True):
                if (choice == 0):
                    break
                elif (choice == 1):
                    admin[0] = systemadmin.Systemadmin.username(usernames)
                elif (choice == 2):
                    admin[2] = systemadmin.Systemadmin.fullname()
                choice = systemadmin.Systemadmin.modifyAdvisorChoice()

                # put client in db and log
            sql_statement = "UPDATE users SET username='%s', fullname='%s' WHERE username='%s'"
            try:
                self.cur.execute(sql_statement % (
                    admin[0], admin[2], usernameInput))
                self.conn.commit()
                self.log("updated admin", "old username " +
                         usernameInput, "no", self.loggedin_user)
                print("admin will be updated")
            except OperationalError:
                self.log("unsuccesfull modification of admin",
                         f"username: {admin[0]}, fullname: {admin[2]}", "yes", self.loggedin_user)
                self.logAlert = 1
            usernameInput = input(
                "please enter the admin's username to modify data (enter [0] to exit): ").lower()
            while (usernameInput not in usernames):
                usernameInput = input(
                    "invalid input, please enter the admin's username to modify data (enter [0] to exit): ").lower()

    def deleteSystemAdmin(self):
        sql_statement = "DELETE FROM users WHERE username='%s'"
        fetch_name = "SELECT fullname FROM users WHERE username='%s'"
        users = self.cur.execute(
            "SELECT username, fullname FROM users WHERE admin=1").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the username of the admin you want to delete (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the username of the admin you want to delete (enter [0] to exit): ").lower()
        while (True):
            if (usernameInput == "0"):
                break
            try:
                fullname = self.cur.execute(
                    fetch_name % (usernameInput)).fetchall()[0][0]
                self.cur.execute(sql_statement %
                                 (usernameInput))
                self.conn.commit()
                self.log("removed admin", "username: " + usernameInput + " - fullname: " +
                         fullname, "no", self.loggedin_user)
                print("admin has been removed")
            except OperationalError:
                self.log("unsuccesfull removing of admin",
                         f"usernameInput: " + usernameInput, "yes", self.loggedin_user)
                self.logAlert = 1
            usernameInput = input(
                "please enter the username of the admin you want to delete (enter [0] to exit): ").lower()
            while (usernameInput not in usernames):
                usernameInput = input(
                    "invalid input, please enter the username of the admin you want to delete (enter [0] to exit): ").lower()

    def resetAdminPassword(self):
        sql_statement = "UPDATE users SET password='%s', temp=1 WHERE username='%s'"
        users = self.cur.execute(
            "SELECT username, fullname FROM users WHERE admin=1").fetchall()
        usernames = [str(row[0]).lower() for row in users]
        usernames.append("0")
        usernameInput = input(
            "please enter the username of the admin who's password you want to change (enter [0] to exit): ").lower()
        while (usernameInput not in usernames):
            usernameInput = input(
                "invalid input, please enter the username of the admin who's password you want to change (enter [0] to exit): ").lower()
        newPassword = advisor.Advisor.updatePassword()
        try:
            self.cur.execute(sql_statement %
                             (newPassword, usernameInput))
            self.conn.commit()
            self.log("reset admin password", "username: " +
                     usernameInput, "no", self.loggedin_user)
            print("password has been reset")
        except OperationalError:
            self.log("unsuccesfull reset of admin password",
                     f"usernameInput: " + usernameInput + "passwordInput: " + newPassword, "yes", self.loggedin_user)
            self.logAlert = 1

    def createBackup(self):
        filePath = 'backup.zip'
        zip = zipfile.ZipFile(filePath, 'w')
        zip.write('mycompany.db')
        zip.close()

    def showLogs(self):
        self.logAlert = 0
        log = self.cur.execute(
            "SELECT * FROM log").fetchall()
        decr = cipher.Cipher.decrypt
        for row in log:
            print("\"%i\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"" % (row[0], decr(
                row[1]), decr(row[2]), decr(row[3]), decr(row[4]), decr(row[5]), decr(row[6])))
        input("PRESS ENTER TO CONTINUE")

    def logout(self):
        self.loggedin = 0
        self.loggedin_user = None
        self.admin_is_loggedin = 0

    def close(self):
        self.conn.close()
