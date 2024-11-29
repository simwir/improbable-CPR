import calendar
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
import abc
from operator import mul
import random
from typing import Any, Generator, Iterator

from improbable_cpr.cpr import Cpr

class Gender(Enum):
    FEMALE=auto()
    MALE=auto()

@dataclass
class Options:
    years: list[int] = field(default_factory=lambda:  list(range(1858, 2058)))
    months: list[int] = field(default_factory=lambda: list(range(1,13)))
    days: list[int] | None = None
    genders: list[Gender] = field(default_factory= lambda: [Gender.FEMALE, Gender.MALE])
    min_date: date | None = None
    max_date: date | None = None


class RunningNumberGenerator:
    def __init__(self, year: int, gender: Gender) -> None:
        self.year = year
        self.gender = gender

    def _validate_7_digit(self, running_number: int) -> bool:
        if running_number >= 1000:
            digit_7 = running_number // 1000
        else:
            digit_7 = 0

        if digit_7 >= 0 and digit_7 <= 3:
            return self.year >= 1900 and self.year <= 1999
        elif digit_7 == 4 or digit_7 == 9:
            return (self.year >= 1937 and self.year <= 1999) or (self.year >= 2000 and self.year <= 2036)
        elif digit_7 >= 5 and digit_7 <= 8:
            return (self.year >= 2000 and self.year <= 2057) or (self.year >= 1858 and self.year <= 1899)
        else:
            raise GenerationException(f"The digit {digit_7} is not between 0 and 9")
        
    def _validate_gender(self, number: int) -> bool:
        if self.gender == Gender.FEMALE:
            return number % 2 == 0
        else:
            return not number % 2 == 0

    def __iter__(self):
        runningNumbers = [i for i in range(10000) if self._validate_gender(i) and self._validate_7_digit(i)]
        random.shuffle(runningNumbers)
        for number in runningNumbers:
            cpr = Cpr()
            cpr.running_number = number
            yield cpr
 
class AbstractGenerator(abc.ABC):
    def __init__(self, choises: list[Any]) -> None:
        self.choises = choises

    @abc.abstractmethod
    def getGenerator(self, choise: Any) -> Generator[Cpr, Any, None]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def enrich(self, cpr: Cpr, choise: Any) -> Cpr:
        raise NotImplementedError

    def __iter__(self):
        generators: dict[Gender, Generator[Cpr, Any, None]] = {}
        choises = self.choises[:]

        while len(choises) > 0:
            choise = random.choice(choises)
            if not choise in generators:
                generators[choise] = self.getGenerator(choise)

            generator = generators[choise]
            try:
                yield self.enrich(next(generator), choise)
            except StopIteration:
                choises.remove(choise)


class GenderGenerator(AbstractGenerator):
    def __init__(self, year: int, genders: list[Gender]) -> None:
        super().__init__(genders)
        self.year = year

    def getGenerator(self, gender: Gender) -> Generator[Cpr, Any, None]:
        return iter(RunningNumberGenerator(self.year, gender))

    def enrich(self, cpr: Cpr, choise: Any) -> Cpr:
        return cpr

class DayGenerator(AbstractGenerator):
    def __init__(self, days: list[int], year: int, options: Options) -> None:
        super().__init__(days)
        self.year = year
        self.options = options

    def getGenerator(self, choise: Any) -> Generator[Cpr, Any, None]:
        return iter(GenderGenerator(self.year, self.options.genders))
    
    def enrich(self, cpr: Cpr, choise: int) -> Cpr:
        cpr.day = choise
        return cpr

class MonthGenerator(AbstractGenerator):
    def __init__(self, year: int, options: Options) -> None:
        super().__init__(self.get_months(year, options))
        self.year = year
        self.options = options

    def enrich(self, cpr: Cpr, choise: int) -> Cpr:
        cpr.month = choise
        return cpr

    def is_limit_month(self, month: int, limit: date) -> bool:
        return self.year == limit.year and month == limit.month

    def get_months(self, year, options: Options) -> list[int]:
        min_filter = lambda x: True
        max_filter = lambda x: True
        if options.min_date is not None and options.min_date.year == year:
            min_filter = lambda month: month >= options.min_date.month # type: ignore
        if options.max_date is not None and options.max_date.year == year:
            max_filter = lambda month: month <= options.max_date.month # type: ignore

        return [month for month in options.months if min_filter(month) and max_filter(month)]

    def get_days(self, month: int) -> list[int]:
        min_day = self.options.min_date.day if self.options.min_date is not None and self.is_limit_month(month, self.options.min_date) else 1
        max_day = self.options.max_date.day if self.options.max_date is not None and self.is_limit_month(month, self.options.max_date) else calendar.monthrange(self.year, month)[1]
        return list(range(min_day, max_day + 1))

    def getGenerator(self, choise: int) -> Generator[Cpr, Any, None]:
        days = self.get_days(choise)
        if self.options.days is not None:
            days = list(set(days) & set(self.options.days))

        return iter(DayGenerator(days, self.year, self.options))

class YearGenerator(AbstractGenerator):
    def __init__(self, options: Options) -> None:
        self.options = options
        super().__init__(self.get_years(options))

    def get_years(self, options: Options) -> list[int]:
        min_filter = lambda x: True
        max_filter = lambda x: True
        if options.min_date is not None:
            min_filter = lambda year: year >= options.min_date.year # type: ignore
        if options.max_date is not None:
            max_filter = lambda year: year <= options.max_date.year # type: ignore

        return [year for year in options.years if min_filter(year) and max_filter(year)]

    def enrich(self, cpr: Cpr, choise: int) -> Cpr:
        cpr.year = choise
        return cpr

    def getGenerator(self, choise: int) -> Generator[Cpr, Any, None]:
        return iter(MonthGenerator(choise, self.options))

class CprGenerator:
    MULTIPLICATION_TABLE = [4, 3, 2, 7, 6, 5, 4, 3, 2, 1]

    def __init__(self, options: Options) -> None:
        self.options = options

    @classmethod
    def validateControlDigit(cls, cpr: Cpr) -> bool:
        return sum(map( mul, map(int, list(cpr.get_no_dash())), cls.MULTIPLICATION_TABLE)) % 11 == 0

    @classmethod
    def invalidControlDigit(cls, cpr: Cpr) -> bool:
        return not cls.validateControlDigit(cpr)

    def __iter__(self) -> Iterator[Cpr]:
        return filter(self.invalidControlDigit, YearGenerator(self.options))

class GenerationException(Exception):
    pass
