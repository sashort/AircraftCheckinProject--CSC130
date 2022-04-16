import names
import random

__boarding_ids__ = list()
__unused_boarding_ids__ = list()
__reserved_ids__ = list()
__random_passenger_count__ = random.randint(36, 135)
__passenger_list__ = list()
__manual_entry_passenger_list__ = list()
__manual_entry_unassigned__ = list()
__conf_dicts__ = dict()


def checkin_begun():
    return len(__checkin__) == 1

__checkin__ = list()


def reset_passenger_list():
    __reserved_ids__.clear()
    __boarding_ids__.clear()
    __passenger_list__.clear()
    __unused_boarding_ids__.clear()
    __manual_entry_passenger_list__.clear()
    __manual_entry_unassigned__.clear
    __random_passenger_count__ = 131  # random.randint(36, 135)
    __checkin__.clear()

    count = 0
    for letter in ('A', 'B', 'C'):
        for number in range(1, 51):
            # The first 15 slots A1 - A15 are reserved for "Business Select" checkins
            if letter == 'A' and number < 16:
                __reserved_ids__.append(letter + str(number))
            else:
                if count > __random_passenger_count__:
                    __unused_boarding_ids__.append(letter + str(number))
                else:
                    __boarding_ids__.append(letter + str(number))
                count += 1


def get_passenger_list():
    return __passenger_list__


def get_my_passenger_list():
    return __manual_entry_passenger_list__


def business_select_seats_available():
    return len(__reserved_ids__)


def gotta_get_away_seats_available():
    return len(__unused_boarding_ids__)


class Passenger:
    def __init__(self, last_name=None):
        self.boarding_id = ""
        self.first_name = names.get_first_name(('male' if random.randrange(2) == 0 else 'female'))
        if last_name is None:
            self.last_name = names.get_last_name()
        else:
            self.last_name = last_name
        self.confirmation_id = ""
        # similar to Southwest Airlines confirmation number, allows for 1,544,804,416 confirmation numbers
        # which can be recycled.
        self.confirmation_id = ""

        # TODO MAKE SURE CONFIRMATION NUMBER IS UNIQUE, WILL CAUSE PROBLEMS WITH DICTIONARY IF NOT
        for i in range(6):
            if random.randrange(2) == 0:
                # No 0 or 1, they can be confused with O and I
                self.confirmation_id += chr(ord('2') + random.randrange(8))
            else:
                self.confirmation_id += chr(ord('A') + random.randrange(26))

    def __boarding_id_number__(self):
        if not isinstance(self.boarding_id, str):
            print("Somehow this isn't a string")
        if self.boarding_id == "":
            return 7000
        value = int(self.boarding_id[1:])
        if self.boarding_id[0:1] == 'A':
            value += 100
        elif self.boarding_id[0:1] == 'B':
            value += 200
        elif self.boarding_id[0:1] == 'C':
            value += 300

        if (isinstance(self, DisabledPassenger) and self.has_assistive_device) or (
                isinstance(self, AttendantPassenger) and self.elder.has_assistive_device):
            value += 1000
        elif (isinstance(self, DisabledPassenger) and self.extra_time) or (
                isinstance(self, AttendantPassenger) and self.elder.extra_time):
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

    def __group_boarding_id_number__(self):
        value = self.__boarding_id_number__()
        if isinstance(self, DisabledPassenger):
            if self.attendant is None or (self.attendant.__boarding_id_number__() < self.__boarding_id_number__()):
                return value
            else:
                return self.attendant.__boarding_id_number__()
        elif isinstance(self, AttendantPassenger):
            if self.elder.__boarding_id_number__() < value:
                return value
            else:
                return self.elder.__boarding_id_number__()
        elif isinstance(self, ParentPassenger):
            if self.spouse is not None and self.spouse.__boarding_id_number__() > value:
                value = self.spouse.__boarding_id_number__()
            for child in self.children:
                if child.__boarding_id_number__() > value:
                    value = child.__boarding_id_number__()
            return value
        elif isinstance(self, ChildPassenger):
            if self.__parent__.__boarding_id_number__() > value:
                value = self.__parent__.__boarding_id_number__()
            if self.__parent__.spouse is not None and self.__parent__.spouse.__boarding_id_number__() > value:
                value = self.__parent__.spouse.__boarding_id_number__()
            for child in self.__parent__.children:
                if child.__boarding_id_number__() > value:
                    value = child.__boarding_id_number__()
            return value
        else:
            return value

    def upgrade(self):
        if isinstance(self, ParentPassenger) or isinstance(self, ChildPassenger):
            return False
        elif self.__group_boarding_id_number__() < 2116:
            # already upgraded or disabled/attendant with assistive device
            return False
        elif len(__reserved_ids__) == 0:
            return False
        else:
            self.boarding_id = __reserved_ids__.pop(0)
            return True

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        myValue = self.__group_boarding_id_number__()
        otherValue = other.__group_boarding_id_number__()
        if myValue != otherValue:
            return myValue > otherValue
        else:
            return self.__boarding_id_number__() > other.__boarding_id_number__()

    def __ge__(self, other):
        myValue = self.__group_boarding_id_number__()
        otherValue = other.__group_boarding_id_number__()
        if myValue != otherValue:
            return myValue >= otherValue
        else:
            return self.__boarding_id_number__() >= other.__boarding_id_number__()

    def __lt__(self, other):
        myValue = self.__group_boarding_id_number__()
        otherValue = other.__group_boarding_id_number__()
        if myValue != otherValue:
            return myValue < otherValue
        else:
            return self.__boarding_id_number__() < other.__boarding_id_number__()

    def __le__(self, other):
        myValue = self.__group_boarding_id_number__()
        otherValue = other.__group_boarding_id_number__()
        if myValue != otherValue:
            return myValue <= otherValue
        else:
            return self.__boarding_id_number__() <= other.__boarding_id_number__()


