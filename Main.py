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
    top = "    ------ --- " + "--------------".rjust(bLen, "-") + " " + "".rjust(lLen, "-") + " " + "".rjust(fLen, "-")
    print("".rjust(len(top), "-"))
    print(title.center(len(top)))
    print("Business Select Seats Available:", str(Flight.business_select_seats_available()).rjust(3) + "/ 15")
    print(" Wanna get Away Seats Available:", str(Flight.wanna_get_away_seats_available()).rjust(3) + "/135")
    time.sleep(.5)
    print()
    print("    CONF #", "BID", "Boarding Group".rjust(bLen), "Last".rjust(lLen, " "), "First".rjust(fLen))
    print(top)
    count = 1
    look_at.sort()
    for passenger in look_at:
        print(str(count).rjust(3), passenger.confirmation_id, passenger.boarding_id.rjust(3),
              passenger.boarding_group().rjust(bLen), passenger.last_name.rjust(lLen), passenger.first_name.rjust(fLen))
        count += 1
    print("".rjust(len(top), "-"))
    input("DOUBLE TAP TO ENTER TO MAIN MENU")


main_menu = Menu("Main Menu", {0: "Exit",
                               1: "Book Seats",
                               2: "Open Check-In Window",
                               3: "Gate Kiosk Window",
                               4: "View My Reservations",
                               5: "View All Passengers",
                               6: "Boarding Window",
                               7: "Reset Flight"})

message = None
while True:
    error_generated = False
    if message is not None and message.find("!") > -1:
        error_generated = True
    choice = main_menu.show(message=message, prompt=">>>Choice: ", center_message=True, message_style="Error Message" if error_generated else "Info Message")
    message = None
    if choice == 1:
        if Flight.book_seats():
            message = "Successfully Booked Seats"
        else:
            message = "Booking was aborted!"
    elif choice == 2:
        if Flight.open_check_in_window():
            message = "Check-in Window Opened"
        else:
            message = "Check-in Window already Open!"
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
        message = "Flight has been reset"
    elif choice == 0:
        break
    # time.sleep(2)
