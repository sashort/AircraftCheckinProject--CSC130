import names
import random
import time

import Flight
from UI import *
__MAX_BUSINESS_SELECT_SEATS__ = 15
__MAX_WANNA_GET_AWAY_SEATS__ = 135
__MAX_SEATS__ = 150

__available_confirmation_ids__ = list()
__available_wanna_get_away_boarding_ids__ = list()
__available_business_select_ids__ = list()
__passenger_list__ = list()
__my_passenger_list__ = list()
__check_in__ = list()
__passenger_dictionary__ = dict()
__boarding_queue__ = list()

def check_in_begun():
    return len(__check_in__) == 1


def get_passenger_list():
    return __passenger_list__


def get_my_passenger_list():
    return __my_passenger_list__


def get_passenger_dict():
    return __passenger_dictionary__


def get_boarding_groups():
    preboard = False
    a = False
    extra_time = False
    family_boarding = False
    b = False
    c = False
    for passenger in get_my_passenger_list():
        if passenger.boarding_group() == "Preboard":
            preboard = True
        elif passenger.boarding_group == "A":
            a = True
        elif passenger.boarding_group == "Extra Time":
            extra_time = True
        elif passenger.boarding_group == "Family Boarding":
            family_boarding = True
        elif passenger.boarding_group == "B":
            b = True
        elif passenger.boarding_group == "C":
            c = True

    values = list()
    if preboard:
        values.append("Preboard")
    if a:
        values.append("A")
    if extra_time:
        values.append('Extra Time')
    if family_boarding:
        values.append("Family Boarding")
    if b:
        values.append("B")
    if c:
        values.append("C")
    return values


def get_passengers_in_boarding_group(boarding_group):
    passengers = list()
    for passenger in __passenger_list__:
        if passenger.boarding_group() == boarding_group:
            passengers.append(passenger)

    # Generate Unsorted/Random list of passengers in boarding group
    random_ordered_passengers = list()
    while len(passengers) > 0:
        random_ordered_passengers.append(passengers.pop(random.randint(0, len(passengers) - 1)))
    return random_ordered_passengers


def business_select_seats_available():
    available = __MAX_BUSINESS_SELECT_SEATS__
    for passenger in __passenger_list__:
        if passenger.is_business_select:
            available -= 1
    return available


def wanna_get_away_seats_available():
    available = __MAX_WANNA_GET_AWAY_SEATS__
    for passenger in __passenger_list__:
        if not passenger.is_business_select:
            available -= 1
    return available


def queue_and_board():
    for bg in Flight.get_boarding_groups():
        should_board_group = input("Press Any Key To Begin Boarding current group: {}".format(bg))
        if should_board_group is not None:
            return
        passengers_in_group = Flight.get_passengers_in_boarding_group(bg)
        for passenger in passengers_in_group:
            __boarding_queue__.append(passenger)

