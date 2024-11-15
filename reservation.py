from __future__ import annotations
from re import search, IGNORECASE
from datetime import datetime
from fpdf import FPDF, enums
from json import dumps, load


class Reservation:
    """
    A class representing a reservation for a resturant.

    Attributtes:
        name (str): The name of the person making the reservation.
        date_time (datetime): The date and the time of the reservation.
        people (int): The number of people who will attend.
    """

    def __init__(self, name: str, date_time: str, people: str) -> None:
        """
        Initializes a Reservation object.

        Parameters:
            name (str): The name of the person making the reservation.
            date_time (str): The date and the time of the reservation.
            people (str): The number of people who will attend.
        """
        self.name: str = name
        self.date_time: datetime = date_time
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
            f"for {self.date_time.strftime("%A, %d %B, %Y")} " +  
            f"at {self.date_time.strftime("%I%p")}."
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
        return cls(name, f"{date} {time}", people)

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
    def date_time(self) -> datetime:
        """
        Gets the date and the time of the reservation.

        Returns:
            Datetime: A datetime object of the date and time attribute of the Reservation instance.
        """
        return self._date_time

    @date_time.setter
    def date_time(self, date_time: str) -> None:
        """
        Sets the date and time attribute value of the reservation.
        """
        while True:
            try:
                cleaned_datetime: datetime = self.clean_datetime(date_time)
                break
            except (ValueError, TypeError, AttributeError):
                date_time: str = input(
                    "Invalid date and/or time. Please, re-enter the date (dd/mm/yyyy): "
                ) + " " + input(
                    "re-enter the time (hh:mm, 24h format): "
                )
                continue
        self._date_time = cleaned_datetime

    @staticmethod
    def clean_datetime(date_time: str) -> datetime:
        """
        Cleans and converts a date and a time introduced by a user into a datetime object.

        Parameters:
            date_time (str): a string date and time in the form of "dd/mm/yyy hh:mm".
        Returns:
            Datetime: A datetime object that includes the date and time of the reservation.
        Raises:
            ValueError:
                - If the date and/or time entered by the user is before the current date or time.
                - If the day, month, year, hour or minute values are not correct.
            AttributeError: If date and/or time aren't in the correct format.
            TypeError: If the user enters a value other than numbers.
        """
        current_datetime = datetime.today()
        reserve_datetime = search(r"^(\d{1,2})\/(\d{1,2})\/(\d{4}) (\d{1,2}):(\d{1,2})$", date_time)

        day = int(reserve_datetime.group(1))
        month = int(reserve_datetime.group(2))
        year = int(reserve_datetime.group(3))
        hours = int(reserve_datetime.group(4))
        minutes = int(reserve_datetime.group(5))

        cleaned_datetime = datetime(year, month, day, hours, minutes)

        if (cleaned_datetime < current_datetime):
            raise ValueError("The date entered has already passed")
        else:
            return cleaned_datetime

    @property
    def people(self) -> int:
        """
        Gets the number of people who will attend the reservation.

        Returns:
            Integer: An int for the number of people who will attend the reservation.
        """
        return self._people

    @people.setter
    def people(self, people: str) -> None:
        """
        Sets the people attribute value of the reservation.
        """
        while True:
            try:
                cleaned_people: int = int(people)
                break
            except ValueError:
                people: str = input("Invalid number. Please, re-enter the number of people (type a numeric number): ")
                continue
        self._people = cleaned_people

    def create_reservation(self) -> str:
        """
        Adds a new reservation in a reservation_database.json document.

        Returns:
            String: A string messsage with the confirmation of the reservation.
        """
        # Open database.json file and load it as a dict object
        with open("reservation_database.json", "r") as database:
            database_dict: dict = load(database)
        # Extract a list of the reservation dicts only 
        database_reservations = list(database_dict.values())
        # Add the new reservation to it
        database_reservations.append({
            "name": self.name,
            "date_time": f"{self.date_time}",
            "people": self.people
        })
        # Sort the reservations list by date
        sorted_database_reservations = sorted(
            database_reservations,
            key = lambda item : item["date_time"]
        )
        # Create a new dictionary with the numbered reservations
        new_database_dict = {}
        for i, reservation in enumerate(sorted_database_reservations):
            new_database_dict[f"{i + 1}"] = reservation
        # Open database and overwrite it with a new database dict
        with open("reservation_database.json", "w") as database:
            database.write(dumps(new_database_dict, indent=4))
        # Export confirmation document
        self.create_confirmation_document()

        return "Reservation confirmed! You will shortly receive a reminder document with the appointment details."

    @staticmethod
    def read_reservation(name) -> str:
        """
        Gets the information of a reservation/s from the database.

        Parameters:
            name (str): A name entered by the user to check the database for reservations.
        Returns:
            String: A string with the information of a reservation/s or a no reservations message.
        """
        # Open database.json file and load it as a dict object
        with open("reservation_database.json", "r") as database:
            database_dict: dict = load(database)
        # Extract a list of the reservation dicts only
        database_reservations = list(database_dict.values())
        # Define the variable to be returned
        matching_reservations = ""
        # Check reservations based on the argument “name” and return the info
        for reservation in database_reservations:
            if reservation["name"] == name:
                matching_reservations += (
                    f"{reservation["name"]} has a reservation on " + 
                    f"{reservation["date_time"][:10]} at " + # To "space" char
                    f"{reservation["date_time"][11:16]} for " + # From "space" char to minutes
                    f"{reservation["people"]} people.\n"
                )
        if matching_reservations:
            return matching_reservations[:len(matching_reservations) - 1] # Remove the last line break 
        else:
            return "The reservation could not be found. Please check the name entered."


    def update_reservation(): ...

    def delete_reservation():
        # Reset the reservation "id"s in the database in case there has been any modification in the database.
        ...

    def create_confirmation_document(self) -> None:
        # Reservation reminder document object
        pdf = FPDF()
        # Reservation reminder document title
        pdf.add_page()
        pdf.set_font("helvetica", "B", 24)
        pdf.cell(
            w = 0,
            h = 20,
            text = "Reservation confirmed!",
            border = "B",
            align = "C",
            new_x = enums.XPos.LMARGIN,
            new_y = enums.YPos.NEXT
        )
        # Blank line
        pdf.cell(0, 10, "", new_x = enums.XPos.LMARGIN, new_y = enums.YPos.NEXT)
        # Reservation reminder document body
        pdf.set_font("helvetica", "", 14)
        pdf.multi_cell(
            w = 100,
            h = 5,
            text = self.__str__(),
            center = True,
            align = "C"
        )
        # Export document
        pdf.output("reservation.pdf")


def main(): ...


if __name__ == "__main__":
    main()
