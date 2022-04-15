import names
import random

___boarding_ids__ = list()
___reserved_ids__ = list()
___random_passenger_count__ = random.randint(36, 135)
___conf_dicts__ = dict()


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

    def ___boarding_id_number__(self):
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
                for child in self.___parent__.children:
                    if child.boarding_id[0:1] != 'A':
                        has_separated_family_member = True
                        break
                if self.___parent__.spouse is not None and self.___parent__.spouse.boarding_id[0:1] != 'A':
                    has_separated_family_member = True

                value += 4000 if has_separated_family_member else 2000
        elif self.boarding_id[0:1] == 'A':
            value += 2000
        elif self.boarding_id[0:1] == 'B':
            value += 5000
        elif self.boarding_id[0:1] == 'C':
            value += 6000
        return value

    def ___group_boarding_id_number__(self):
        value = self.___boarding_id_number__()
        if isinstance(self, DisabledPassenger):
            if self.attendant is None or (self.attendant.___boarding_id_number__() < self.___boarding_id_number__()):
                return value
            else:
                return self.attendant.___boarding_id_number__()
        elif isinstance(self, AttendantPassenger):
            if self.elder.___boarding_id_number__() < value:
                return value
            else:
                return self.elder.___boarding_id_number()
        elif isinstance(self, ParentPassenger):
            if self.spouse is not None and self.spouse.___boarding_id_number__() > value:
                value = self.spouse.___boarding_id_number__()
            for child in self.children:
                if child.___boarding_id_number__() > value:
                    value = child.___boarding_id_number__()
            return value
        elif isinstance(self, ChildPassenger):
            if self.___parent__.___boarding_id_number__() > value:
                value = self.___parent__.___boarding_id_number__()
            if self.___parent__.spouse is not None and self.___parent__.spouse.___boarding_id_number__() > value:
                value = self.___parent__.spouse.___boarding_id_number__()
            for child in self.___parent__.children:
                if child.___boarding_id_number__() > value:
                    value = child.___boarding_id_number__()
            return value
        else:
            return value

    def upgrade(self):
        if isinstance(self, ParentPassenger) or isinstance(self, ChildPassenger):
            return False
        elif self.___group_boarding_id_number__() < 2116:
            # already upgraded or disabled/attendant with assistive device
            return False
        elif len(___reserved_ids__) == 0:
            return False
        else:
            self.boarding_id = ___reserved_ids__.pop(0)
            return True

    def __eq__(self, other):
        return self.___group_boarding_id_number__() == other.___group_boarding_id_number__()

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        myValue = self.___group_boarding_id_number__()
        otherValue = other.___group_boarding_id_number__()
        return myValue > otherValue

    def __ge__(self, other):
        myValue = self.___group_boarding_id_number__()
        otherValue = other.___group_boarding_id_number__()
        return myValue >= otherValue

    def __lt__(self, other):
        myValue = self.___group_boarding_id_number__()
        otherValue = other.___group_boarding_id_number__()
        return myValue < otherValue

    def __le__(self, other):
        myValue = self.___group_boarding_id_number__()
        otherValue = other.___group_boarding_id_number__()
        return myValue <= otherValue


class ChildPassenger(Passenger):
    def __init__(self, last_name=None):
        super(ChildPassenger, self).__init__(last_name)


class ParentPassenger(Passenger):
    def __init__(self, last_name=None):
        super(ParentPassenger, self).__init__(last_name)


class DisabledPassenger(Passenger):
    def __init__(self, last_name=None):
        super(DisabledPassenger, self).__init__(last_name)
        # 50% chance disabled person will have an assistive device
        self.has_assistive_device = random.randint(0, 1) == 1
        self.extra_time = False


class AttendantPassenger(Passenger):
    def __init__(self, last_name=None):
        super(AttendantPassenger, self).__init__(last_name)


def generate_passenger_list():
    # random number of passengers that ensures at least 1 passenger will have the Boarding ID B1
    def apply_boarding_id(passenger, next_available=True):
        if next_available:
            passenger.boarding_id = ___boarding_ids__.pop(0)
        else:
            passenger.boarding_id = ___boarding_ids__.pop(random.randint(0, len(___boarding_ids__)-1))

    ___reserved_ids__.clear()
    ___boarding_ids__.clear()
    ___random_passenger_count__ = random.randint(36, 135)

    count = 0
    for letter in ('A', 'B', 'C'):
        for number in range(1, 51):
            # The first 15 slots A1 - A15 are reserved for "Business Select" checkins
            if letter == 'A' and number < 16:
                ___reserved_ids__.append(letter + str(number))
            else:
                ___boarding_ids__.append(letter + str(number))
                count += 1
                if count == ___random_passenger_count__:
                    break
        if count == ___random_passenger_count__:
            break

    passengers = list()
    while len(___boarding_ids__) > 0:
        # determine type of passenger. 5% chance to be Business Select (if available),
        # 5% chance to be a child, 5% to be elderly
        passenger_type = random.randrange(1 if len(___reserved_ids__) > 0 else 6, 101)
        if passenger_type in range(1, 5) and len(___reserved_ids__) > 0:
            passenger = Passenger()
            passenger.boarding_id = ___reserved_ids__.pop(0)
            passengers.append(passenger)
        else:
            if passenger_type in range(6, 11) and len(___boarding_ids__) > 1:
                # child passenger(s) if enough capacity for at least 1 child and 1 adult
                parent = ParentPassenger()
                apply_boarding_id(parent, True)
                passengers.append(parent)
                if random.randint(1, 100) >= 65 and len(___boarding_ids__) > 1:
                    # 35% chance both parents/guardians are on the trip. Some families only have 1 parent,
                    # or a grandparent or single individual may be accompanying minor
                    parent.spouse = ParentPassenger(parent.last_name)
                    parent.spouse.spouse = parent
                    apply_boarding_id(parent.spouse, False)
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

                while len(___boarding_ids__) > 0 and child_count > 0:
                    child = ChildPassenger(parent.last_name)
                    child.___parent__ = parent
                    children.append(child)
                    child_count -= 1
                    apply_boarding_id(child, False)
                    passengers.append(child)

                parent.children = children
                if parent.spouse is not None:
                    parent.spouse.children = children
                passenger = parent

            elif passenger_type in range(11, 15):
                #  disabled passenger(s)
                passenger = DisabledPassenger()
                apply_boarding_id(passenger)
                passengers.append(passenger)
                if random.randint(0, 1) == 1 and len(___boarding_ids__) > 1:
                    passenger.attendant = AttendantPassenger(passenger.last_name)
                    passenger.attendant.elder = passenger
                    apply_boarding_id(passenger.attendant, False)
                    passengers.append(passenger.attendant)
                else:
                    passenger.attendant = None
            else:
                passenger = Passenger()
                apply_boarding_id(passenger)
                passengers.append(passenger)
    return passengers
