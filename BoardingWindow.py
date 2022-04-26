from PassengerPriorityQueue import *
from Flight import *
from UI import *

boarding_menu = Menu("Boarding Window", {1: "Queue Current Boarding Group",
                                         2: "Board Current Boarding Group",
                                         3: "Show Queue By Order Of Entry",
                                         4: "Show Prioritized Queue",
                                         'X': "Return to Main Menu"}, exit_value='X', not_available_return_value=-1)


def show_menu():
    queue = PassengerPriorityQueue()
    group_ids = get_boarding_groups()
    passengers = list()
    while True:
        if len(group_ids) > 0:
            boarding_menu.set_message("Current Boarding Group:\n" + group_ids[0], "Information")
        boarding_menu.menu_item(1).set_disabled(len(group_ids) == 0 or len(queue) > 0)
        boarding_menu.menu_item(2).set_disabled(len(queue) == 0)
        boarding_menu.menu_item(3).set_disabled(len(queue) == 0)
        boarding_menu.menu_item(4).set_disabled(len(queue) == 0)
        boarding_menu.menu_item('X').set_disabled(len(group_ids) > 0 or len(queue) > 0)
        if not boarding_menu.menu_item(1).disabled():
            default_value = 1
        elif not boarding_menu.menu_item(2).disabled():
            default_value = 2
        elif not boarding_menu.menu_item('X').disabled():
            default_value = 'X'
        else:
            default_value = None
        choice = boarding_menu.show(">>>Choice: ", indent=1, show_available_seats=True, sticky_message=True, default_value=default_value)
        if choice == 1:
            passengers = get_passengers_in_boarding_group(group_ids[0])
            for p in passengers:
                queue.enqueue(p)
        elif choice == 2:
            display_passenger_list(queue.__queue__, "NOW BOARDING " + group_ids[0].upper(), delay_between_entries=.25, sort=False, index_list=passengers)
            queue.clear()
            group_ids.pop(0)
            if len(group_ids) == 0:
                boarding_menu.set_message("Boarding Complete", "Confirmation")
                Flight.__boarded__.append(True)
            passengers.clear()
        elif choice == 3:
            display_passenger_list(passengers, "ORDER OF QUEUE ENTRY", False)
        elif choice == 4:
            display_passenger_list(queue.__queue__, "PRIORITIZED QUEUE", False, index_list=passengers)
        elif choice == 'X':
            get_my_passenger_list().clear()
            get_passenger_list().clear()
            return
