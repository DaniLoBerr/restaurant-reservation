# Getting Started
"""
- What will your software do? What features will it have? How will it be executed?
    - Aplicación de terminal
    - Mensaje de bienvenida
    - Preguntar por fecha de la reserva y personas (incluir el formato, incluir posibilidad de cancelación)
        - Si está escrito en otro formato, repreguntar
        - Si está completo ese día y/o ese hora, repreguntar
    - Mensaje de:
        - Cancelación si decide cancelar.
        - Reserva completada si se ha completado.
            - Guardar en un archivo json los datos de todas las reservas
            - Exportar un pdf con la confirmación, la fecha y la hora de la reserva.
- What new skills will you need to acquire? What topics will you need to research?
    - Librería date
    - Clases
    - try-catch
    - i/o
    - pytest
"""
class Reservation:
    """
    A class representing a reservation.

    Attributtes:
        name (str): The name of the person making the reservation.
        date (...): The date of the reservation.
        time (...): The time of the reservation.
        people (int): The number of people who will attend
    """

    def __init__(self, name, date, time, people):
        """
        Initializes a Reservation object.

        Parameters:
            name (str): The name of the person making the reservation.
            date (...): The date of the reservation.
            time (...): The time of the reservation.
            people (int): The number of people who will attend
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