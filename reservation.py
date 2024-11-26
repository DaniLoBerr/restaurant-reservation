from __future__ import annotations
from re import search, IGNORECASE
from datetime import datetime, date, time
from fpdf import FPDF, enums
from json import dumps, load


class Reservation:
    """
    A class representing a reservation for a resturant.

    :param name: The name of the person making the reservation.
    :type name: str
    :param rdate: The date of the reservation.
    :type rdate: date
    :param rtime: The time of the reservation.
    :type rtime: time
    :param people: The number of people who will attend.
    :type people: int
    """
    # Class variables
    restaurant_tables = 4
    tables_capacity = 4
    restaurant_capacity = 16

    # Special methods
    def __init__(
            self,
            name: str,
            rdate: str = "1-1-3000",
            rtime: str = "12:00",
            people: str = "0"
        ) -> None:
        """
        Initializes a Reservation object.

        :param name: The name of the person making the reservation.
        :type name: str
        :param rdate: The date of the reservation.
        :type rdate: str
        :param rtime: The time of the reservation.
        :type rtime: str
        :param people: The number of people who will attend.
        :type people: str
        """
        self.name: str = name
        self.rdate: date = rdate
        self.rtime: time = rtime
        self.people: int = people

    def __str__(self) -> str:
        """
        Returns a string representation of a Reservation instance.

        :return: A string with the information of a Reservation instance.
        :rtype: str
        """
        return (
            f"Reservation for {self.people} people " +
            f"in the name of {self.name} " +
            f"for {self.rdate.strftime("%A, %d %B, %Y")} " +
            f"at {self.rtime.strftime("%I %p")}."
        )

    # Getters and Setters
    @property
    def name(self) -> str:
        """
        Gets the name of the reservation.

        :return: The name of the person making the reservation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Sets the name attribute value of the reservation.

        :param name: The name attribute value of the Reservation instance.
        :type name: str
        """
        while True:
            try:
                cleaned_name: str = self.clean_name(name)
                break
            except ValueError:
                name: str = input("Invalid name. Please, re-enter your name (first and last): ")
                continue
        self._name = cleaned_name

    @property
    def rdate(self) -> date:
        """
        Gets the date of the reservation.

        :return: A date object representing the date of the reservation.
        :rtype: date
        """
        return self._rdate

    @rdate.setter
    def rdate(self, rdate: str) -> None:
        """
        Sets the date attribute value of the reservation.

        :param rdate: The date attribute value of the Reservation instance.
        :type rdate: str
        """
        while True:
            try:
                cleaned_rdate: date = self.clean_date(rdate)
                break
            except (ValueError, TypeError, AttributeError):
                rdate: str = input("Invalid date . Please, re-enter the date (dd-mm-yyyy): ")
                continue
        self._rdate = cleaned_rdate

    @property
    def rtime(self) -> time:
        """
        Gets the time of the reservation.

        :return: A time object representing the time of the reservation.
        :rtype: time
        """
        return self._rtime

    @rtime.setter
    def rtime(self, rtime: str) -> None:
        """
        Sets the time attribute value of the reservation.

        :param rtime: The time attribute of the Reservation instance.
        :type rtime: str
        """
        while True:
            try:
                cleaned_rtime: time = self.clean_time(rtime)
                break
            except (ValueError, TypeError, AttributeError):
                rtime: str = input("Invalid time . Please, re-enter the time (hh:mm, 24h format): ")
                continue
        self._rtime = cleaned_rtime

    @property
    def people(self) -> int:
        """
        Gets the number of people who will attend the reservation.

        :return: The number of people who will attend the reservation.
        :rtype: int
        """
        return self._people

    @people.setter
    def people(self, people: str) -> None:
        """
        Sets the people attribute value of the reservation.

        :param people: The people attribute of the Reservation instance.
        :type people: str
        """
        while True:
            try:
                cleaned_people: int = self.clean_people(people)
                break
            except ValueError:
                people: str = input("Invalid number. Please, re-enter the number of people (type a numeric number between 1 and 16): ")
                continue
        self._people = cleaned_people

    # Validation methods
    @staticmethod
    def clean_name(name: str) -> str:
        """
        Validates and cleans a name introduced by a user.

        :param name: A string in the form of "first-name last-name".
        :type name: str
        :return: A string in the form of "First-name Last-name".
        :rtype: str
        :raises ValueError: If name isn't in the correct format.
        """
        if matches := search(r"^([a-zñáéíóú]{1,20}) ([a-zñáéíóú]{1,20})$", name, IGNORECASE):
            return f"{matches.group(1).title()} {matches.group(2).title()}"
        else:
            raise ValueError("Name not valid")

    @staticmethod
    def clean_date(rdate: str) -> date:
        """
        Cleans and converts a date introduced by a user into a date object.

        Parameters:
        :param rdate (str): a string date in the form of "dd-mm-yyyy".
        :type rdate: str
        :returns: A date object that includes the date of the reservation.
        :rtype: dtr
        :raises ValueError: If the date entered by the user is before the current date.
        :raises ValueError: If the day, month or year values are not correct.
        :raises AttributeError: If date isn't in the correct format.
        :raises TypeError: If the user enters a value other than numbers.
        """
        current_date = date.today()
        reservation_date = search(r"^(\d{1,2})-(\d{1,2})-(\d{4})$", rdate)
        cleaned_date = date(
            year = int(reservation_date.group(3)),
            month = int(reservation_date.group(2)),
            day = int(reservation_date.group(1))
        )
        if cleaned_date < current_date:
            raise ValueError("The date entered has already passed")
        else:
            return cleaned_date

    def clean_time(self, rtime: str) -> time:
        """
        Cleans and converts a time introduced by a user into a time object.

        :param rtime: A string time in the form of "hh:mm" with the 24h format.
        :type rtime: str
        :returns: A time object that includes the time of the reservation.
        :rtype: time
        :raises ValueError: If the time entered by the user is before the current date and time.
        :raises ValueError: If the hour or minute values are not correct.
        :raises AttributeError: If time isn't in the correct format.
        :raises TypeError: If the user enters a value other than numbers.
        """
        current_date = datetime.today().date()
        current_time = datetime.today().time()
        reservation_time = search(r"^(12|14|20|22):(00)$", rtime)
        cleaned_time = time(
            hour = int(reservation_time.group(1)),
            minute = int(reservation_time.group(2))
        )
        if self.rdate <= current_date and cleaned_time < current_time:
            raise ValueError("The date entered has already passed")
        else:
            return cleaned_time

    def clean_people(self, people: str) -> int:
        """
        Cleans and converts a number of people introduced by a user into a time object.

        :param people: a string number in the form of "n".
        :type people: str
        :return: An integer representing the number of people that will attend to the restaurant.
        :rtype: int
        :raises ValueError: If the number entered by the user is less than 1 or greater than 16.
        :raises AttributeError: If time isn't in the correct format.
        :raises TypeError: If the user enters a value other than numbers.
        """
        reservation_people = search(r"^([0-1]?[0-6]|[7-9])$", people)
        cleaned_people = int(reservation_people.group(1))
        if cleaned_people == None:
            raise ValueError("The number entered is not valid")
        else:
            return cleaned_people

    # CRUD reservations
    @classmethod
    def create_reservation(cls) -> str:
        """
        Creates a new reservation, stores it in the database and creates a pdf document with the info

        :return: A string with the result of the operation.
        :rtype: str
        """
        print(cls.get_name_constraints())
        reservation: Reservation = cls(cls.request_name())
        if not cls.check_name_availability(reservation):
            return "There is already a reservation with that name."
        
        reservation.rdate = cls.request_date()
        print(cls.get_time_constraints())
        reservation.rtime = cls.request_time()
        print(cls.get_people_constraints())
        reservation.people = cls.request_people()
        if not cls.check_reservation_availability(reservation):
            return "Sorry, we do not have availability for the data you have provided."
        
        cls.update_database(reservation)
        cls.create_confirmation_document(reservation)
        return cls.get_confirmation_message()

    @classmethod
    def read_reservation(cls):
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
    def update_reservation(cls):
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
    def delete_reservation(cls):
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
    def request_name() -> str:
        """
        Requests the user for the name of the reservation.

        :return: The name entered by the user for the reservation.
        :rtype: str
        """
        return input("Enter the name of the reservation (first and last): ")

    @staticmethod
    def request_date() -> str:
        """
        Requests the user for the date of the reservation.

        :return: The date entered by the user for the reservation.
        :rtype: str
        """
        return input("Enter the date of the reservation (dd-mm-yyyy): ")

    @staticmethod
    def request_time() -> str:
        """
        Requests the user for the name of the reservation.

        :return: The time entered by the user for the reservation.
        :rtype: str
        """
        return input("Enter the time of the reservation (hh:mm, 24h format): ")

    @staticmethod
    def request_people() -> str:
        """
        Requests the user for the number of people who will attend the reservation.

        :return: The number of people who will attend the reservation.
        :rtype: str
        """
        return input("Enter the number of people attending: ")

    # Check availability in the database
    @classmethod
    def check_name_availability(cls, user_reservation: Reservation) -> bool:
        """
        Checks if the name entered by the user is available to make a reservation.

        :param user_reservation: A reservation object.
        :type user_reservation: Reservation
        :return: True if the name entered by the user is available, False if is not.
        :rtype: bool
        """
        database_reservations = cls.get_list_of_reservations()
        for database_reservation in database_reservations:
            if database_reservation["name"] == user_reservation.name:
                return False
        return True

    @classmethod
    def check_reservation_availability(cls, user_reservation: Reservation) -> bool:
        """
        Checks if the name entered by the user is available to make a reservation.

        :param user_reservation: A reservation object.
        :type user_reservation: Reservation
        :return: True if the name entered by the user is available, False if is not.
        :rtype: bool
        """
        database_reservations = cls.get_list_of_reservations()
        tables_available = cls.restaurant_tables
        for database_reservation in database_reservations:
            if database_reservation["rdate"] == user_reservation.rdate.strftime("%Y-%m-%d"):
                if database_reservation["rtime"] == user_reservation.rtime.strftime("%H:%M"):
                    # TODO: no hardcode
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
            user_reservation.people / tables_available > cls.tables_capacity or
            user_reservation.people / tables_available < 0
        ) else True

    # Contraints
    @staticmethod
    def get_name_constraints() -> str:
        """
        Gets a message with the name constraints for the reservation.

        :return: A message with the name constraints.
        :rtype: str
        """
        return "Only one reservation per person is allowed."

    @staticmethod
    def get_time_constraints() -> str:
        """
        Gets a message with the time constraints for the reservation.

        :return: A message with the time constraints.
        :rtype: str
        """
        # TODO: No hardcode
        return "Time slots for reservations: 12:00h, 14:00h, 20:00h and 22:00h."

    @classmethod
    def get_people_constraints(cls) -> str:
        """
        Gets a message with the people constraints for the reservation.

        :return: A message with the people constraints.
        :rtype: str
        """
        return (
            f"Maximum capacity of the restaurant by time slots: {cls.restaurant_capacity}, "
            f"{cls.restaurant_tables} tables of {cls.tables_capacity} people each."
        )

    # Closing messages
    @staticmethod
    def get_confirmation_message() -> str:
        """
        Gets a message with the confirmation of the reservation.

        :return: A confirmation message.
        :rtype: str
        """
        return "Reservation confirmed! You will shortly receive a reminder document with the appointment details."

    @staticmethod
    def get_delete_message() -> str:
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
    def create_confirmation_document(reservation) -> None:
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
    def update_database(cls, user_reservation: Reservation) -> None:
        """
        Updates the database to include a new reservation.

        :param user_reservation: A reservation object.
        :type user_reservation: Reservation
        """
        # Extract a list of the database reservations
        database_reservations = cls.get_list_of_reservations()
        # Add the new reservation to the list
        database_reservations.append(dict(
            name = user_reservation.name,
            rdate = user_reservation.rdate.strftime("%Y-%m-%d"),
            rtime = user_reservation.rtime.strftime("%H:%M"),
            people = user_reservation.people
        ))
        # Sort the reservations list by date
        sorted_database_reservations = sorted(
            database_reservations,
            key = lambda item : item["rdate"]
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
        cls.create_confirmation_document(user_reservation)

    @staticmethod
    def get_list_of_reservations() -> list:
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
    Main function of the script whose puporse is to ask a user if he/she wants to
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
        case "a": print(Reservation.create_reservation())
        case "b": print(Reservation.read_reservation())
        case "c": print(Reservation.update_reservation())
        case "d": print(Reservation.delete_reservation())
        case "e": exit(Reservation.get_goodbye_message())
        case _: exit("The option entered is not correct")
    print(Reservation.get_goodbye_message())


if __name__ == "__main__":
    main()
