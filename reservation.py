# Future imports
from __future__ import annotations

# Standard library imports
from re import search, IGNORECASE
from datetime import datetime, date, time
from json import dumps, load

# Third-party imports
from fpdf import FPDF, enums


class Reservation:
    """A class used to represent a restaurant reservation.

    **Class variables**
    :cvar _restaurant_tables: The number of tables in the restaurant.
    :vartype: int
    :cvar _tables_capacity: The number of people per table.
    :vartype: int
    :cvar _restaurant_capacity: The maximum number of customers.
    :vartype: int
    :cvar _reservation_slots: The predefined time slots when
    reservations can be made.
    :vartype: list

    **Attributes**
    :attr _name: The name of the person making the reservation.
    :type _name: str
    :attr _date: The date of the reservation.
    :type _date: date
    :attr _time: The time of the reservation.
    :type _time: time
    :attr _people: The number of people who will attend.
    :type _people: int

    **Public methods**
    :meth create_reservation: Creates a new reservation and stores it
    in the database.
    :meth read_reservation: Gets the data of a reservation stored in
    the database.
    :meth update_reservation: Updates the data of a reservation
    stored in the database.
    :meth delete_reservation: Deletes a reservation stored in the
    database.
    """

    # Class variables
    _restaurant_tables: int = 4
    _tables_capacity: int = 4
    _restaurant_capacity: int = 16
    _reservation_slots: list = [
        time(12, 0),
        time(14, 0),
        time(20, 0),
        time(22, 0),
    ]

    # Special methods
    def __init__(
            self,
            rname: str,
            rdate: str = "1-1-3000",
            rtime: str = "12:00",
            rpeople: str = "0"
    ) -> None:
        """Initialize a Reservation object.

        :param rname: The name of the person making the reservation.
        :type rname: str
        :param rdate: The date of the reservation (default "1-1-3000").
        :type rdate: str
        :param rtime: The time of the reservation (default "12:00").
        :type rtime: str
        :param rpeople: The number of people who will attend
        (default "0").
        :type rpeople: str
        """

        self._name: str = rname
        self._date: date = rdate
        self._time: time = rtime
        self._people: int = rpeople

    def __str__(self) -> str:
        """Return a string representation of a Reservation instance.

        :return: A string with the information of a Reservation
        instance.
        :rtype: str
        """

        return (
            f"Reservation for {self._people} people "
            f"in the name of {self._name} "
            f"for {self._date.strftime("%A, %d %B, %Y")} "
            f"at {self._time.strftime("%I %p")}."
        )

    # Getters and Setters
    @property
    def _name(self) -> str:
        """Get the name of the reservation.

        :return: The name of the person making the reservation.
        :rtype: str
        """

        return self._rname

    @_name.setter
    def _name(self, name: str) -> None:
        """Set the name attribute value of the reservation.

        :param name: The name attribute value of the Reservation
        instance.
        :type name: str
        """

        while True:
            try:
                validated_name: str = self._validate_name(name)
                break
            except ValueError:
                name: str = input(
                    "Invalid name. "
                    "Please, re-enter your name (first and last): "
                )
                continue
        self._rname: str = validated_name

    @property
    def _date(self) -> date:
        """Get the date of the reservation.

        :return: A date object representing the date of the reservation.
        :rtype: date
        """

        return self._rdate

    @_date.setter
    def _date(self, rdate: str) -> None:
        """Set the date attribute value of the reservation.

        :param rdate: The date attribute value of the Reservation
        instance.
        :type rdate: str
        """

        while True:
            try:
                validated_date: date = self._validate_date(rdate)
                break
            except(ValueError, TypeError, AttributeError):
                rdate: str = input(
                    "Invalid date. "
                    "Please, re-enter the date (dd-mm-yyyy): "
                )
                continue
        self._rdate: date = validated_date

    @property
    def _time(self) -> time:
        """Get the time of the reservation.

        :return: A time object representing the time of the reservation.
        :rtype: time
        """

        return self._rtime

    @_time.setter
    def _time(self, rtime: str) -> None:
        """Set the time attribute value of the reservation.

        :param rtime: The time attribute of the Reservation instance.
        :type rtime: str
        """

        while True:
            try:
                validated_time: time = self._validate_time(rtime)
                break
            except(ValueError, TypeError, AttributeError):
                rtime: str = input(
                    "Invalid time. "
                    "Please, re-enter the time (hh:mm, 24h format): "
                )
                continue
        self._rtime: time = validated_time

    @property
    def _people(self) -> int:
        """Get the number of people who will attend the reservation.

        :return: The number of people who will attend the reservation.
        :rtype: int
        """

        return self._rpeople

    @_people.setter
    def _people(self, people: str) -> None:
        """Set the people attribute value of the reservation.

        :param people: The people attribute of the Reservation instance.
        :type people: str
        """

        while True:
            try:
                validated_people: int = self._validate_people(people)
                break
            except AttributeError:
                people: str = input(
                    "Invalid number. "
                    "Please, re-enter the number of people "
                    "(type a numeric number between 1 and 16): "
                )
                continue
        self._rpeople: int = validated_people

    # Validation methods
    @staticmethod
    def _validate_name(name: str) -> str:
        """Validate and format the name entered by the user.

        :param name: The user's name in the format "first-name
        last-name".
        :type name: str
        :return: A formated string in the format "First-name Last-name".
        :rtype: str
        :raise ValueError: If name isn't in the correct "first-name
        last-name" format.
        """

        if matches := search(
            r"^([a-zñáéíóú]{1,20}) ([a-zñáéíóú]{1,20})$", name, IGNORECASE
        ):
            return f"{matches.group(1).title()} {matches.group(2).title()}"
        else:
            raise ValueError("Name not valid")

    @staticmethod
    def _validate_date(rdate: str) -> date:
        """Convert and validate a date string into a date object.

        :param rdate: The date string in "dd-mm-yyyy" format.
        :type rdate: str
        :return: The corresponding date object.
        :rtype: date
        :raise ValueError: If rdate is in the past or improperly
        formatted.
        :raise TypeError: If a non-numeric value is entered.
        :raise AttributeError: If rdate isn't in the correct
        "xx-xx-xxxx" hyphens format.
        """

        current_date: date = date.today()
        reservation_date: str = search(r"^(\d{1,2})-(\d{1,2})-(\d{4})$", rdate)
        validated_date: date = date(
            year=int(reservation_date.group(3)),
            month=int(reservation_date.group(2)),
            day=int(reservation_date.group(1)),
        )
        if validated_date < current_date:
            raise ValueError("The date entered has already passed")
        else:
            return validated_date

    def _validate_time(self, rtime: str) -> time:
        """Convert and validate a time string into a time object.

        :param rtime: The time string in "hh:mm" 24h format.
        :type rtime: str
        :return: The corresponding time object.
        :rtype: time
        :raise ValueError: If the time is in the past or improperly
        formatted.
        :raise TypeError: If a non-numeric value is entered.
        :raise AttributeError: If rtime isn't in the correct "xx:xx"
        colon format.
        """

        current_date: date = datetime.today().date()
        current_time: time = datetime.today().time()
        # TODO: Replace hardcode. Use _reservation_slots
        reservation_time: str = search(r"^(12|14|20|22):(00)$", rtime)
        validated_time: time = time(
            hour=int(reservation_time.group(1)),
            minute=int(reservation_time.group(2)),
        )
        if self._date <= current_date and validated_time < current_time:
            raise ValueError("The date entered has already passed")
        else:
            return validated_time

    @staticmethod
    def _validate_people(people: str) -> int:
        """Convert and validate a number string into a integer.

        :param people: A number string in "n" format.
        :type people: str
        :return: A corresponding integer number.
        :rtype: int
        :raise AttributeError: If people's value is anything but a
        number between 1 and 16, both included.
        """

        reservation_people: str = search(r"^([0-1]?[0-6]|[7-9])$", people)
        return int(reservation_people.group(1))

    # CRUD reservation methods
    @classmethod
    def create_reservation(cls) -> None:
        """Create a new reservation.

        This method prints the constraints and requests the necessary
        data to create a reservation object with it to store it as a
        dictionary in a json file database.
        It checks for availability in the database based on the user
        data and the restaurant constraints and exits the program if
        there is none. If available, updates the database with the new
        reservation, exports a confirmation pdf with the reservation
        info and prints a confirmation message.
        """

        # Get data from user and check availability
        print(cls._get_name_constraints())
        reservation: Reservation = cls(cls._request_name())
        if not cls._check_name_availability(reservation):
            exit("There is already a reservation with that name.")
        reservation._date = cls._request_date()
        print(cls._get_time_constraints())
        reservation._time = cls._request_time()
        print(cls._get_people_constraints())
        reservation._people = cls._request_people()
        if not cls._check_reservation_availability(reservation):
            exit(
                "Sorry, we do not have availability "
                "for the data you have provided."
            )
        # Update database and confirmation
        cls.__update_database(reservation)
        cls._create_confirmation_document(reservation)
        print(cls._get_confirmation_message())

    @classmethod
    def display_reservation(cls) -> None:
        """Display reservation details for a given name.

        This method prompts the user for a name and creates and object
        with it and its default values. If there is not a reservation in
        the database associated with that name, it prints a no
        reservation message. Otherwise, it gets the details from
        the reservation, updates the object with them and prints it.
        """

        # Get name from user and check if exists in database
        reservation: Reservation = cls(cls._request_name())
        if cls._check_name_availability(reservation):
            print("There is no reservation with that name.")
        else:
            # Update object data and print it
            for database_reservation in cls.__get_reservations():
                if reservation._name == database_reservation["name"]:
                    year, month, day = database_reservation["date"].split("-")
                    reservation._date = f"{day}-{month}-{year}"
                    reservation._time = database_reservation["time"]
                    reservation._people = str(database_reservation["people"])
            print(reservation)

    @classmethod
    def update_reservation(cls) -> None:
        """Update a reservation stored in the database.

        This method calls the cancel_reservation method to remove the
        reservation details the user wants to update, displays a message
        to the user to enter the new details and calls the
        create_reservation method to add the new reservation details
        to the database.
        """

        cls.cancel_reservation()
        print("Please, enter the new reservation details: ")
        cls.create_reservation()

    @classmethod
    def cancel_reservation(cls) -> None:
        """
        Remove a reservation stored in the database.

        ...
        """

        # TODO: Refactor method

        # Get name from user and check if exists in database
        user_reservation: Reservation = cls(cls._request_name())
        if cls._check_name_availability(user_reservation):
            print("There is no reservation with that name.")
        else:
            # Get list of database reservations
            database_reservations: list = cls.__get_reservations()
            # Create a new list without the previous user reservation
            updated_reservations: list = [
                reservation for reservation in database_reservations
                if reservation["name"] != user_reservation._name
            ]
            # Create a dictionary with numbered reservations
            numbered_reservations: dict = {
                str(i + 1): 
                    reservation for i, reservation
                    in enumerate(updated_reservations)
            }
            # Write the updated reservations back to the JSON file
            with open("reservation_database.json", "w") as database:
                database.write(dumps(numbered_reservations, indent=4))
            # Confirmation
            print("Your reservation has been cancelled.")

    # Request methods
    @staticmethod
    def _request_name() -> str:
        """Request the user to input the name for the reservation.

        :return: The reservation name entered by the user.
        :rtype: str
        """

        return input("Enter the name of the reservation (first and last): ")

    @staticmethod
    def _request_date() -> str:
        """Request the user to input the date for the reservation.

        :return: The reservation date entered by the user.
        :rtype: str
        """

        return input("Enter the date of the reservation (dd-mm-yyyy): ")

    @staticmethod
    def _request_time() -> str:
        """Request the user to input the time for the reservation.

        :return: The reservation time entered by the user.
        :rtype: str
        """

        return input("Enter the time of the reservation (hh:mm, 24h format): ")

    @staticmethod
    def _request_people() -> str:
        """Request the user to input the number of people who will attend
        the reservation.

        :return: The reservation number of people entered by the user.
        :rtype: str
        """

        return input("Enter the number of people attending: ")

    # Check availability in the database
    @classmethod
    def _check_name_availability(cls, user_reservation: Reservation) -> bool:
        """Verify whether the name provided by the user is available
        for a reservation.

        :param user_reservation: An instance of the Reservation class
        containing the user's details.
        :type user_reservation: Reservation
        :return: True if the name is available, False otherwise.
        :rtype: bool
        """

        # Retrieve the list of current reservations from the database
        database_reservations: list = cls.__get_reservations()
        # Check if any reservation already uses the provided name
        for database_reservation in database_reservations:
            if database_reservation["name"] == user_reservation._name:
                return False
        return True

    @classmethod
    def _check_reservation_availability(
        cls, user_reservation: Reservation
    ) -> bool:
        """Check if a reservation can be made based on the restaurant's
        current availability.

        This method verifies the availability of tables for the
        specified date, time and number of people, and ensures the
        reservation request aligns with capacity constraints.

        :param user_reservation: An instance of the Reservation class
        containing reservation details.
        :type user_reservation: Reservation
        :return: True if the reservation can be accommodated,
        False otherwise.
        :rtype: bool
        """

        # TODO: refactor this and add comments
        database_reservations: list = cls.__get_reservations()
        tables_available: int = cls._restaurant_tables
        for database_reservation in database_reservations:
            if(
                database_reservation["date"]
                == user_reservation._date.strftime("%Y-%m-%d")
            ):
                if(
                    database_reservation["time"]
                    == user_reservation._time.strftime("%H:%M")
                ):
                    match database_reservation["people"]:
                        case 1 | 2 | 3 | 4:
                            tables_available -= 1
                        case 5 | 6 | 7 | 8:
                            tables_available -= 2
                        case 9 | 10 | 11 | 12:
                            tables_available -= 3
                        case 13 | 14 | 15 | 16:
                            tables_available -= 4
        return(
            False if(
                tables_available == 0
                or (user_reservation._people
                    / tables_available > cls._tables_capacity)
                or user_reservation._people / tables_available < 0
            )
            else True
        )

    # Get contraints methods
    @staticmethod
    def _get_name_constraints() -> str:
        """Return a message explaining the name constraints for
        reservations.

        :return: A string describing the name constraints.
        :rtype: str
        """

        return "Only one reservation per person is allowed."

    @classmethod
    def _get_time_constraints(cls) -> str:
        """Return a message explaining the time constraints for
        reservations.

        :return: A string describing the time constraints.
        :rtype: str
        """

        return(
            "Time slots for reservations: "
            + ", ".join(t.strftime("%H:%M") for t in cls._reservation_slots)
        )

    @classmethod
    def _get_people_constraints(cls) -> str:
        """Return a message explaining the people constraints for
        reservations.

        :return: A string describing the people constraints.
        :rtype: str
        """

        return(
            "Maximum capacity of the restaurant by time slots: "
            f"{cls._restaurant_capacity}, "
            f"{cls._restaurant_tables} tables of "
            f"{cls._tables_capacity} people each."
        )

    # Closing messages methods
    # TODO: Refactor functionality of this methods
    @staticmethod
    def _get_confirmation_message() -> str:
        """Return a confirmation message for a reservation.

        :return: A string confirming the operation.
        :rtype: str
        """

        return(
            "Reservation confirmed! You will shortly receive a "
            "reminder document with the appointment details."
        )

    @staticmethod
    def _get_delete_message() -> str:
        """Return a delete confirmation message for a reservation.

        :return: A confirmation message indicating that the
        reservation was canceled.
        :rtype: str
        """

        return "Reservation deleted."

    # Other methods
    @staticmethod
    def _create_confirmation_document(reservation) -> None:
        """Export a pdf with the confirmation and reservation details.

        :param reservation: A reservation object with the
        reservation details.
        :type reservation: Reservation
        """

        # Document object
        pdf = FPDF()
        # Document title
        pdf.add_page()
        pdf.set_font("helvetica", "B", 24)
        pdf.cell(
            w=0,
            h=20,
            text="Reservation confirmed!",
            border="B",
            align="C",
            new_x=enums.XPos.LMARGIN,
            new_y=enums.YPos.NEXT,
        )
        # Blank line
        pdf.cell(
            0, 10, "", new_x=enums.XPos.LMARGIN, new_y=enums.YPos.NEXT
        )
        # Document body
        pdf.set_font("helvetica", "", 14)
        pdf.multi_cell(
            w=100, h=5, text=str(reservation), center=True, align="C"
        )
        # Document exportation
        pdf.output("reservation.pdf")

    @classmethod
    def __update_database(cls, user_reservation: Reservation) -> None:
        """Update the database to include a new reservation.

        The database is stored in a JSON file. The new reservation is
        added, and the reservations are sorted by date and time before
        saving.

        :param user_reservation: A reservation object with the details
        of the new reservation.
        :type user_reservation: Reservation
        """

        # Load the current reservations from the database
        reservations_database: list = cls.__get_reservations()
        # Add the new reservation as a dictionary
        reservations_database.append(
            {
                "name": user_reservation._name,
                "date": user_reservation._date.strftime("%Y-%m-%d"),
                "time": user_reservation._time.strftime("%H:%M"),
                "people": user_reservation._people,
            }
        )
        # Sort reservations by date, then by time
        sorted_reservations: list = sorted(
            reservations_database,
            key=lambda item: (item["date"], item["time"]),
        )
        # Create a dictionary with numbered reservations
        numbered_reservations: dict = {
            str(i + 1): 
                reservation for i, reservation
                in enumerate(sorted_reservations)
        }
        # Write the updated reservations back to the JSON file
        with open("reservation_database.json", "w") as database:
            database.write(dumps(numbered_reservations, indent=4))

    @staticmethod
    def __get_reservations() -> list:
        """Retrieve all reservations from the JSON file database.

        :return: A list of reservations, where each reservation is
        represented as a dictionary.
        :rtype: list
        """

        with open("reservation_database.json", "r") as database:
            database_dict: dict = load(database)
        return list(database_dict.values())


def main():
    """Main function of the script.

    Prompt the user to choose an action: create, update, update,
    retrieve or delete a restaurant reservation, and then performs the
    selected task.
    """

    match (
        input(
            "\nWelcome to our restaurant! "
            "How can we help you?\n"
            "(Please select one of the options "
            "by typing 'a', 'b', 'c', 'd' or 'e' and press enter):\n"
            "a. Create a new reservation.\n"
            "b. Show my reservation details.\n"
            "c. Update my reservation details.\n"
            "d. Cancel my reservation.\n"
            "e. Exit.\n"
            ": "
        ).lower()
    ):
        case "a":
            Reservation.create_reservation()
        case "b":
            Reservation.display_reservation()
        case "c":
            Reservation.update_reservation()
        case "d":
            Reservation.cancel_reservation()
        case "e":
            pass
        case _:
            print("The option entered is not correct")
    print("Thanks and see you soon!")


if __name__ == "__main__":
    main()
