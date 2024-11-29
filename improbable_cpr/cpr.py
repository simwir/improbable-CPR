from typing import Self

class Cpr():

    def __init__(self) -> None:
        self.running_number: int | None = None
        self.year: int | None = None
        self.month: int | None = None
        self.day: int | None = None

    @classmethod
    def from_str(cls, cpr_str: str) -> Self:
        cpr = cls()
        cpr.day = int(cpr_str[0:2])
        cpr.month = int(cpr_str[2:4])
        cpr.year = cls.calculate_year(int(cpr_str[7]), int(cpr_str[4:6]))
        cpr.running_number = int(cpr_str[6:10])
        return cpr

    @classmethod
    def calculate_year(cls, digit_7: int, two_digit_year: int) -> int:
        if digit_7 >= 0 and digit_7 <= 3:
            return 1900 + two_digit_year
        elif digit_7 == 4 or digit_7 == 9:
            if (two_digit_year >= 37 and two_digit_year <= 99):
                return 1900 + two_digit_year
            else:
                return 2000 + two_digit_year
        elif digit_7 >= 5 and digit_7 <= 8:
            if two_digit_year >= 0 and two_digit_year <= 57:
                return 2000 + two_digit_year
            else:
                return 1800 + two_digit_year
        else:
            raise CprException(f"The digit {digit_7} is not between 0 and 9")

    def get_last_two_digits_of_year(self) -> int | None:
        if self.year is None:
            return None
        return self.year % 100

    def get_date(self) -> str:
        return f"{self.day:02d}{self.month:02d}{self.get_last_two_digits_of_year():02d}"

    def get_running_number(self) -> str:
        return f"{self.running_number:04d}"
    
    def get_no_dash(self) -> str:
        return self.get_date() + self.get_running_number()

    def get_dash(self) -> str:
        return self.get_date() + "-" + self.get_running_number()

    def __str__(self) -> str:
        return self.get_dash()

    def __repr__(self) -> str:
        return f"Cpr({self.day}, {self.month}, {self.year}, {self.running_number})"
    
class CprException(Exception):
    pass