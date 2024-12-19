# Standard library imports
from datetime import date

# Third-party imports
import pytest

# Local imports
from reservation import validate_name
from reservation import validate_date
from reservation import validate_time
from reservation import validate_people


def main():
    test_validate_name()
    test_validate_date()
    test_validate_time()
    test_validate_people()


def test_validate_name():
    assert validate_name("Dani Berrocal")
    assert validate_name("Joe Gómez")
    assert validate_name("martiño rodríguez")
    with pytest.raises(ValueError):
        validate_name("a")
    with pytest.raises(ValueError):
        validate_name("Electroencefalografista Esternocleidomastoideo")
    with pytest.raises(ValueError):
        validate_name("Homer J. Simpson")
    with pytest.raises(ValueError):
        validate_name("- -")


def test_validate_date():
    assert validate_date("17-12-2025")
    assert validate_date("04-08-2027")
    with pytest.raises(ValueError):
        validate_date("17-12-2023")
    with pytest.raises(ValueError):
        validate_date("35-12-2026")
    with pytest.raises(AttributeError):
        validate_date("17.12.2023")
    with pytest.raises(AttributeError):
        validate_date("hello, world")


def test_validate_time():
    assert validate_time(date(2025, 12, 23), "12:00")
    assert validate_time(date(2025, 12, 23), "14:00")
    assert validate_time(date(2025, 12, 23), "20:00")
    assert validate_time(date(2025, 12, 23), "22:00")
    with pytest.raises(ValueError):
        validate_time(date(2023, 12, 23), "12:00")
    with pytest.raises(AttributeError):
        validate_time(date(2025, 12, 23), "14:30")
    with pytest.raises(AttributeError):
        validate_time(date(2025, 12, 23), "22h")
    with pytest.raises(AttributeError):
        validate_time(date(2025, 12, 23), "11 PM")
    with pytest.raises(AttributeError):
        validate_time(date(2025, 12, 23), "20-00")


def test_validate_people():
    assert validate_people("1")
    assert validate_people("9")
    assert validate_people("16")
    with pytest.raises(AttributeError):
        validate_people("20")
    with pytest.raises(AttributeError):
        validate_people("-2")
    with pytest.raises(AttributeError):
        validate_people("seventeen")



if __name__ == "__main__":
    main()