import Flight
import time
from UI import *


def display_passenger_list(look_at, title="PASSENGER LIST"):
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
          styled(styles["Outlined"], ' ' + str(Flight.business_select_seats_available()).rjust(3) + ' ') + " / 15")
    print(" Wanna get Away Seats Available:",
          styled(styles["Outlined"], ' ' + str(Flight.wanna_get_away_seats_available()).rjust(3) + ' ') + " /135")
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
        if i < len(look_at) - 1 and passenger.boarding_group() != look_at[i + 1].boarding_group() or i == len(look_at) - 1:
            print(styled(styles["Underlined"],
                         str(count).rjust(3) + ' ' + passenger.confirmation_id + ' ' + passenger.boarding_id.rjust(
                             3) + ' ' +
                         passenger.boarding_group().rjust(bLen) + ' ' + passenger.last_name.rjust(lLen) + ' ' +
                         passenger.first_name.rjust(fLen)))
            if i < len(look_at) - 1:
                time.sleep(1)
        else:
            print(str(count).rjust(3), passenger.confirmation_id, passenger.boarding_id.rjust(3),
                  passenger.boarding_group().rjust(bLen), passenger.last_name.rjust(lLen),
                  passenger.first_name.rjust(fLen))
            # if prev_passenger is not None:
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
                               'X': "Exit"}, exit_value='X', invalid_return_value=-1)

message = None
choice = -2
while True:
    choice = main_menu.show(message=message, prompt=">>>Choice: ", center_message=True)
    message = None
    main_menu.set_style(None)
    if choice == 1:
        if Flight.book_seats():
            message = "✓ Successfully Booked Seats"
            main_menu.set_style("Confirmation")
        else:
            message = "✗ Booking was aborted!"
            main_menu.set_style("Error")
    elif choice == 2:
        if Flight.open_check_in_window():
            message = "✓  Check-in Window Opened"
            main_menu.set_style("Information")
        else:
            message = "✗ Check-in Window already Open!"
            main_menu.set_style("Caution")
    elif choice == 3:
        pass
        # TODO links with gate kiosk. Here you can upgrade passengers to Business Select and Disabled people can request "Extra Time" status
    elif choice == 4:
        display_passenger_list(Flight.get_my_passenger_list(), "MY PASSENGER LIST")
    elif choice == 5:
        display_passenger_list(Flight.get_passenger_list())
    elif choice == 6:
        pass
        # TODO Takes passengers from Flight.get_passenger_list() and randomly inserts them into the priority queue
    elif choice == 7:
        # resets flight. All custom passengers will be lost.
        Flight.reset_flight()
        message = "✓ Flight has been reset!"
        main_menu.set_style("Information")
    elif choice == main_menu.invalid_return_value:
        message = "✗ Invalid Input!"
        main_menu.set_style("Error")
    elif choice == main_menu.exit_value:
        break
    # time.sleep(2)
