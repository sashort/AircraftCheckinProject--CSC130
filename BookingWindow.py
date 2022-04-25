from Flight import *
from UI import *

booking_menu = Menu("Select Ticket(s) Type", {1: "Business Select",
                                              2: "Disabled",
                                              3: "Family Tickets",
                                              4: "Regular Wanna Get Away Tickets",
                                              'X': "Return to Main Menu"}, exit_value='X')

assistive_device_menu = Menu("Do you have\nan assistive device?", {'Y': "Yes",
                                                                   'N': "No",
                                                                   'X': "Abort"}, exit_value='X')

attendant_menu = Menu("Will an attendant\nbe accompanying you?", {'Y': "Yes",
                                                                  'N': "No",
                                                                  'X': "Abort"}, exit_value='X')

spouse_menu = Menu("Will a spouse\nbe accompanying you?", {'Y': "Yes",
                                                           'N': "No",
                                                           'X': "Abort"}, exit_value='X')
child_count_menu = Menu("How Many Children?", {'X': "Abort"}, exit_value='X')
first_name_menu = Menu("", {'X': "Abort"}, exit_value='X')
last_name_menu = Menu("", {'X': "Abort"}, exit_value='X')


def show_menu():
    def show_business_select_menu():
        while True:
            last_name_menu.set_message("Your Information: Last Name")
            last = last_name_menu.show("Last Name: ", indent=2, sticky_message=True)
            if last == "X":
                booking_menu.set_message("Business Select Booking Aborted", "Error")
                return
            first_name_menu.set_message("Your Information: First Name")
            first = first_name_menu.show("First Name: ", indent=2, sticky_message=True)
            if first == "X":
                booking_menu.set_message("Business Select Booking Aborted", "Error")
                return
            get_my_passenger_list().append(Passenger(last, first, is_business_select=True))


