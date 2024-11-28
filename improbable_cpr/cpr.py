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
        cpr.year = int(cpr_str[4:6])
        cpr.running_number = int(cpr_str[6:10])
        return cpr


    def get_year(self) -> int | None:
        if self.year is None:
            return None
        return self.year % 100

    def get_date(self) -> str:
        return f"{self.day:02d}{self.month:02d}{self.get_year():02d}"

    def get_running_number(self) -> str:
        return f"{self.running_number:04d}"
    
    def get_no_dash(self) -> str:
        return self.get_date() + self.get_running_number()

    def get_dash(self) -> str:
        return self.get_date() + "-" + self.get_running_number()

    def __str__(self) -> str:
        return self.get_dash()

    def __repr__(self) -> str:
        return f"Cpr({self.year}, {self.month}, {self.day}, {self.running_number})"