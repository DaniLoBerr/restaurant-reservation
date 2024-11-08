class Reservation:
    """
    A class representing a reservation.

    Attributtes:
        name (str): The name of the person making the reservation.
        date (...): The date of the reservation.
        time (...): The time of the reservation.
        people (int): The number of people who will attend.
    """

    def __init__(self, name, date, time, people):
        """
        Initializes a Reservation object.

        Parameters:
            name (str): The name of the person making the reservation.
            date (...): The date of the reservation.
            time (...): The time of the reservation.
            people (int): The number of people who will attend.
        """
        self.name = name
        self.date = date
        self.time = time
        self.people = people
    
    def __string__(self):
        """
        ...

        Returns:
            ...
        """
        ...

    @classmethod
    def reserve(cls):
        """
        Creates a Reservation instance with the name for the reservation, a date,
        a time and the people attending entered by the user.

        Returns:
            Reservation: an instance of Reservation
        """
        name = input("In whose name do you want to make the reservation? (type first and last name): ")
        date = input("What day would you like to make a reservation? (dd/mm/yyyy): ")
        time = input("What time? (hh:mm, 24h format): ")
        people = input("How many people will the reservation be for? (type a number): ")
        return cls(name, date, time, people)

    @property
    def name(self):
        ...
    
    @name.setter
    def name(self):
        ...

    @property
    def date(self):
        ...
    
    @date.setter
    def date(self):
        ...
    
    @property
    def time(self):
        ...
    
    @time.setter
    def time(self):
        ...
    
    @property
    def people(self):
        ...
    
    @people.setter
    def people(self):
        ...
    
    def delete(self):
        ...
    
    def update(self):
        ...
    
    def confirmation(self):
        ...


def main():
    ...


if __name__ == "__main__":
    main()