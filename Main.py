import Flight
import time


def display_passenger_list(look_at):
    lLen = 0
    fLen = 0
    bLen = 3
    for passenger in look_at:
        if len(passenger.first_name) > fLen:
            fLen = len(passenger.first_name)
        if len(passenger.last_name) > lLen:
            lLen = len(passenger.last_name)
        if len(passenger.boarding_group()) > bLen:
            bLen = len(passenger.boarding_group())
    top = "------ --- " + "--------------".rjust(bLen, "-") + " " + "".rjust(lLen, "-") + " " + "".rjust(fLen, "-")
    print("".rjust(len(top), "-"))
    print("PASSENGER LIST".center(len(top)))
    print("Business Select Seats Available:", Flight.business_select_seats_available())
    print(" Wanna get Away Seats Available:", Flight.wanna_get_away_seats_available())
    time.sleep(2)
    print()
    print("CONF #", "BID", "Boarding Group".rjust(bLen), "Last".rjust(lLen, " "), "First".rjust(fLen))
    print(top)
    for passenger in look_at:
        print(passenger.confirmation_id, passenger.boarding_id.rjust(3), passenger.boarding_group().rjust(bLen), passenger.last_name.rjust(lLen), passenger.first_name.rjust(fLen))
    print("".rjust(len(top), "-"))
    input("PRESS ANY KEY TO RETURN TO MAIN MENU")


while True:
    for i in range(300):
        print("")
    print("MAIN MENU".center(26, "-"))
    print("1 Book seats")
    print("---------------------------")
    print("2 Open Check-In Window")
    print("3 Gate Kiosk Menu")
    print("---------------------------")
    print("4 View My Flight Info")
    print("5 View All Flight Info")
    print("---------------------------")
    print("6 Board Passengers")
    print("---------------------------")
    print("7 Reset Flight")
    print("0 Exit")

    value = input("\nCHOICE >>>  ")
    if value == "1":
        Flight.book_seats()
    elif value == "2":
        Flight.open_check_in_window()
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
    elif value == "0":
        break


