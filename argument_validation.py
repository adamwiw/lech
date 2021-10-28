from argparse import ArgumentTypeError
from datetime import datetime


class ArgumentValidation:
    def __init__(self, number: str):
        self.__number = number

    def __int(self) -> int:
        try:
            return int(self.__number)
        except ValueError:
            raise ArgumentTypeError('Not a number')

    def range(self, minimum: int, maximum: int) -> str:
        number = self.__int()
        if number < minimum or number > maximum:
            raise ArgumentTypeError('Out of range')
        return str(number)


def validate_day(day: str) -> str:
    argument_validation = ArgumentValidation(day)
    return argument_validation.range(1, 31)


def validate_month(month: str) -> str:
    argument_validation = ArgumentValidation(month)
    return argument_validation.range(1, 12)


def validate_year(year: str) -> str:
    argument_validation = ArgumentValidation(year)
    return argument_validation.range(1900, datetime.now().year)
