import BoardingWindow
from Flight import *
import BookingWindow
import GateKiosk
import BookingWindow


main_menu = Menu("Main Menu", {1: "Book Seats",
                               2: "Open Check-In Window",
                               3: "Gate Kiosk Window",
                               4: "View My Reservations",
                               5: "View All Passengers",
                               6: "Boarding Window",
                               7: "Reset Flight",
                               'X': "Exit"}, exit_value='X')
while True:
    main_menu.menu_item(1).set_disabled(Flight.boarded())
    main_menu.menu_item(2).set_disabled(check_in_begun() or Flight.boarded())
    main_menu.menu_item(3).set_disabled(not check_in_begun() or Flight.boarded())
    main_menu.menu_item(4).set_disabled(len(get_my_passenger_list()) == 0 or Flight.boarded())
    main_menu.menu_item(5).set_disabled(Flight.boarded())
    main_menu.menu_item(6).set_disabled(not check_in_begun() or Flight.boarded())

    choice = main_menu.show(">>>Choice: ")
    if choice == main_menu.invalid_return_value:
        main_menu.set_message("✗ Invalid Input!", "Error")
    elif choice == main_menu.not_available_return_value:
        main_menu.set_message("✗ Menu Option Not Available!", "Caution")
    elif choice == main_menu.exit_value:
        break
    elif choice == 1:
        BookingWindow.show_menu()
    elif choice == 2:
        open_check_in_window()
        main_menu.set_message("✓  Check-in Window Opened", "Information")
    elif choice == 3:
        GateKiosk.show_menu()
    elif choice == 4:
        display_passenger_list(get_my_passenger_list(), "MY PASSENGER LIST")
    elif choice == 5:
        display_passenger_list(get_passenger_list())
    elif choice == 6:
        BoardingWindow.show_menu()
    elif choice == 7:
        # resets flight. All custom passengers will be lost.
        reset_flight()
        main_menu.set_message("✓ Flight has been reset!", "Information")
    # time.sleep(2)

for i in range(100):
    print()
print(styled("Bold", styled("Confirmation", "".center(100))))
print(styled("Bold", styled("Confirmation", "THANK YOU FOR CHOOSING NOT-CARDINAL DIRECTION AIRLINES".center(100))))
print(styled("Confirmation", "".center(100)))
print(styled("Passenger List Banner", "\tJamison Sasser - GateKiosk.py".ljust(97)))
print(styled("Passenger List Banner", "\tPeter Scott    - BoardingWindow.py".ljust(97)))
print(styled("Passenger List Banner", "\tS. Andy Short  - UI.py, BookingWindow.py".ljust(97)))
print(styled("Passenger List Banner", "\tStefan Slaczka - PassengerPriorityQueue.py".ljust(97)))
print(styled("Passenger List Banner", "\t       VARIOUS - Main.py, Flight.py".ljust(97)))
time.sleep(3)
