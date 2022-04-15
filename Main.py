import Passengers
print("CONF #", " ID", "LAST NAME".rjust(20) + ",", "FIRST NAME".rjust(20), "GRP#")
print("".rjust(58, "-"))
passengers = Passengers.generate_passenger_list()
passengers.sort()
for passenger in passengers:
    print(passenger.confirmation_id, passenger.boarding_id.rjust(3), passenger.last_name.rjust(20) + ",", passenger.first_name.rjust(20), passenger.___group_boarding_id_number__(), str(type(passenger)))
