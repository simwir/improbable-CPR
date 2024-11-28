import calendar
from dataclasses import dataclass
from enum import Enum, auto
import abc
from operator import mul
import random
from typing import Any, Generator

from improbable_cpr.cpr import Cpr

class Gender(Enum):
    FEMALE=auto()
    MALE=auto()

@dataclass
class Options:
    years: list[int] | None = None
    months: list[int] | None = None
    days: list[int] | None = None
    genders: list[Gender] | None = None


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
    def __init__(self, days: list[int], year: int, genders: list[Gender]) -> None:
        super().__init__(days)
        self.year = year
        self.genders = genders

    def getGenerator(self, choise: Any) -> Generator[Cpr, Any, None]:
        return iter(GenderGenerator(self.year, self.genders))
    
    def enrich(self, cpr: Cpr, choise: int) -> Cpr:
        cpr.day = choise
        return cpr

class MonthGenerator(AbstractGenerator):
    def __init__(self, months: list[int], year: int, genders: list[Gender], days: list[int] | None) -> None:
        super().__init__(months)
        self.year = year
        self.genders = genders
        self.days = days

    def enrich(self, cpr: Cpr, choise: int) -> Cpr:
        cpr.month = choise
        return cpr

    def getGenerator(self, choise: int) -> Generator[Cpr, Any, None]:
        num_days = calendar.monthrange(self.year, choise)[1]
        days = list(range(1, num_days + 1))
        if self.days is not None:
            days = list(set(days) & set(self.days))

        return iter(DayGenerator(days, self.year, self.genders))

class YearGenerator(AbstractGenerator):
    def __init__(self, years: list[int] | None = None, genders: list[Gender] | None = None, days: list[int] | None = None, months: list[int] | None = None) -> None:
        if years is None:
            years = list(range(1858, 2058))
        super().__init__(years)
        if genders is None:
            genders = [Gender.FEMALE, Gender.MALE]
        self.genders = genders
        self.days = days
        if months is None:
            months = list(range(1,13))
        self.months = months

    def enrich(self, cpr: Cpr, choise: int) -> Cpr:
        cpr.year = choise
        return cpr

    def getGenerator(self, choise: int) -> Generator[Cpr, Any, None]:
        return iter(MonthGenerator(self.months, choise, self.genders, self.days))

class CprGenerator:
    MULTIPLICATION_TABLE = [4, 3, 2, 7, 6, 5, 4, 3, 2, 1]

    def __init__(self, years: list[int] | None = None, genders: list[Gender] | None = None, days: list[int] | None = None, months: list[int] | None = None) -> None:
        self.years = years
        self.genders = genders
        self.days = days
        self.months = months

    @classmethod
    def validateControlDigit(cls, cpr: Cpr) -> bool:
        return sum(map( mul, map(int, list(cpr.get_no_dash())), cls.MULTIPLICATION_TABLE)) % 11 == 0

    @classmethod
    def invalidControlDigit(cls, cpr: Cpr) -> bool:
        return not cls.validateControlDigit(cpr)

    def __iter__(self):
        return filter(self.invalidControlDigit, YearGenerator(self.years, self.genders, self.days, self.months))

class GenerationException(Exception):
    pass
