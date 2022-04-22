import Flight
from Flight import *
import time

import GateKiosk
from UI import *


def display_passenger_list(look_at, title="PASSENGER LIST"):
    def related(lst, index1, index2):
        if index1 < 0 or index2 >= len(lst):
            return False
        if isinstance(lst[index1], DisabledPassenger) and isinstance(lst[index2], AttendantPassenger) and \
                lst[index1].attendant is lst[index2]:
            return True
        elif isinstance(lst[index1], AttendantPassenger) and isinstance(lst[index2], DisabledPassenger) and \
                lst[index2].attendant is lst[index1]:
            return True
        elif isinstance(lst[index1], ParentPassenger) and isinstance(lst[index2], ParentPassenger) and \
                lst[index1].spouse is lst[index2]:
            return True
        elif isinstance(lst[index1], ParentPassenger) and isinstance(lst[index2], ChildPassenger) and \
                lst[index2] in lst[index1].children:
            return True
        elif isinstance(lst[index2], ParentPassenger) and isinstance(lst[index1], ChildPassenger) and \
                lst[index1] in lst[index2].children:
            return True
        elif isinstance(lst[index1], ChildPassenger) and isinstance(lst[index2], ChildPassenger) and \
                lst[index1].__parent__ is lst[index2].__parent__:
            return True
        return False

    lLen = 4
    fLen = 5
    bLen = 14
    for passenger in look_at:
        if len(passenger.first_name) > fLen:
            fLen = len(passenger.first_name)
        if len(passenger.last_name) > lLen:
            lLen = len(passenger.last_name)
        if len(passenger.boarding_group()) > bLen:
            bLen = len(passenger.boarding_group())
    for i in range(100):
        print()
    top = "    ------ --- " + "--------------".rjust(bLen, "-") + " " + "".rjust(lLen, "-") + " " + "".rjust(fLen, "-")
    print("".rjust(len(top), "─"))
    print(styled("Passenger List Banner", "".center(len(top))))
    print(styled("Passenger List Banner", title.center(len(top))))
    print(styled("Passenger List Banner", "".center(len(top))))
    print()
    print("Business Select Seats Available:",
          styled(styles["Outlined"], ' ' + str(business_select_seats_available()).rjust(3) + ' ') + " / 15")
    print(" Wanna get Away Seats Available:",
          styled(styles["Outlined"], ' ' + str(wanna_get_away_seats_available()).rjust(3) + ' ') + " /135")
    print()
    time.sleep(1)
    print("    " + styled("Column Header", "CONF #"), styled("Column Header", "BID"),
          styled("Column Header", "Boarding Group".rjust(bLen)),
          styled("Column Header", "Last".rjust(lLen, " ")), styled("Column Header", "First".rjust(fLen)))
    count = 1
    look_at.sort()
    prev_passenger = None
    for i in range(len(look_at)):
        passenger = look_at[i]
        if i < len(look_at) - 1 and passenger.boarding_group() != look_at[i + 1].boarding_group() or i == len(
                look_at) - 1:
            print(styled(styles["Underlined"],
                         str(count).rjust(3) + ' ' + passenger.confirmation_id + ' ' + passenger.boarding_id.rjust(
                             3) + ' ' +
                         passenger.boarding_group().rjust(bLen) + ' ' + passenger.last_name.rjust(lLen) + ' ' +
                         passenger.first_name.rjust(fLen)), end="")
            if i < len(look_at) - 1:
                time.sleep(1)
        else:
            print(str(count).rjust(3), passenger.confirmation_id, passenger.boarding_id.rjust(3),
                  passenger.boarding_group().rjust(bLen), passenger.last_name.rjust(lLen),
                  passenger.first_name.rjust(fLen), end="")
            # if prev_passenger is not None:
        if related(look_at, i-1, i):
            if related(look_at, i, i+1):
                print(" │", end="")
            else:
                print(" ╯", end="")
        elif related(look_at, i, i+1):
            print(" ╮", end="")
        else:
            print("  ", end="")
        if isinstance(passenger, ChildPassenger):
            print(" 👶")
        elif isinstance(passenger, DisabledPassenger):
            print(" ♿")
        else:
            print()
        count += 1
        prev_passenger = passenger
    input(styled("Inverted", "DOUBLE TAP TO ENTER TO CONTINUE".center(len(top))))


main_menu = Menu("Main Menu", {1: "Book Seats",
                               2: "Open Check-In Window",
                               3: "Gate Kiosk Window",
                               4: "View My Reservations",
                               5: "View All Passengers",
                               6: "Boarding Window",
                               7: "Reset Flight",
                               'X': "Exit"}, exit_value='X')
while True:
    main_menu.menu_item(2).set_disabled(check_in_begun())
    main_menu.menu_item(4).set_disabled(len(get_my_passenger_list()) == 0)
    main_menu.menu_item(3).set_disabled(not check_in_begun())
    main_menu.menu_item(6).set_disabled(not check_in_begun())

    choice = main_menu.show(">>>Choice: ")
    if choice == main_menu.invalid_return_value:
        main_menu.set_message("✗ Invalid Input!", "Error")
    elif choice == main_menu.not_available_return_value:
        main_menu.set_message("✗ Menu Option Not Available!", "Caution")
    elif choice == main_menu.exit_value:
        break
    elif choice == 1:
        if book_seats():
            main_menu.set_message("✓ Successfully Booked Seats", "Confirmation")
        else:
            main_menu.set_message("✗ Booking was aborted!", "Error")
    elif choice == 2:
        Flight.open_check_in_window()
        main_menu.set_message("✓  Check-in Window Opened", "Information")
    elif choice == 3:
        GateKiosk.show_menu()
    elif choice == 4:
        display_passenger_list(get_my_passenger_list(), "MY PASSENGER LIST")
    elif choice == 5:
        display_passenger_list(get_passenger_list())
    elif choice == 6:
        pass
        # TODO Takes passengers from get_passenger_list() and randomly inserts them into the priority queue
    elif choice == 7:
        # resets flight. All custom passengers will be lost.
        reset_flight()
        main_menu.set_message("✓ Flight has been reset!", "Information")
    # time.sleep(2)