def show_menu():
    def show_business_select_menu():
        while True:
            last_name_menu.set_message("Your Information: Last Name", "Information")
            last = last_name_menu.show("Last Name: ", indent=2, sticky_message=True, show_available_seats=True)
            if last == "X":
                booking_menu.set_message("Business Select Booking Aborted", "Error")
                return
            first_name_menu.set_message("Your Information: First Name", "Information")
            first = first_name_menu.show("First Name: ", indent=2, sticky_message=True, show_available_seats=True)
            if first == "X":
                booking_menu.set_message("Business Select Booking Aborted", "Error")
                return
            get_my_passenger_list().append(Passenger(last, first, is_business_select=True))
            booking_menu.set_message("Business Select Seat Booked", "Confirmation")
            break

    def show_gga_menu():
        while True:
            last_name_menu.set_message("Your Information: Last Name", "Information")
            last = last_name_menu.show("Last Name: ", indent=2, sticky_message=True, show_available_seats=True)
            if last == "X":
                booking_menu.set_message("Business Select Booking Aborted", "Error")
                return
            first_name_menu.set_message("Your Information: First Name", "Information")
            first = first_name_menu.show("First Name: ", indent=2, sticky_message=True, show_available_seats=True)
            if first == "X":
                booking_menu.set_message("Business Select Booking Aborted", "Error")
                return
            get_my_passenger_list().append(Passenger(last, first))
            booking_menu.set_message("Gotta Get Away\nSeat Booked", "Confirmation")
            break

    def show_disabled_menu():
        while True:
            attendant = attendant_menu.show(">>>Response: ", show_available_seats=True, indent=2)
            if attendant != attendant_menu.invalid_return_value:
                if attendant == "Y":
                    if wanna_get_away_seats_available() < 2:
                        attendant_menu.set_message("Not Enough Seats Available\nFor Attendant", "Caution")
                    else:
                        break
                else:
                    break
            else:
                attendant_menu.set_message("Invalid Response", "Error")
        if attendant == "X":
            booking_menu.set_message("Disabled Booking Aborted", "Error")
            return
        while True:
            assistive_device = assistive_device_menu.show(">>>Response: ", show_available_seats=True, indent=2)
            if assistive_device != assistive_device_menu.invalid_return_value:
                break
            else:
                assistive_device_menu.set_message("Invalid Response", "Error")
        if assistive_device == "X":
            booking_menu.set_message("Disabled Booking Aborted", "Error")
            return
        last_name_menu.set_message("Your Information: Last Name", "Information")
        last = last_name_menu.show("Last Name: ", indent=2, show_available_seats=True)
        if last == "X":
            booking_menu.set_message("Disabled Booking Aborted", "Error")
            return
        first_name_menu.set_message("Your Information: First Name", "Information")
        first = first_name_menu.show("First Name: ", indent=2, show_available_seats=True)
        if first == "X":
            booking_menu.set_message("Disabled Booking Aborted", "Error")
            return
        if attendant == "Y":
            last_name_menu.set_message("Attendant Information: Last Name\nLeave Blank To Use '" + last + "'",
                                       "Information")
            a_last = last_name_menu.show("Attendant Last Name: ", indent=2, show_available_seats=True,
                                         default_value=last)
            if a_last == "X":
                booking_menu.set_message("Disabled Booking Aborted", "Error")
                return
            first_name_menu.set_message("Attendant Information: First Name", "Information")
            a_first = first_name_menu.show("First Name: ", indent=2, show_available_seats=True)
            if a_first == "X":
                booking_menu.set_message("Disabled Booking Aborted", "Error")
                return
            a = AttendantPassenger(a_last, a_first)
            d = DisabledPassenger(last, first, assistive_device == "Y", a)
            a.elder = d
            d.attendant = a
            get_my_passenger_list().append(d)
            get_my_passenger_list().append(a)
            booking_menu.set_message("Disabled Passenger and\nAttendant Booked", "Confirmation")
        elif attendant == "N":
            get_my_passenger_list().append(DisabledPassenger(last, first, assistive_device == "Y"))
            booking_menu.set_message("Disabled Passenger Booked", "Confirmation")

    def show_family_menu():
        while True:
            total = 1
            child_count = child_count_menu.show(">>>Children: ", show_available_seats=True, indent=2)
            if isinstance(child_count, str):
                if child_count == child_count_menu.exit_value:
                    booking_menu.set_message("Family Booking Aborted", "Error")
                    return
                else:
                    child_count_menu.set_message("Invalid Number\nOf Children", "Error")
            elif child_count < 1:
                child_count_menu.set_message("Invalid Number\nOf Children", "Error")
            elif child_count + 1 > wanna_get_away_seats_available():
                child_count_menu.set_message("Not Enough Seats Available\nFor " + str(child_count) + " Children",
                                             "Caution")
            else:
                total += child_count
                break

        if str(child_count).upper() == "X":
            booking_menu.set_message("Family Booking Aborted", "Error")
            return
        while True:
            spouse = spouse_menu.show(">>>Response: ", show_available_seats=True, indent=2)
            if spouse != spouse_menu.invalid_return_value:
                if spouse == "Y":
                    if child_count + 2 > wanna_get_away_seats_available():
                        spouse_menu.set_message("Not Enough Seats Available\nFor You Spouse", "Caution")
                    else:
                        total += 1
                        break
                else:
                    break
            else:
                spouse_menu.set_message("Invalid Response", "Error")

        if spouse == "X":
            booking_menu.set_message("Family Booking Aborted", "Error")
            return
        else:
            name_list = list()
            for i in range(total):
                message_suffix = ""
                if i == 0:
                    message = "Your Information: "
                elif i == 1 and spouse == "Y":
                    message = "Spouse's Information: "
                    message_suffix = "\nLeave Blank to use '" + name_list[0] + "'"
                elif spouse == 'Y':
                    message = "Child " + str(i - 1) + " Information: "
                    message_suffix = "\nLeave Blank to use '" + name_list[0] + "'"
                else:
                    message = "Child " + str(i) + " Information: "
                    message_suffix = "\nLeave Blank to use '" + name_list[0] + "'"
                last_name_menu.set_message(message + "Last Name" + message_suffix, "Information")
                first_name_menu.set_message(message + "First Name", "Information")
                last = last_name_menu.show("Last Name: ", indent=2, show_available_seats=True,
                                           default_value=None if message_suffix == "" else name_list[0])
                if last == "X":
                    booking_menu.set_message("Family Booking Aborted", "Error")
                    return
                first = first_name_menu.show("First Name: ", indent=2, show_available_seats=True, sticky_message=True)
                if first == "X":
                    booking_menu.set_message("Family Booking Aborted", "Error")
                    return
                name_list.append(last)
                name_list.append(first)
        parent = ParentPassenger(name_list.pop(0), name_list.pop(1))
        get_my_passenger_list().append(parent)
        if spouse == 'Y':
            sp = ParentPassenger(name_list.pop(0), name_list.pop(0), spouse=parent)
            parent.spouse = sp
            get_my_passenger_list().append(sp)
        else:
            sp = None
        while len(name_list) > 0:
            child = ChildPassenger(name_list.pop(0), name_list.pop(0), parent)
            parent.children.append(child)
            get_my_passenger_list().append(child)
            if sp is not None:
                sp.children.append(child)
        booking_menu.set_message("Family Tickets Booked", "Confirmation")

    while True:
        reg = wanna_get_away_seats_available()
        bus = business_select_seats_available()
        booking_menu.menu_item(1).set_disabled(bus == 0)
        booking_menu.menu_item(2).set_disabled(reg < 1)
        booking_menu.menu_item(3).set_disabled(reg < 2)
        booking_menu.menu_item(4).set_disabled(reg < 1)

        choice = booking_menu.show(">>>Ticket Type: ", show_available_seats=True)
        if choice == 1:
            show_business_select_menu()
        elif choice == 2:
            show_disabled_menu()
        elif choice == 3:
            show_family_menu()
        elif choice == 4:
            show_gga_menu()
        elif choice == booking_menu.invalid_return_value:
            booking_menu.set_message("Invalid Selection", "Error")
        elif choice == booking_menu.exit_value:
            break