def reset_flight():
    __available_confirmation_ids__.clear()
    __available_business_select_ids__.clear()
    __available_wanna_get_away_boarding_ids__.clear()
    __passenger_list__.clear()
    __my_passenger_list__.clear()
    __passenger_dictionary__.clear()
    __random_passenger_count__ = random.randint(36, __MAX_WANNA_GET_AWAY_SEATS__)
    __check_in__.clear()

    # generate unique confirmation numbers
    while len(__available_confirmation_ids__) < __MAX_SEATS__:
        new_confirmation_id = ""
        for i in range(6):
            if random.randint(0, 1) == 0:
                # No 0 or 1, they can be confused with O and I
                new_confirmation_id += chr(ord('2') + random.randint(0, 7))
            else:
                new_confirmation_id += chr(ord('A') + random.randint(0, 25))
        if new_confirmation_id not in __available_confirmation_ids__:
            __available_confirmation_ids__.append(new_confirmation_id)

    # generate boarding ids
    for letter in ('A', 'B', 'C'):
        for number in range(1, 51):
            # The first 15 slots A1 - A15 are reserved for "Business Select" check_ins
            if letter == 'A' and number < 16:
                __available_business_select_ids__.append(letter + str(number))
            else:
                __available_wanna_get_away_boarding_ids__.append(letter + str(number))

    # populate flight with random passengers, with enough room to fill at least up to C1
    normal_passenger_count = 0
    business_passenger_count = 0
    while normal_passenger_count < __random_passenger_count__:
        # determine type of passenger. 5% chance to be Business Select (if available),
        # 5% chance to be a child, 5% to be elderly
        passenger_type = random.randint(1 if business_passenger_count < __MAX_BUSINESS_SELECT_SEATS__ else 6, 100)
        if passenger_type in range(1, 6):
            passenger = Passenger(is_business_select=True)
            passenger.check_in()
            business_passenger_count += 1
            __passenger_dictionary__[passenger.confirmation_id] = passenger
        else:
            if passenger_type in range(6, 11) and normal_passenger_count <= __random_passenger_count__ - 2:
                # child passenger(s) if enough capacity for at least 1 child and 1 adult
                parent = ParentPassenger()
                __passenger_dictionary__[parent.confirmation_id] = parent
                normal_passenger_count += 1
                if random.randint(1, 100) >= 65 and len(__available_wanna_get_away_boarding_ids__) > 2:
                    # 35% chance both parents/guardians are on the trip. Some families only have 1 parent,
                    # or a grandparent or single individual may be accompanying minor
                    parent.spouse = ParentPassenger(parent.last_name, spouse=parent)
                    __passenger_dictionary__[parent.spouse.confirmation_id] = parent.spouse
                    normal_passenger_count += 1

                child_count_probability = random.randint(1, 100)
                if child_count_probability in range(1, 41):
                    # 40% chance of having 1 child
                    # 40% chance of having 1 child
                    child_count = 1
                elif child_count_probability in range(41, 81):
                    # 40% chance of having 2 children
                    child_count = 2
                elif child_count_probability in range(81, 96):
                    # 15% chance of having 3 children
                    child_count = 3
                else:
                    # 5% chance of having a larger family
                    # with 4/5 young children
                    child_count = random.randint(4, 6)

                while normal_passenger_count < __random_passenger_count__ and len(parent.children) < child_count:
                    child = ChildPassenger(parent.last_name, parent=parent)
                    parent.children.append(child)
                    __passenger_dictionary__[child.confirmation_id] = child
                    normal_passenger_count += 1

                if parent.spouse is not None:
                    parent.spouse.children = parent.children

            elif passenger_type in range(11, 15):
                #  disabled passenger(s)
                passenger = DisabledPassenger()
                __passenger_dictionary__[passenger.confirmation_id] = passenger
                normal_passenger_count += 1
                if normal_passenger_count < __random_passenger_count__ and random.randint(0, 1) == 1:
                    passenger.attendant = AttendantPassenger(
                        passenger.last_name if random.randint(1, 100) <= 75 else None, elder=passenger)
                    normal_passenger_count += 1
                    __passenger_dictionary__[passenger.attendant.confirmation_id] = passenger.attendant
            else:
                passenger = Passenger()
                __passenger_dictionary__[passenger.confirmation_id] = passenger
                normal_passenger_count += 1