class ChildPassenger(Passenger):
    def __init__(self, last_name=None):
        super(ChildPassenger, self).__init__(last_name)
        self.__parent__ = None


class ParentPassenger(Passenger):
    def __init__(self, last_name=None):
        super(ParentPassenger, self).__init__(last_name)
        self.spouse = None
        self.children = list()


class DisabledPassenger(Passenger):
    def __init__(self, last_name=None):
        super(DisabledPassenger, self).__init__(last_name)
        # 50% chance disabled person will have an assistive device
        self.has_assistive_device = random.randint(0, 1) == 1
        self.extra_time = False
        self.attendant = None


class AttendantPassenger(Passenger):
    def __init__(self, last_name=None):
        super(AttendantPassenger, self).__init__(last_name)
        self.elder = None


def book_seats():
    my_list = list()
    print("SEATS AVAILABLE:", business_select_seats_available(), "Business Select |", gotta_get_away_seats_available(), "Gotta Get Away")
    print("NOTE: Business Select not available for disabled individuals or families.")
    last_name = input("\tWhat is your Last Name? ")
    first_name = input("\tWhat is your First Name? ")
    if input("\tAre you disabled [Y/N]? ") in "Yy":
        if gotta_get_away_seats_available() > 0:
            passenger = DisabledPassenger(last_name)
            passenger.first_name = first_name
            passenger.has_assistive_device = input("\tDo you have an Assistive Device [Y/N]? ") in "Yy"
            if input("\tWill an Attendant be accompanying you [Y/N]? ") in "Yy":
                if gotta_get_away_seats_available() > 1:
                    last_name = input("\t\tAttendant Last Name: ")
                    first_name = input("\t\tAttendant First Name: ")
                    attendant = AttendantPassenger(last_name)
                    attendant.first_name = first_name
                    passenger.attendant = attendant
                    attendant.elder = passenger
                    my_list.append(passenger)
                    my_list.append(attendant)
                else:
                    print("\tSorry, not enough seats available.")
                    if input("\t\tWould you still like to fly alone [Y/N]? ") in "Yy":
                        my_list.append(passenger)
        else:
            print("\tSorry, no seats available.")
    elif input("\tAre you traveling with children younger than 7 years of age [Y/N]? ") in "Yy":
        if gotta_get_away_seats_available() > 1:
            passenger = ParentPassenger(last_name)
            passenger.first_name = first_name
            parent_count = 1
            child_count = int(input("\t\tHow may children 6- are flying with you? "))
            abort = False
            if input("\t\tWill a spouse be accompanying you as well [Y/N]? ") in "Yy":
                abort = False
                if child_count + 2 > gotta_get_away_seats_available():
                    print("\t\tSorry, not enough seats for spouse.")
                    if input("\t\tDo you wish to continue [Y/N]? ") in "Yy":
                        my_list.append(passenger)
                    else:
                        abort = True
                else:
                    last_name = input("\t\t\tSpouse's Last Name: ")
                    first_name = input("\t\t\tSpouse's First Name: ")
                    spouse = ParentPassenger(last_name)
                    spouse.first_name = first_name
                    passenger.spouse = spouse
                    spouse.spouse = passenger
                    my_list.append(passenger)
                    my_list.append(spouse)
                    parent_count += 1
            else:
                my_list.append(passenger)
            if child_count + parent_count <= gotta_get_away_seats_available() and not abort:
                children = list()
                for i in range(1, child_count + 1):
                    last_name = input("\t\tChild " + str(i) + " Last Name: ")
                    first_name = input("\t\tChild " + str(i) + " First Name: ")
                    child = ChildPassenger(last_name)
                    child.first_name = first_name
                    child.__parent__ = passenger
                    children.append(child)
                    my_list.append(child)
                passenger.children = children
                if passenger.spouse is not None:
                    passenger.spouse.children = children
            else:
                my_list.remove(passenger)
                print("\t\tSorry, not enough seats available.")
        else:
            print("\tSorry, no seats available.")
    else:
        passenger = Passenger(last_name)
        passenger.first_name = first_name
        if business_select_seats_available() > 0 and input("\tIs this a Business Select Ticket [Y/N]? ") in "Yy":
            passenger.boarding_id = __reserved_ids__.pop(0)
            my_list.append(passenger)
            checkin(passenger, business_select=True)
        elif gotta_get_away_seats_available() > 0:
            my_list.append(passenger)
        else:
            print("\tSorry, no seats available.")
    if len(my_list) > 0:
        for passenger in my_list:
            __manual_entry_passenger_list__.append(passenger)
            if passenger.boarding_id == "":
                __boarding_ids__.append(__unused_boarding_ids__.pop(0))
                if checkin_begun():
                    print("Checking In")
                    checkin(passenger)
                else:
                    __manual_entry_unassigned__.append(passenger)
        if checkin_begun():
            if not 2101 <= passenger.__boarding_id_number__() <= 2115:
                print("Check-in has already started.")
                print("You were assigned the next available boarding group/number(s)")
                print("for your Gotta Get Away tickets. You may upgrade at the gate kiosk")
                print("if there are Business Select tickets still available, and you aren't")
                print("disabled or flying with children.")

    return my_list


