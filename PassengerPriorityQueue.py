from Flight import Passenger


class PassengerPriorityQueue:
    def __init__(self):
        self.__queue__ = list()

    def clear(self):
        self.__queue__.clear()

    def enqueue(self, passenger: Passenger):
        if len(self.__queue__) > 0:
            for i in range(len(self.__queue__)):
                if passenger.group_boarding_id_number() < self.__queue__[i].group_boarding_id_number():
                    self.__queue__.insert(i, passenger)
                    return
        self.__queue__.append(passenger)

    def dequeue(self):
        if len(self) == 0:
            raise KeyError("Cannot dequeue from empty Passenger Priority Queue")
        else:
            return self.__queue__.pop()

    def is_empty(self):
        return len(self.__queue__) == 0

    def __len__(self):
        return len(self.__queue__)

    def peek(self):
        if self.size() > 0:
            return self.__queue__[len(self.__queue__)-1]
        else:
            raise KeyError("Cannot peek on empty Passenger Priority Queue")
