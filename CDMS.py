from os import close, system
import db
import input_handling
import ui

company_db_name = 'mycompany.db'
client_tb_name = 'client'
users_tb_name = 'users'

welcome_message = '''
 ________________________________________
|                                        |
|                                        |
|                WELCOME                 |
|  to our Client Data Management System  |
|                                        |
|                                        |
|________________________________________|

'''

database = db.db(company_db_name, company_db_name, users_tb_name)

main_interface = ui.UI(welcome_message, [
    [1, "login", database.login],
    [0, "exit", database.close]
])

main_interface.run()
