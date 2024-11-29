from datetime import date
from typing import Iterator, Self
from improbable_cpr.cpr import Cpr
from improbable_cpr.generators import CprGenerator, Gender, Options


today_func = date.today

class CprBuilder:
    def __init__(self):
        self.options = Options()
        self.iterator: Iterator[Cpr] | None = None

    def with_years(self, years: list[int]) -> Self:
        self.options.years = years
        return self

    def with_year_range(self, start_year: int, end_year) -> Self:
        return self.with_years(list(range(start_year, end_year + 1)))

    def with_year(self, year: int) -> Self:
        return self.with_years([year])

    def with_genders(self, genders: list[Gender]) -> Self:
        self.options.genders = genders
        return self

    def with_days(self, days: list[int]) -> Self:
        self.options.days = days
        return self

    def with_day_range(self, start_day: int, end_day: int) -> Self:
        return self.with_days(list(range(start_day, end_day + 1)))

    def with_day(self, day: int) -> Self:
        return self.with_days([day])

    def with_months(self, months: list[int]) -> Self:
        self.options.months = months
        return self

    def with_month_range(self, start_month: int, end_month: int) -> Self:
        return self.with_months(list(range(start_month, end_month + 1)))

    def with_month(self, month: int) -> Self:
        return self.with_months([month])

    def with_min_date(self, min_date: date) -> Self:
        self.options.min_date = min_date
        return self

    def with_max_date(self, max_date: date) -> Self:
        self.options.max_date = max_date
        return self

    def with_age(self, age: int) -> Self:
        today = today_func()
        birth_year = today.year - age
        self.options.max_date = date(birth_year, today.month, today.day)
        try:
            self.options.min_date = date(birth_year - 1, today.month, today.day + 1)
        except ValueError as e:
            if e.args[0] == 'day is out of range for month':
                try:
                    self.options.min_date = date(birth_year - 1, today.month + 1, 1)
                except ValueError as e:
                    if e.args[0] == 'month must be in 1..12':
                        self.options.min_date = date(birth_year, 1, 1)
                    else:
                        raise e
            else:
                raise e
        return self


    def __iter__(self) -> Iterator[Cpr]:
        return iter(CprGenerator(self.options))

    def __next__(self) -> Cpr:
        if self.iterator is None:
            self.iterator = iter(self)
        return next(self.iterator)