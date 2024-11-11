import datetime

from __future__ import annotations
from re import search, IGNORECASE


class Reservation:
    """
    A class representing a reservation for a resturant.

    Attributtes:
        name (str): The name of the person making the reservation.
        date (datetime.date): The date of the reservation.
        time (datetime.time): The time of the reservation.
        people (int): The number of people who will attend.
    """

    def __init__(self, name: str, date: str, time: str, people: str) -> None:
        """
        Initializes a Reservation object.

        Parameters:
            name (str): The name of the person making the reservation.
            date (str): The date of the reservation.
            time (str): The time of the reservation.
            people (str): The number of people who will attend.
        """
        self.name: str = name
        self.date: datetime.date = date
        self.time: datetime.time = time
        self.people: int = people

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of a Reservation
        instance.

        Returns:
            String: a string with the information of a Reservation instance.
        """
        return f"Reservation for {self.people} people in the name of {self.name} for the {self.date} at {self.time}h."

    @classmethod
    def reserve(cls) -> Reservation:
        """
        Creates a Reservation instance with the name for the reservation, a date,
        a time and the people attending entered by the user.

        Returns:
            Reservation: an instance of Reservation.
        """
        name: str = input(
            "In whose name do you want to make the reservation? (type first and last name): "
        )
        date: str = input(
            "What day would you like to make a reservation? (dd/mm/yyyy): "
        )
        time: str = input("What time? (hh:mm, 24h format): ")
        people: str = input(
            "How many people will the reservation be for? (type a number): "
        )
        return cls(name, date, time, people)

    @property
    def name(self) -> str:
        """
        Get the name of the reservation.

        Returns:
            String: A string of the name attribute of the instance of Reservation.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Set the name attribute value of the reservation.
        """
        while True:
            try:
                cleaned_name: str = self.clean_name(name)
                break
            except ValueError:
                name: str = input("Invalid name. Please, re-enter your name: ")
                continue
        self._name = cleaned_name

    @staticmethod
    def clean_name(name: str) -> str:
        if matches := search(r"^([a-z]{1,20}) ([a-z]{1,20})$", name, IGNORECASE):
            return f"{matches.group(1).title()} {matches.group(2).title()}"
        else:
            raise ValueError("Name not valid")

    @property
    def date(self): ...

    @date.setter
    def date(self): ...

    @property
    def time(self): ...

    @time.setter
    def time(self): ...

    @property
    def people(self): ...

    @people.setter
    def people(self): ...

    def delete(self): ...

    def update(self): ...

    def confirmation(self): ...


def main(): ...


if __name__ == "__main__":
    main()
