import random
import time
from UI import *
import Namelist

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
__boarded__ = list()
__field_widths__ = dict()
__field_widths__["Number"] = 3
__field_widths__["Confirmation Number"] = 4
__field_widths__["Boarding ID"] = 3
__field_widths__["Boarding Group"] = len("To Be Determined")
__field_widths__["Last Name"] = 4
__field_widths__["First Name"] = 5


def total_field_width():
    tot = __field_widths__["Number"] + \
          __field_widths__["Confirmation Number"] + \
          __field_widths__["Boarding ID"] + \
          __field_widths__["Boarding Group"] + \
          __field_widths__["Last Name"] + \
          __field_widths__["First Name"] + 7
    return tot


def check_in_begun():
    return len(__check_in__) == 1


def boarded():
    return len(__boarded__) > 0


def get_passenger_list():
    return __passenger_list__


def get_my_passenger_list():
    return __my_passenger_list__


def get_passenger_dict():
    return __passenger_dictionary__


def get_boarding_groups():
    bg = dict()
    bg["Preboard"] = False
    bg["A"] = False
    bg["Extra Time"] = False
    bg["Family Boarding"] = False
    bg["B"] = False
    bg["C"] = False
    for passenger in get_passenger_list():
        if passenger.boarding_group() == "Preboard":
            bg["Preboard"] = True
        elif passenger.boarding_group() == "A":
            bg["A"] = True
        elif passenger.boarding_group() == "Extra Time":
            bg["Extra Time"] = True
        elif passenger.boarding_group() == "Family Boarding":
            bg["Family Boarding"] = True
        elif passenger.boarding_group() == "B":
            bg["B"] = True
        elif passenger.boarding_group() == "C":
            bg["C"] = True
    values = list()
    for key in bg.keys():
        if bg[key]:
            values.append(key)
    return values


def get_passengers_in_boarding_group(boarding_group):
    passengers = list()
    for passenger in __passenger_list__:
        if passenger.boarding_group() == boarding_group:
            passengers.append(passenger)
    # Generate Unsorted/Random list of passengers in boarding group
    random.shuffle(passengers)
    return passengers


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


def show_available_seats(indent=0):
    indent_string = ""
    for i in range(indent):
        indent_string += '\t'
    print(indent_string + "     Business Select Seats Available:",
          styled(styles["Outlined"], ' ' + str(business_select_seats_available()).rjust(3) + ' ') + " / 15")
    print(indent_string + "      Wanna Get Away Seats Available:",
          styled(styles["Outlined"], ' ' + str(wanna_get_away_seats_available()).rjust(3) + ' ') + " /135")


def reset_flight():
    __available_confirmation_ids__.clear()
    __available_business_select_ids__.clear()
    __available_wanna_get_away_boarding_ids__.clear()
    __passenger_list__.clear()
    __my_passenger_list__.clear()
    __passenger_dictionary__.clear()
    __random_passenger_count__ = random.randint(36, __MAX_WANNA_GET_AWAY_SEATS__)
    __check_in__.clear()
    __field_widths__["Last Name"] = 4
    __field_widths__["First Name"] = 5
    __boarded__.clear()

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
            self.first_name = Namelist.get_first_name(('male' if random.randint(0, 1) == 0 else 'female'))
        else:
            self.first_name = first_name
        if last_name is None:
            self.last_name = Namelist.get_last_name()
        else:
            self.last_name = last_name
        self.confirmation_id = ""
        # similar to Southwest Airlines confirmation number, allows for 1,544,804,416 confirmation numbers
        # which can be recycled.
        self.confirmation_id = ""

        self.confirmation_id = __available_confirmation_ids__.pop(0)
        self.is_business_select = is_business_select
        __passenger_list__.append(self)
        __passenger_dictionary__[self.confirmation_id] = self
        __field_widths__["Last Name"] = max(__field_widths__["Last Name"], len(self.last_name))
        __field_widths__["First Name"] = max(__field_widths__["First Name"], len(self.first_name))
        if check_in_begun() or self.is_business_select:
            self.check_in()

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
            elif self.is_business_select:
                return 2000
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
        elif self.boarding_group() == "A" or self.boarding_group() == "To Be Determined":
            return False
        else:
            self.extra_time = True
            return True


class AttendantPassenger(Passenger):
    def __init__(self, last_name=None, first_name=None, elder=None):
        super(AttendantPassenger, self).__init__(last_name, first_name)
        self.elder = elder


reset_flight()
