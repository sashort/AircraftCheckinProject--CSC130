import Flight
import time
from UI import *

passenger_dict = Flight.get_passenger_dict()
passenger = Flight.get_my_passenger_list()


def show_menu():
    main_menu = Menu("Gate Kiosk Menu", {0: "Exit",
                                         1: "Upgrade Seats",
                                         2: "Add Extra Boarding Time"}, exit_value=0, invalid_return_value=-1)
    message = None
    choice = -2
    while True:
        choice = main_menu.show(message=message, prompt=">>>Choice: ", center_message=True,
                                error=choice == main_menu.invalid_return_value)
        message = None
        main_menu.set_theme(None)

        if choice == 1:
            if upgrade_passenger():
                message = "Successfully Seats Upgrade"
                main_menu.set_theme(themes["Info Message"])
            else:
                message = "Unintelligible For Upgrade"
                main_menu.set_theme(themes["Error Message"])
        elif choice == 2:
            if grant_extra_time():
                message = "Extra Time Added"
                main_menu.set_theme(themes["Info Message"])
            else:
                message = "Unintelligible For Extra Time"
                main_menu.set_theme(themes["Error Message"])
        elif choice == main_menu.invalid_return_value:
            message = "Invalid Input!"
            main_menu.set_theme(themes["Error Message"])
        elif choice == main_menu.exit_value:
            break


def upgrade_passenger():
    for p in passenger:
        for p1 in passenger_dict:
            if p1.__eq__(p):
                return p.upgrade()

    return False


def grant_extra_time():
    for p in passenger:
        for p1 in passenger_dict:
            if p1.__eq__(p):
                if isinstance(p, Flight.DisabledPassenger):
                    return p.request_extra_time()
    else:
        return False