def book_seats():
    abort_message = ""
    original_size = len(__my_passenger_list__)
    new_passengers = list()
    passenger = None
    outlined = Style(outlined=True)
    blue = Style(background_color=(0, 0, 255))
    print(styled(blue, " SEATS AVAILABLE "), styled(outlined, ' ' + str(business_select_seats_available()) + ' '), "Business Select |", styled(outlined, ' ' + str(wanna_get_away_seats_available()) + ' '),
          "Wanna Get Away")
    print("NOTE: Business Select not available for disabled individuals or families.")
    last_name = input("╭     Last Name?  ")
    first_name = input("│    First Name? ")
    if wanna_get_away_seats_available() > 0 and input("│Disabled [Y/N]? ") in "Yy":
        passenger = DisabledPassenger(last_name, first_name,
                                      has_assistive_device=input(
                                          "│\t▶       Do you have an Assistive Device [Y/N]? ") in "Yy")
        new_passengers.append(passenger)
        if input("│\t▶ Will an Attendant be accompanying you [Y/N]? ") in "Yy":
            if wanna_get_away_seats_available() > 1:
                print("│\t\t  Leave last name blank to use '" + passenger.last_name + "'")
                last_name = input("│\t\t╭ Attendant Last Name: ")
                if last_name == "":
                    last_name = passenger.last_name
                first_name = input("│\t\t╰ Attendant First Name: ")
                passenger.attendant = AttendantPassenger(last_name, first_name, passenger)
                new_passengers.append(passenger.attendant)
            else:
                print("\t" + styled("Caution Message", "Sorry, not enough seats available for attendant."))
                if input("\t\tWould you still like to fly alone [Y/N]? ") in "Yy":
                    new_passengers.append(passenger)
                else:
                    abort_message = "Sorry, not enough seats available for attendant."
    elif wanna_get_away_seats_available() > 1 and \
            input("\tFlying with children 6- [Y/N]? ") in "Yy":
        passenger = ParentPassenger(last_name, first_name)
        new_passengers.append(passenger)
        parent_count = 1
        child_count = int(input("\t\tHow may children 6- are flying with you? "))
        if child_count > wanna_get_away_seats_available():
            abort_message = "Sorry, not enough seats available for " + str(child_count) + " children."
        elif input("\t\tWill a spouse be accompanying you as well [Y/N]? ") in "Yy":
            if child_count + 1 > wanna_get_away_seats_available():
                print("\t\t" + styled("Caution Message", "Sorry, not enough seats for spouse."))
                if input("\t\tDo you wish to continue [Y/N]? ") in "Nn":
                    abort_message = "Sorry, not enough seats available for your spouse."
            else:
                print("\t\t\tLeave last name blank to use '" + passenger.last_name + "'")
                last_name = input("\t\t\tSpouse's Last Name: ")
                if last_name == "":
                    last_name = passenger.last_name
                first_name = input("\t\t\tSpouse's First Name: ")
                passenger.spouse = ParentPassenger(last_name, first_name, spouse=passenger)
                new_passengers.append(passenger.spouse)
                parent_count += 1
        if child_count + parent_count <= wanna_get_away_seats_available() and abort_message == "":
            children = list()
            print("\t\tLeave last name blank to use '" + passenger.last_name + "'")
            for i in range(1, child_count + 1):
                last_name = input("\t\tChild " + str(i) + " Last Name: ")
                if last_name == "":
                    last_name = passenger.last_name
                first_name = input("\t\tChild " + str(i) + " First Name: ")
                child = ChildPassenger(last_name, first_name, parent=passenger)
                children.append(child)
                new_passengers.append(child)
            passenger.children = children
            if passenger.spouse is not None:
                passenger.spouse.children = children
    elif business_select_seats_available() > 0 and input("\tIs this a Business Select Ticket [Y/N]? ") in "Yy":
        passenger = Passenger(last_name, first_name, is_business_select=True)
        passenger.check_in()
        new_passengers.append(passenger)
    elif wanna_get_away_seats_available() > 0:
        passenger = Passenger(last_name, first_name)
        new_passengers.append(passenger)
    else:
        abort_message = "Sorry, no seats available."
        return False
    if abort_message != "":
        print('\t' + styled("Error Message", "⚠ " + abort_message))
        time.sleep(3)
    elif input("CONFIRM BOOKING [Y/N]? ") not in "Yy":
        abort_message = "Booking Aborted By User"
        print('\t' + styled("Error Message", "⚠ " + abort_message))
        time.sleep(3)
    if abort_message != "":
        __passenger_list__.remove(passenger)
        new_passengers.remove(passenger)
        if isinstance(passenger, ParentPassenger):
            for passenger in passenger.children:
                __passenger_list__.remove(passenger)
                new_passengers.remove(passenger)
            if passenger.spouse is not None:
                __passenger_list__.remove(passenger.spouse)
                new_passengers.remove(passenger)
        elif isinstance(passenger, DisabledPassenger) and passenger.attendant is not None:
            __passenger_list__.remove(passenger.attendant)
            new_passengers.remove(passenger.attendant)
        return False
    for p in new_passengers:
        __passenger_dictionary__[p.confirmation_id] = p
        __my_passenger_list__.append(p)
        if check_in_begun():
            p.check_in()

    if check_in_begun() and not passenger.is_business_select and \
            not isinstance(passenger, ParentPassenger) and \
            not isinstance(passenger, ChildPassenger) and \
            not isinstance(passenger, DisabledPassenger) and \
            not isinstance(passenger, AttendantPassenger):
        print("Check-in has already started.")
        print("You were assigned the next available boarding group/number(s)")
        print("for your Wanna Get Away tickets. You may upgrade at the gate kiosk.")
    new_passengers.clear()
    return len(__my_passenger_list__) > original_size


