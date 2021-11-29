from sqlite3.dbapi2 import OperationalError


class UI:
    def __init__(self, header, menuitems):
        self.header = header
        self.menuitems = menuitems
        self.menuoptions = [option[0] for option in self.menuitems]
        self.menufunctions = [option[2] for option in self.menuitems]

    def menu_display(self):
        print(self.header)
        for option in self.menuitems:
            print('[' + str(option[0]) + ']' + ' ' + option[1])

    def run(self):
        self.menu_display()
        try:
            option = int(
                input('please select the number of the option you would like to select: '))
            print()
        except:
            option = -1
            print()

        while (option != self.menuoptions[-1]):
            if option in self.menuoptions:
                self.menuitems[self.menuoptions.index(option)][2]()

            else:
                print('invalid option')

            print()
            self.menu_display()
            try:
                option = int(input('choose a number from the menu: '))
                print()
            except:
                option = -1
                print()
