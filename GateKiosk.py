from Flight import *
from UI import *

passenger_dict = get_passenger_dict()
kiosk_menu = Menu("Gate Kiosk Menu", {1: "Upgrade to Business Select",
                                      2: "Request Extra Boarding Time",
                                      'X': "Return to Main Menu"}, exit_value='X', invalid_return_value=-1)


def show_menu():
    while True:
        choice = kiosk_menu.show(">>>Choice: ")
        if choice == 1:
            upgrade_passenger()
        elif choice == 2:
            grant_extra_time()
        elif choice == kiosk_menu.invalid_return_value:
            kiosk_menu.set_message("Invalid Input!", "Error")
        elif choice == kiosk_menu.exit_value:
            break


def upgrade_passenger():
    passenger_id = input("Enter Passenger Confirmation ID: ")
    if passenger_id in passenger_dict.keys():
        my_passenger = passenger_dict[passenger_id]
        if my_passenger.is_business_select:
            kiosk_menu.set_message("Passenger Already Business Select", styles["Caution"])
        elif isinstance(my_passenger, DisabledPassenger) or \
                isinstance(my_passenger, AttendantPassenger) or \
                isinstance(my_passenger, ParentPassenger) or \
                isinstance(my_passenger, ChildPassenger):
            kiosk_menu.set_message("Passenger Not Eligible\nfor Business Select", styles["Error"])
        elif business_select_seats_available() == 0:
            kiosk_menu.set_message("No Business Select Seats Available", styles["Error"])
        elif passenger_dict[passenger_id].upgrade():
            kiosk_menu.set_message(
                "Passenger Upgraded To Business Select\nNew Boarding ID: " + passenger_dict[passenger_id].boarding_id,
                styles["Confirmation"])
    else:
        kiosk_menu.set_message("Invalid Confirmation Number", styles["Error"])


def grant_extra_time():
    passenger_id = input("Enter Passenger Confirmation ID: ")
    if passenger_id in passenger_dict.keys():
        my_passenger = passenger_dict[passenger_id]
        if isinstance(my_passenger, DisabledPassenger):
            if my_passenger.extra_time:
                kiosk_menu.set_message("Passenger Already Granted Extra Time", styles["Caution"])
            elif my_passenger.request_extra_time():
                kiosk_menu.set_message("Extra Time Granted For Passenger", styles["Confirmation"])
            else:
                kiosk_menu.set_message("Extra Time Denied For Passenger", styles["Error"])
        else:
            kiosk_menu.set_message("Passenger Not Eligible\nfor Extra Time", styles["Error"])
    else:
        kiosk_menu.set_message("Invalid Confirmation Number", styles["Error"])
