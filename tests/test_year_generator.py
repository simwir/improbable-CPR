import itertools
from datetime import date

import pytest
from improbable_cpr.generators import Gender
from improbable_cpr.generators import Options
from improbable_cpr.generators import YearGenerator


@pytest.mark.parametrize("year", [(1900), (2000)])
def test_single_year(year: int, seed_random):
    for cpr in itertools.islice(YearGenerator(Options(years=[year])), 100):
        assert cpr.year == year


def test_multiple_years(seed_random):
    year1 = False
    year2 = False
    for cpr in YearGenerator(Options(years=[2038, 1899])):
        if cpr.year == 2038:
            year1 = True
        elif cpr.year == 1899:
            year2 = True
        else:
            assert False, f"Year {cpr.year} does not equal 2038 or 1899"
        if year1 and year2:
            break

    assert year1
    assert year2


def test_all_months(seed_random):
    months = {i: False for i in range(1, 13)}
    for cpr in YearGenerator(
        Options(years=[2020], genders=[Gender.FEMALE], days=[25])
    ):
        assert cpr.year == 2020
        assert cpr.month in months
        months[cpr.month] = True
        if all(months.values()):
            break

    for key, value in months.items():
        assert value, f"Month {key} not seen"


def test_some_months():
    month1 = False
    month2 = False
    for cpr in YearGenerator(
        Options(years=[1966], genders=[Gender.MALE], days=[12], months=[5, 9])
    ):
        assert cpr.year == 1966
        if cpr.month == 5:
            month1 = True
        elif cpr.month == 9:
            month2 = True
        else:
            assert False, f"Month {cpr.month} does not equal 5 or 9"

        if month1 and month2:
            break

    assert month1
    assert month2


def test_no_years_before_min_year(seed_random):
    has_results = False
    for cpr in YearGenerator(
        Options(
            years=[1988, 1989], months=[12], days=[6], min_date=date(1989, 5, 5)
        )
    ):
        has_results = True
        assert cpr.year == 1989
    assert has_results


def test_no_years_after_max_year(seed_random):
    has_results = False
    for cpr in YearGenerator(
        Options(
            years=[1988, 1989], months=[3], days=[6], max_date=date(1988, 5, 5)
        )
    ):
        has_results = True
        assert cpr.year == 1988
    assert has_results


def test_years_only_between_min_and_max_year(seed_random):
    has_results = False
    for cpr in YearGenerator(
        Options(
            years=[2004, 2005, 2006],
            months=[8],
            days=[5],
            min_date=date(2005, 1, 1),
            max_date=date(2005, 12, 31),
        )
    ):
        has_results = True
        assert cpr.year == 2005
    assert has_results