def open_check_in_window():
    if not check_in_begun():
        __check_in__.append(True)
        randomized_board_list = list()
        for passenger in __passenger_list__:
            if passenger.is_business_select and passenger.boarding_id == "":
                passenger.check_in()
            elif not passenger.is_business_select and passenger.boarding_id == "":
                randomized_board_list.append(passenger)
        while len(randomized_board_list) > 0:
            randomized_board_list[0].boarding_id = __available_wanna_get_away_boarding_ids__.pop(
                random.randint(0, len(randomized_board_list) - 1))
            randomized_board_list.pop(0)
        return True
    return False


class Passenger:
    def __init__(self, last_name=None, first_name=None, *, is_business_select=False):
        self.boarding_id = ""
        if first_name is None:
            self.first_name = names.get_first_name(('male' if random.randint(0, 1) == 0 else 'female'))
        else:
            self.first_name = first_name
        if last_name is None:
            self.last_name = names.get_last_name()
        else:
            self.last_name = last_name
        self.confirmation_id = ""
        # similar to Southwest Airlines confirmation number, allows for 1,544,804,416 confirmation numbers
        # which can be recycled.
        self.confirmation_id = ""

        self.confirmation_id = __available_confirmation_ids__.pop(0)
        self.is_business_select = is_business_select
        __passenger_list__.append(self)

    def check_in(self, next_available=True):
        # returns True if already checked in or boarding already started
        if (self.boarding_id is None or self.boarding_id == "") and (check_in_begun() or self.is_business_select):
            if self.is_business_select:
                self.boarding_id = __available_business_select_ids__.pop(0)
                return True
            elif next_available or len(__available_wanna_get_away_boarding_ids__) == 1:
                self.boarding_id = __available_wanna_get_away_boarding_ids__.pop(0)
                return True
            else:
                self.boarding_id = __available_wanna_get_away_boarding_ids__.pop(
                    random.randint(0, len(__available_wanna_get_away_boarding_ids__) - 1))
                return True
            return True
        return False

    def boarding_id_number(self):
        if self.boarding_id == "":
            if isinstance(self, DisabledPassenger) and (self.has_assistive_device or self.attendant is not None):
                return 1000
            elif isinstance(self, DisabledPassenger) and self.extra_time:
                return 3000
            elif isinstance(self, AttendantPassenger):
                return 1000
            else:
                return 7000
        value = int(self.boarding_id[1:])
        if self.boarding_id[0:1] == 'A':
            value += 100
        elif self.boarding_id[0:1] == 'B':
            value += 200
        elif self.boarding_id[0:1] == 'C':
            value += 300

        if (isinstance(self, DisabledPassenger) and (self.has_assistive_device or self.attendant is not None)) or \
                isinstance(self, AttendantPassenger):
            value += 1000
        elif isinstance(self, DisabledPassenger) and self.extra_time:
            value += 3000
        elif isinstance(self, ParentPassenger):
            if self.boarding_id[0:1] != 'A':
                value += 4000
            else:
                has_separated_family_member = False
                for child in self.children:
                    if child.boarding_id[0:1] != 'A':
                        has_separated_family_member = True
                        break
                if self.spouse is not None and self.spouse.boarding_id[0:1] != 'A':
                    has_separated_family_member = True
                value += 4000 if has_separated_family_member else 2000
        elif isinstance(self, ChildPassenger):
            if self.boarding_id[0:1] != 'A':
                value += 4000
            else:
                has_separated_family_member = False
                for child in self.__parent__.children:
                    if child.boarding_id[0:1] != 'A':
                        has_separated_family_member = True
                        break
                if self.__parent__.spouse is not None and self.__parent__.spouse.boarding_id[0:1] != 'A':
                    has_separated_family_member = True

                value += 4000 if has_separated_family_member else 2000
        elif self.boarding_id[0:1] == 'A':
            value += 2000
        elif self.boarding_id[0:1] == 'B':
            value += 5000
        elif self.boarding_id[0:1] == 'C':
            value += 6000
        return value

    def group_boarding_id_number(self):
        value = self.boarding_id_number()
        if isinstance(self, DisabledPassenger):
            if self.attendant is None:
                return value
            elif value > self.attendant.boarding_id_number():
                return value
            else:
                return self.attendant.boarding_id_number()
        elif isinstance(self, AttendantPassenger):
            # Attendant might not be in the same boarding order if elder
            # does not have an assistive implement, and hasn't been granted
            # extra time.
            if value > self.elder.boarding_id_number():
                return value
            else:
                return self.elder.boarding_id_number()
        elif isinstance(self, ParentPassenger):
            if self.spouse is not None and self.spouse.boarding_id_number() > value:
                value = self.spouse.boarding_id_number()
            for child in self.children:
                if child.boarding_id_number() > value:
                    value = child.boarding_id_number()
            return value
        elif isinstance(self, ChildPassenger):
            if self.__parent__.boarding_id_number() > value:
                value = self.__parent__.boarding_id_number()
            if self.__parent__.spouse is not None and self.__parent__.spouse.boarding_id_number() > value:
                value = self.__parent__.spouse.boarding_id_number()
            for child in self.__parent__.children:
                if child.boarding_id_number() > value:
                    value = child.boarding_id_number()
            return value
        else:
            return value

    def boarding_group(self):
        if isinstance(self, DisabledPassenger) and (self.has_assistive_device or self.attendant is not None):
            return "Preboard"
        elif isinstance(self, AttendantPassenger):
            return "Preboard"
        elif self.is_business_select or self.group_boarding_id_number() < 3000:
            return "A"
        elif self.group_boarding_id_number() < 4000:
            return "Extra Time"
        elif self.group_boarding_id_number() < 5000:
            return "Family Boarding"
        elif self.group_boarding_id_number() < 6000:
            return "B"
        elif self.group_boarding_id_number() < 7000:
            return "C"

        return "To Be Determined"

    def upgrade(self):
        if isinstance(self, ParentPassenger) or isinstance(self, ChildPassenger):
            return False
        elif isinstance(self, DisabledPassenger) or isinstance(self, AttendantPassenger):
            return False
        elif self.is_business_select or business_select_seats_available() == 0:
            return False
        else:
            __available_wanna_get_away_boarding_ids__.insert(0, self.boarding_id)
            self.boarding_id = __available_business_select_ids__.pop(0)
            self.is_business_select = True
            return True

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        my_value = self.group_boarding_id_number()
        other_value = other.group_boarding_id_number()
        if my_value != other_value:
            return my_value > other_value
        else:
            return self.boarding_id_number() > other.boarding_id_number()

    def __ge__(self, other):
        my_value = self.group_boarding_id_number()
        other_value = other.group_boarding_id_number()
        if my_value != other_value:
            return my_value >= other_value
        else:
            return self.boarding_id_number() >= other.boarding_id_number()

    def __lt__(self, other):
        my_value = self.group_boarding_id_number()
        other_value = other.group_boarding_id_number()
        if my_value != other_value:
            return my_value < other_value
        else:
            return self.boarding_id_number() < other.boarding_id_number()

    def __le__(self, other):
        my_value = self.group_boarding_id_number()
        other_value = other.group_boarding_id_number()
        if my_value != other_value:
            return my_value <= other_value
        else:
            return self.boarding_id_number() <= other.boarding_id_number()


