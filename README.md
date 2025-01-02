# Restaurant Reservation System
### Video Demo:
[Link](https://youtu.be/NsWipdTj9Rk?si=9m_ACRs8TV-6SDgp)
### Description:
A command line restaurant reservation application to practice the basics
of Python and object-oriented programming.
It allows a user to make, modify, show or cancel a reservation at a
restaurant, and each reservation includes a name, date, time and number
of people attending.
This is the final project of the CS50P course taught by Harvard
University.
### Project structure
This project consists of 5 files:
- reservation.py: In this file is included the code related to the
program. It is composed of:
    - A class called Reservation that includes everything related to
    a reservation.
    - A main function that runs the program when executed the file.
    - 4 validation methods that validate the name, date, time and
    people attending a reservation in a specific format.
- test_reservation.py: In this file are included the unit tests written
for the validation methods of the "reservation.py" file.
- reservation_database.json: This file works as a database to store
reservations.
- requirements.txt: This file includes the third-party libraries used
in the program.
- README.md: This file explains the composition and operation of the
project.
### Program Operation
When you run the file reservation.py with Python from the command-line,
the program displays an introductory message and asks you to choose
between 4 options:
- The first one is to make a reservation. First, the program asks you
for a name for the reservation, in a "first-name last-name" format.
Then it asks you for the date on which the reservation will be made, in
a "dd-mm-yyyy" format. After this, the program will ask you for the
time at which the reservation will be made, giving you a choice between
the 4 times available for this hypethetical restaurant to eat. Finally,
the program will ask you for the number of people that will go to the
restaurant, informing you about the restaurant's capacity and the
maximum number of people that can be accommodated in each time slot.

    Each time the program propmts you for information, if the data
    entered is not correct, i.e. the name is not in the correct format
    the date and/or time are not in the correct format or are out of
    date, or if the number of people entered does not match the
    restaurant's capacity or availability, the program will ask again
    until the information is entered correctly.

    If all data is correct, the program will save the reservation in
    the database and export a pdf with the reservation details.
- The second one is to show the details of a reservation. The program
asks you for a name and, if a reservation exists with that name, it
shows you the reservation details.
- The third one is to update a reservation. The program asks you for a
name and, if a reservation exists with that name, it removes it from
the database and prompts you to make a new reservation.
- The fourth one is to cancel a reservation. The program asks you for a
name and, if a reservation exists with that name, it
removes it from the database.
#### Requirements
This program uses two pip-installable third-party libraries:
- Pytest: This library is used to run the program tests of the file
"test_reservation.py".
- fpdf: This library is used to export a pdf with a reservation details
when a reservation is made or updated.