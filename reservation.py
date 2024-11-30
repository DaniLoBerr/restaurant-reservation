# Standard imports
from __future__ import annotations
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
    :cvar _reservation_slots: The predefined time slots when reservations 
    can be made.
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
        time(22, 0)
    ]

    # Special methods
    def __init__(
            self,
            rname: str,
            rdate: str = "1-1-3000",
            rtime: str = "12:00",
            rpeople: str = "0"
        ) -> None:
        """Initializes a Reservation object.

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
        """Returns a string representation of a Reservation instance.

        :return: A string with the information of a Reservation instance.
        :rtype: str
        """

        return (
            f"Reservation for {self._people} people " +
            f"in the name of {self._name} " +
            f"for {self._date.strftime("%A, %d %B, %Y")} " +
            f"at {self._time.strftime("%I %p")}."
        )

    # Getters and Setters
    @property
    def _name(self) -> str:
        """Gets the name of the reservation.

        :return: The name of the person making the reservation.
        :rtype: str
        """

        return self._rname

    @_name.setter
    def _name(self, name: str) -> None:
        """Sets the name attribute value of the reservation.

        :param name: The name attribute value of the Reservation instance.
        :type name: str
        """

        while True:
            try:
                validated_name: str = self._validate_name(name)
                break
            except ValueError:
                name: str = input("Invalid name. Please, re-enter your name (first and last): ")
                continue
        self._rname = validated_name

    @property
    def _date(self) -> date:
        """Gets the date of the reservation.

        :return: A date object representing the date of the reservation.
        :rtype: date
        """

        return self._rdate

    @_date.setter
    def _date(self, rdate: str) -> None:
        """Sets the date attribute value of the reservation.

        :param rdate: The date attribute value of the Reservation instance.
        :type rdate: str
        """

        while True:
            try:
                validated_date: date = self._validate_date(rdate)
                break
            except (ValueError, TypeError, AttributeError):
                rdate: str = input("Invalid date . Please, re-enter the date (dd-mm-yyyy): ")
                continue
        self._rdate = validated_date

    @property
    def _time(self) -> time:
        """Gets the time of the reservation.

        :return: A time object representing the time of the reservation.
        :rtype: time
        """

        return self._rtime

    @_time.setter
    def _time(self, rtime: str) -> None:
        """Sets the time attribute value of the reservation.

        :param rtime: The time attribute of the Reservation instance.
        :type rtime: str
        """

        while True:
            try:
                validated_time: time = self._validate_time(rtime)
                break
            except (ValueError, TypeError, AttributeError):
                rtime: str = input("Invalid time . Please, re-enter the time (hh:mm, 24h format): ")
                continue
        self._rtime = validated_time

    @property
    def _people(self) -> int:
        """Gets the number of people who will attend the reservation.

        :return: The number of people who will attend the reservation.
        :rtype: int
        """

        return self._rpeople

    @_people.setter
    def _people(self, people: str) -> None:
        """Sets the people attribute value of the reservation.

        :param people: The people attribute of the Reservation instance.
        :type people: str
        """

        while True:
            try:
                validated_people: int = self._validate_people(people)
                break
            except AttributeError:
                people: str = input("Invalid number. Please, re-enter the number of people (type a numeric number between 1 and 16): ")
                continue
        self._rpeople = validated_people

    # Validation methods
    @staticmethod
    def _validate_name(name: str) -> str:
        """Validates and formats the name entered by the user.

        :param name: The user's name in the format "first-name last-name".
        :type name: str
        :return: A formated string in the format "First-name Last-name".
        :rtype: str
        :raise ValueError: If name isn't in the correct "first-name 
        last-name" format.
        """

        if matches := search(r"^([a-zñáéíóú]{1,20}) ([a-zñáéíóú]{1,20})$", name, IGNORECASE):
            return f"{matches.group(1).title()} {matches.group(2).title()}"
        else:
            raise ValueError("Name not valid")

    @staticmethod
    def _validate_date(rdate: str) -> date:
        """Converts and validates a date string into a date object.

        :param rdate: The date string in "dd-mm-yyyy" format.
        :type rdate: str
        :return: The corresponding date object.
        :rtype: date
        :raise ValueError: If rdate is in the past or improperly formatted.
        :raise TypeError: If a non-numeric value is entered.
        :raise AttributeError: If rdate isn't in the correct "xx-xx-xxxx" 
        hyphens format.
        """

        current_date = date.today()
        reservation_date = search(r"^(\d{1,2})-(\d{1,2})-(\d{4})$", rdate)
        validated_date = date(
            year = int(reservation_date.group(3)),
            month = int(reservation_date.group(2)),
            day = int(reservation_date.group(1))
        )
        if validated_date < current_date:
            raise ValueError("The date entered has already passed")
        else:
            return validated_date

    def _validate_time(self, rtime: str) -> time:
        """Converts and validates a time string into a time object.

        :param rtime: The time string in "hh:mm" 24h format.
        :type rtime: str
        :return: The corresponding time object.
        :rtype: time
        :raise ValueError: If the time is in the past or improperly formatted.
        :raise TypeError: If a non-numeric value is entered.
        :raise AttributeError: If rtime isn't in the correct "xx:xx" colon 
        format.
        """

        current_date = datetime.today().date()
        current_time = datetime.today().time()
        # TODO: Replace hardcode. Use _reservation_slots
        reservation_time = search(r"^(12|14|20|22):(00)$", rtime)
        validated_time = time(
            hour = int(reservation_time.group(1)),
            minute = int(reservation_time.group(2))
        )
        if self._date <= current_date and validated_time < current_time:
            raise ValueError("The date entered has already passed")
        else:
            return validated_time

    @staticmethod
    def _validate_people(people: str) -> int:
        """Converts and validates a number string into a integer.

        :param people: A number string in "n" format.
        :type people: str
        :return: A corresponding integer number.
        :rtype: int
        :raise AttributeError: If people's value is anything but a number
        between 1 and 16, both included.
        """

        reservation_people = search(r"^([0-1]?[0-6]|[7-9])$", people)
        return int(reservation_people.group(1))

    # CRUD reservation methods
    @classmethod
    def create_reservation(cls) -> None:
        """Creates a new reservation.
        
        This method prints the constraints and requests the necessary data
        to create a reservation object with it to store it as a dictionary 
        in a json file database.
        It checks for availability in the database based on the user data 
        and the restaurant constraints and exits the program if there is
        none. If available, updates the database with the new 
        reservation, exports a confirmation pdf with the reservation info 
        and prints a confirmation message.
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
            exit("Sorry, we do not have availability for the data you have provided.")
        # Update database and confirmation
        cls.__update_database(reservation)
        cls._create_confirmation_document(reservation)
        print(cls._get_confirmation_message())

    @classmethod
    def read_reservation(cls) -> None:
        """
        ...
        """
        # Pedir el nombre al usuario.
        # Validamos nombre.
        # Si es inválido, repreguntamos
        # Crear un objeto con ese nombre.
        # Comprobar que hay alguna reserva con el nombre de ese objeto
        # Si no hay reserva, salimos del programa con el mensaje de que no hay reserva
        # Si existe una reserva con ese nombre, convertimos esas reserva en un objeto y imprimos los datos de ese objeto por pantalla. Cerramos programa
        ...

    @classmethod
    def update_reservation(cls) -> None:
        """
        ...
        """
        # Pedir el nombre al usuario.
        # Validamos nombre.
        # Si es inválido, repreguntamos
        # Crear un objeto con ese nombre.
        # Comprobar que si hay alguna reserva con el nombre de ese objeto
        # Si ya existe una reserva con ese nombre: obtenemos el diccionaria de la base de datos con ese nombre
        # Lo convertimos en objeto
        # Preguntamos por fecha
        # Validamos fecha.
        # Si es inválida, repreguntamos.
        # Comprobar disponibildiad fecha
        # Si no hay disponibilidad, mandar mensaje y repreguntar por fecha con opción a cancelar.
        # Si hay disponibilidad, sustituimos la fecha del objeto
        # Preguntar por hora, mostrando las horas disponibles (comprobar disponibilidad), en formato de elige una opción, con opción a cancelar.
        # Validar opción que se marque
        # Si es inválida, repreguntamos
        # Sustituimos hora al objeto
        # Comprobar disponibilidad personas.
        # Enviar al usuario personas y mesas disponibles, con opción a cancelar.
        # Preguntar por personas.
        # Validar personas
        # Si es inválida, repreguntamos
        # Sustituimos personas al obejto
        # Con todos los datos, convertir el objeto en diccionario.
        # Agregarlo en la base de datos.
        # Enviar mensaje de sustitución.
        # Enviar pdf con los datos.
        ...

    @classmethod
    def delete_reservation(cls) -> None:
        """
        ...
        """
        # Pedir el nombre al usuario.
        # Validamos nombre.
        # Si es inválido, repreguntamos
        # Crear un objeto con ese nombre.
        # COmprobar que existe un diccionario con ese nombre en la base de datos
        # Si no existe, salimos del programa con mensaje.
        # Si existe, eliminamos el diccionario de la base de datos.
        # Reenumeramos la base de datos.
        # Salimos del programa con mensaje de confirmación de la eliminación
        ...

    # Request methods
    @staticmethod
    def _request_name() -> str:
        """Requests the user to input the name for the reservation.

        :return: The reservation name entered by the user.
        :rtype: str
        """

        return input("Enter the name of the reservation (first and last): ")

    @staticmethod
    def _request_date() -> str:
        """Requests the user to input the date for the reservation.

        :return: The reservation date entered by the user.
        :rtype: str
        """

        return input("Enter the date of the reservation (dd-mm-yyyy): ")

    @staticmethod
    def _request_time() -> str:
        """Requests the user to input the time for the reservation.

        :return: The reservation time entered by the user.
        :rtype: str
        """

        return input("Enter the time of the reservation (hh:mm, 24h format): ")

    @staticmethod
    def _request_people() -> str:
        """Requests the user to input the number of people who will attend 
        the reservation.

        :return: The reservation number of people entered by the user.
        :rtype: str
        """

        return input("Enter the number of people attending: ")

    # Check availability in the database
    @classmethod
    def _check_name_availability(cls, user_reservation: Reservation) -> bool:
        """Verifies whether the name provided by the user is available for a 
        reservation.

        :param user_reservation: An instance of the Reservation class 
        containing the user's details.
        :type user_reservation: Reservation
        :return: True if the name is available, False otherwise.
        :rtype: bool
        """

        # Retrieve the list of current reservations from the database
        database_reservations = cls.__get_reservations_list()
        # Check if any reservation already uses the provided name
        for database_reservation in database_reservations:
            if database_reservation["name"] == user_reservation._name:
                return False
        return True

    @classmethod
    def _check_reservation_availability(cls, user_reservation: Reservation) -> bool:
        """Checks if a reservation can be made based on the restaurant's 
        current availability.

        This method verifies the availability of tables for the specified date, 
        time and number of people, and ensures the reservation request aligns 
        with capacity constraints.

        :param user_reservation: An instance of the Reservation class containing 
        reservation details.
        :type user_reservation: Reservation
        :return: True if the reservation can be accommodated, False otherwise.
        :rtype: bool
        """

        #TODO: refactor this and add comments
        database_reservations = cls.__get_reservations_list()
        tables_available = cls._restaurant_tables
        for database_reservation in database_reservations:
            if database_reservation["date"] == user_reservation._date.strftime("%Y-%m-%d"):
                if database_reservation["time"] == user_reservation._time.strftime("%H:%M"):
                    match database_reservation["people"]:
                        case 1 | 2 | 3 | 4:
                            tables_available -= 1
                        case 5 | 6 | 7 | 8:
                            tables_available -= 2
                        case 9 | 10 | 11 | 12:
                            tables_available -= 3
                        case 13 | 14 | 15 | 16:
                            tables_available -= 4
        return False if (
            tables_available == 0 or
            user_reservation._people / tables_available > cls._tables_capacity or
            user_reservation._people / tables_available < 0
        ) else True

    # Get contraints methods
    @staticmethod
    def _get_name_constraints() -> str:
        """Returns a message explaining the name constraints for reservations.

        :return: A string describing the name constraints.
        :rtype: str
        """

        return "Only one reservation per person is allowed."

    @classmethod
    def _get_time_constraints(cls) -> str:
        """Returns a message explaining the time constraints for reservations.

        :return: A string describing the time constraints.
        :rtype: str
        """

        return(
            "Time slots for reservations: " + 
            ", ".join(t.strftime("%H:%M") for t in cls._reservation_slots)
        )

    @classmethod
    def _get_people_constraints(cls) -> str:
        """Returns a message explaining the people constraints for reservations.

        :return: A string describing the people constraints.
        :rtype: str
        """

        return (
            f"Maximum capacity of the restaurant by time slots: {cls._restaurant_capacity}, "
            f"{cls._restaurant_tables} tables of {cls._tables_capacity} people each."
        )

    # Closing messages
    @staticmethod
    def _get_confirmation_message() -> str:
        """
        Gets a message with the confirmation of the reservation.

        :return: A confirmation message.
        :rtype: str
        """
        return "Reservation confirmed! You will shortly receive a reminder document with the appointment details."

    @staticmethod
    def _get_delete_message() -> str:
        """
        Gets a message confirming the reservation deletion.

        :return: A confirming deletion message.
        :rtype: str
        """
        return "Reservation deleted."

    @staticmethod
    def get_goodbye_message() -> str:
        """
        Gets a message as a goodbye for the ending process of the reservation.

        :return: A goodbye message.
        :rtype: str
        """
        return "Thanks and see you soon!"

    # Other methods
    @staticmethod
    def _create_confirmation_document(reservation) -> None:
        """
        Generate a pdf with the confirmation and data of the reservation.

        :param reservation: A reservation object.
        :type reservation: Reservation
        """
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
            text = f"{reservation}",
            center = True,
            align = "C"
        )
        # Export document
        pdf.output("reservation.pdf")

    @classmethod
    def __update_database(cls, user_reservation: Reservation) -> None:
        """
        Updates the database to include a new reservation.

        :param user_reservation: A reservation object.
        :type user_reservation: Reservation
        """
        # Extract a list of the database reservations
        database_reservations = cls.__get_reservations_list()
        # Add the new reservation to the list
        database_reservations.append(dict(
            name = user_reservation._name,
            date = user_reservation._date.strftime("%Y-%m-%d"),
            time = user_reservation._time.strftime("%H:%M"),
            people = user_reservation._people
        ))
        # Sort the reservations list by date
        sorted_database_reservations = sorted(
            database_reservations,
            key = lambda item : item["date"]
        )
        # TODO: Sort by time also
        # Create a new dictionary with the numbered reservations
        new_database_dict = {}
        for i, reservation in enumerate(sorted_database_reservations):
            new_database_dict[f"{i + 1}"] = reservation
        # Open database and overwrite it with a new database dict
        with open("reservation_database.json", "w") as database:
            database.write(dumps(new_database_dict, indent=4))
        # Export confirmation document
        cls._create_confirmation_document(user_reservation)

    @staticmethod
    def __get_reservations_list() -> list:
        """
        Gets a list of all the reservations, in form of dictionaries, stored in the database.

        :return: A list of dictionary reservations.
        :rtype: list
        """
        with open("reservation_database.json", "r") as database:
            database_dict: dict = load(database)
        return list(database_dict.values())

def main():
    """
    Main function of the script whose purpose is to ask a user if he/she wants to
    create, update, get data or delete a restaurant reservation and perfom the
    selected task.
    """
    match(
        input(
            "\nWelcome to our restaurant! " +
            "How can we help you?\n" +
            "(Please select one of the options by typing a, b, c, d or e and press enter):\n" +
            "a. Create a new reservation.\n" +
            "b. Show my reservation details.\n" +
            "c. Update my reservation details.\n" +
            "d. Cancel my reservation.\n" +
            "e. Exit.\n" +
            ": "
        ).lower()
    ):
        case "a": Reservation.create_reservation()
        case "b": Reservation.read_reservation()
        case "c": Reservation.update_reservation()
        case "d": Reservation.delete_reservation()
        case "e": pass
        case _: exit("The option entered is not correct")
    print(Reservation.get_goodbye_message())


if __name__ == "__main__":
    main()