# random number of passengers that ensures at least 1 passenger will have the Boarding ID B1
def checkin(passenger, next_available=True, business_select=False):
    if passenger.boarding_id is None or passenger.boarding_id == "":
        if business_select:
            passenger.boarding_id = __reserved_ids__.pop(0)
        elif next_available:
            passenger.boarding_id = __boarding_ids__.pop(0)
        else:
            passenger.boarding_id = __boarding_ids__.pop(random.randint(0, len(__boarding_ids__)-1))
    __passenger_list__.append(passenger)


def open_checkin_window():
    __checkin__.append(True)
    passengers = list()
    if len(__manual_entry_unassigned__) > 0:
        for passenger in __manual_entry_unassigned__:
            checkin(passenger, next_available=False)
        __manual_entry_unassigned__.clear()
    while len(__boarding_ids__) > 0:
        # determine type of passenger. 5% chance to be Business Select (if available),
        # 5% chance to be a child, 5% to be elderly
        passenger_type = random.randrange(1 if len(__reserved_ids__) > 0 else 6, 101)
        if passenger_type in range(1, 5) and len(__reserved_ids__) > 0:
            passenger = Passenger()
            passenger.boarding_id = __reserved_ids__.pop(0)
            passengers.append(passenger)
        else:
            if passenger_type in range(6, 11) and len(__boarding_ids__) > 1:
                # child passenger(s) if enough capacity for at least 1 child and 1 adult
                parent = ParentPassenger()
                checkin(parent, True)
                passengers.append(parent)
                if random.randint(1, 100) >= 65 and len(__boarding_ids__) > 1:
                    # 35% chance both parents/guardians are on the trip. Some families only have 1 parent,
                    # or a grandparent or single individual may be accompanying minor
                    parent.spouse = ParentPassenger(parent.last_name)
                    parent.spouse.spouse = parent
                    checkin(parent.spouse, False)
                    passengers.append(parent.spouse)
                else:
                    parent.spouse = None

                children = list()
                child_count_probability = random.randrange(1, 101)
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

                while len(__boarding_ids__) > 0 and child_count > 0:
                    child = ChildPassenger(parent.last_name)
                    child.__parent__ = parent
                    children.append(child)
                    child_count -= 1
                    checkin(child, False)
                    passengers.append(child)

                parent.children = children
                if parent.spouse is not None:
                    parent.spouse.children = children
                passenger = parent

            elif passenger_type in range(11, 15):
                #  disabled passenger(s)
                passenger = DisabledPassenger()
                checkin(passenger)
                passengers.append(passenger)
                if random.randint(0, 1) == 1 and len(__boarding_ids__) > 1:
                    passenger.attendant = AttendantPassenger(passenger.last_name)
                    passenger.attendant.elder = passenger
                    checkin(passenger.attendant, False)
                    passengers.append(passenger.attendant)
                else:
                    passenger.attendant = None
            else:
                passenger = Passenger()
                checkin(passenger)
                passengers.append(passenger)


reset_passenger_list()
