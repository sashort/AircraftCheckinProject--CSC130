import Flight
import time


def display_passenger_list(look_at):
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
    print("PASSENGER LIST".center(len(top)))
    print("Business Select Seats Available:", str(Flight.business_select_seats_available()).rjust(3) + "/ 15")
    print(" Wanna get Away Seats Available:", str(Flight.wanna_get_away_seats_available()).rjust(3) + "/135")
    time.sleep(.5)
    print()
    print("    CONF #", "BID", "Boarding Group".rjust(bLen), "Last".rjust(lLen, " "), "First".rjust(fLen))
    print(top)
    count = 1
    look_at.sort()
    for passenger in look_at:
        print(str(count).rjust(3), passenger.confirmation_id, passenger.boarding_id.rjust(3), passenger.boarding_group().rjust(bLen), passenger.last_name.rjust(lLen), passenger.first_name.rjust(fLen))
        count += 1
    print("".rjust(len(top), "-"))
    input("PRESS ANY KEY TO RETURN TO MAIN MENU")


message = ""
while True:
    for i in range(300):
        print("")
    if message != "":
        print(message + '\n')
        message = ""
    print("MAIN MENU".center(26, "-"))
    print("1 Book seats")
    print("---------------------------")
    if not Flight.check_in_begun():
        print("2 Open Check-In Window")
    print("3 Gate Kiosk Menu")
    print("---------------------------")
    if len(Flight.get_my_passenger_list()) > 0:
        print("4 View My Flight Info")
    print("5 View All Flight Info")
    print("---------------------------")
    print("6 Board Passengers")
    print("---------------------------")
    print("7 Reset Flight")
    print("0 Exit")
    print("Boarding FAQ can be found at https://www.southwest.com/help/day-of-travel/boarding-process")

    value = input("\nCHOICE >>>  ")
    if value == "1":
        if Flight.book_seats():
            message = "Succesfully Booked Seats!"
        else:
            message = "Booking was aborted."
    elif value == "2":
        if Flight.open_check_in_window():
            message = "Check-in Window Opened"
        else:
            message = "Check-in Window already Open"
    elif value == "3":
        pass
        #TODO links with gate kiosk. Here you can upgrade passengers to Business Select and Disabled people can request "Extra Time" status
    elif value == "4":
        display_passenger_list(Flight.get_my_passenger_list())
    elif value == "5":
        display_passenger_list(Flight.get_passenger_list())
    elif value == "6":
        pass
        # TODO Takes passengers from Flight.get_passenger_list() and randomly inserts them into the priority queue
    elif value == "7":
        # resets flight. All custom passengers will be lost.
        Flight.reset_flight()
        message = "Flight has been reset!"
    elif value == "8":
        print(Flight.__boarding_ids__)
    elif value == "0":
        break
    # time.sleep(2)


