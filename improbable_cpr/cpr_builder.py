from typing import Self
from improbable_cpr.cpr import Cpr
from improbable_cpr.generators import Gender

class CprBuilder:

    def with_years(self, years: list[int]) -> Self:
        self.years = years
        return self

    def with_year_range(self, start_year: int, end_year) -> Self:
        return self.with_years(list(range(start_year, end_year + 1)))

    def with_year(self, year: int) -> Self:
        return self.with_years([year])

    def with_genders(self, genders: list[Gender]) -> Self:
        self.genders = genders
        return self

    def with_days(self, days: list[int]) -> Self:
        self.days = days
        return self

    def with_day_range(self, start_day: int, end_day: int) -> Self:
        return self.with_days(list(range(start_day, end_day + 1)))

    def with_day(self, day: int) -> Self:
        return self.with_days([day])

    def with_months(self, months: list[int]) -> Self:
        self.months = months
        return self

    def with_month_range(self, start_month: int, end_month: int) -> Self:
        return self.with_months(list(range(start_month, end_month + 1)))

    def with_month(self, month: int) -> Self:
        return self.with_months([month])

    def build_list(self) -> list[Cpr]:
        return []