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
        return (
            f"Reservation for {self.people} people " +  
            f"in the name of {self.name} " + 
            f"for {self.date.strftime("%A, %d %B, %Y")} " +  
            f"at {self.time.strftime("%I%p")}."
        )

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
        Gets the name of the reservation.

        Returns:
            String: A string of the name attribute of the Reservation instance.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Sets the name attribute value of the reservation.
        """
        while True:
            try:
                cleaned_name: str = self.clean_name(name)
                break
            except ValueError:
                name: str = input("Invalid name. Please, re-enter your name (first and last): ")
                continue
        self._name = cleaned_name

    @staticmethod
    def clean_name(name: str) -> str:
        """
        Validates and cleans a name introduced by a user.

        Parameters:
            name (str): A string in the form of "first-name last-name".
        Returns:
            String: A string in the form of "First-name Last-name".
        Raises:
            ValueError: If name isn't in the correct format.
        """
        if matches := search(r"^([a-z]{1,20}) ([a-z]{1,20})$", name, IGNORECASE):
            return f"{matches.group(1).title()} {matches.group(2).title()}"
        else:
            raise ValueError("Name not valid")

    @property
    def date(self) -> datetime.date:
        """
        Gets the date of the reservation.

        Returns:
            datetime.Date: A date object of the date attribute of the Reservation instance.
        """
        return self._date

    @date.setter
    def date(self, date: str) -> None:
        """
        Sets the date attribute value of the reservation.
        """
        while True:
            try:
                cleaned_date: datetime.date = self.clean_date(date)
                break
            except (ValueError, TypeError):
                date: str = input("Invalid date. Please, re-enter the date (dd/mm/yyyy): ")
                continue
        self._date = cleaned_date

    @staticmethod
    def clean_date(date: str) -> datetime.date:
        """
        Cleans and converts a date introduced by a user into a datetime object.

        Parameters:
            date (str): a string date in the form of "dd/mm/yyy".
        Returns:
            datetime.date: A date object.
        Raises:
            ValueError:
                - If date isn't in the correct format.
                - If the date entered by the user is before the current date.
                - If the day, month or year values are not correct.
            TypeError: If the user enters a value other than numbers.
        """
        MINDAY = 0
        MAXDAY = 31
        MINMONTH = 0
        MAXMONTH = 12
        current_date = datetime.date.today()
        reserve_date = search(r"^(\d{1,2})\/(\d{1,2})\/(\d{4})$", date)

        day = int(reserve_date.group(1))
        month = int(reserve_date.group(2))
        year = int(reserve_date.group(3))

        if (
            day < MINDAY or
            day > MAXDAY or
            month < MINMONTH or
            month > MAXMONTH or
            year < datetime.MINYEAR or
            year > datetime.MAXYEAR
        ): 
            raise ValueError

        cleaned_date = datetime.date(year, month, day)

        if (cleaned_date < current_date):
            raise ValueError
        else:
            return cleaned_date

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
