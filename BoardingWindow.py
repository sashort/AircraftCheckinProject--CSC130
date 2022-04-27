from PassengerPriorityQueue import *
from Flight import *
from UI import *

boarding_menu = Menu("Boarding Window", {1: "Queue Current Boarding Group",
                                         2: "Board Current Boarding Group",
                                         3: "Show Queue By Order Of Entry",
                                         4: "Show Prioritized Queue",
                                         'X': "Return to Main Menu"}, exit_value='X')


def show_menu():
    queue = PassengerPriorityQueue()
    group_ids = get_boarding_groups()
    passengers = list()
    disable_default_value = list()
    while True:
        if len(group_ids) > 0:
            boarding_menu.set_message(("[Queued]" if len(queue) > 0 else 'Next') + " Boarding Group:\n" + group_ids[0], "Information")
        boarding_menu.menu_item(1).set_disabled(len(group_ids) == 0 or len(queue) > 0)
        boarding_menu.menu_item(2).set_disabled(len(queue) == 0)
        boarding_menu.menu_item(3).set_disabled(len(queue) == 0)
        boarding_menu.menu_item(4).set_disabled(len(queue) == 0)
        boarding_menu.menu_item('X').set_disabled(len(group_ids) > 0 or len(queue) > 0)
        if len(disable_default_value) > 0:
            default_value = None
            disable_default_value.pop()
        elif not boarding_menu.menu_item(1).disabled():
            default_value = 1
        elif not boarding_menu.menu_item(2).disabled():
            default_value = 2
        elif not boarding_menu.menu_item('X').disabled():
            default_value = 'X'
        else:
            default_value = None
        choice = boarding_menu.show(">>>Choice: ", indent=1, show_available_seats=False, sticky_message=True, default_value=default_value)
        if len(disable_default_value) > 0:
            disable_default_value.pop()
        if choice == 1:
            passengers = get_passengers_in_boarding_group(group_ids[0])
            for p in passengers:
                queue.enqueue(p)
        elif choice == 2:
            if group_ids[0] == "Family Boarding" or group_ids[0] == "Preboard":
                banner_string = group_ids[0] + " In Progress"
            else:
                banner_string = "Now Boarding: " + group_ids[0]
            display_passenger_list(queue.__queue__, banner_string, delay_between_entries=.25, sort=False, index_list=passengers, show_availability=False)
            queue.clear()
            group_ids.pop(0)
            if len(group_ids) == 0:
                boarding_menu.set_message("Boarding Complete", "Confirmation")
                Flight.__boarded__.append(True)
            passengers.clear()
        elif choice == 3:
            disable_default_value.append(True)
            display_passenger_list(passengers, "Order of Queue Entry for:\n" + group_ids[0], False, show_availability=False)
        elif choice == 4:
            disable_default_value.append(True)
            display_passenger_list(queue.__queue__, "Prioritized Queue for Boarding Group:\n" + group_ids[0], False, index_list=passengers, show_availability=False)
        elif choice == 'X':
            get_my_passenger_list().clear()
            get_passenger_list().clear()
            return
        elif choice == boarding_menu.not_available_return_value:
            print(styled("Caution Message", "That menu option isn't currently available!"))
            time.sleep(2)
        elif choice == boarding_menu.invalid_return_value:
            print(styled("Error Message", "Invalid Input!\nPlease select an enabled menu option!"))
            time.sleep(2)