class ChildPassenger(Passenger):
    def __init__(self, last_name=None, first_name=None, parent=None):
        super(ChildPassenger, self).__init__(last_name, first_name)
        self.__parent__ = parent


class ParentPassenger(Passenger):
    def __init__(self, last_name=None, first_name=None, children=None, spouse=None):
        super(ParentPassenger, self).__init__(last_name, first_name)
        if children is None:
            self.children = list()
        else:
            self.children = children
        self.spouse = spouse


class DisabledPassenger(Passenger):
    def __init__(self, last_name=None, first_name=None, has_assistive_device=None, attendant=None):
        super(DisabledPassenger, self).__init__(last_name, first_name)
        if has_assistive_device is None:
            # 50% chance disabled person will have an assistive device
            self.has_assistive_device = random.randint(0, 1) == 1
        else:
            self.has_assistive_device = has_assistive_device

        self.attendant = attendant
        self.extra_time = False

    def request_extra_time(self):
        if self.extra_time:
            return False
        elif self.has_assistive_device or self.attendant is not None:
            return False
        else:
            self.extra_time = True
            return True


class AttendantPassenger(Passenger):
    def __init__(self, last_name=None, first_name=None, elder=None):
        super(AttendantPassenger, self).__init__(last_name, first_name)
        self.elder = elder


reset_flight()
