from datetime import date

import pytest
from improbable_cpr.generators import Gender
from improbable_cpr.generators import MonthGenerator
from improbable_cpr.generators import Options


@pytest.mark.parametrize(
    "month,num_days",
    [
        (1, 31),
        (2, 28),
        (3, 31),
        (4, 30),
        (5, 31),
        (6, 30),
        (7, 31),
        (8, 31),
        (9, 30),
        (10, 31),
        (11, 30),
        (12, 31),
    ],
)
def test_entire_single_month(month, num_days, seed_random):
    days: dict[int, bool] = {i: False for i in range(1, num_days + 1)}
    for cpr in MonthGenerator(
        1995, Options(months=[month], genders=[Gender.FEMALE])
    ):
        assert cpr.month == month
        assert cpr.day in days
        days[cpr.day] = True
        if all(days.values()):
            break

    for key, value in days.items():
        assert value, f"Day {key} not seen"


def test_date_interval(seed_random):
    days: dict[int, bool] = {i: False for i in range(20, 31)}
    for cpr in MonthGenerator(
        1998,
        Options(months=[6], genders=[Gender.MALE], days=list(range(20, 32))),
    ):
        assert cpr.month == 6
        assert cpr.day in days
        days[cpr.day] = True

    for key, value in days.items():
        assert value, f"Day {key} not seen"


def test_multiple_months(seed_random):
    month1 = False
    month2 = False
    for cpr in MonthGenerator(
        2006, Options(months=[4, 9], genders=[Gender.FEMALE])
    ):
        if cpr.month == 4:
            month1 = True
        elif cpr.month == 9:
            month2 = True
        else:
            assert False, f"Month {cpr.month} does not equal 4 or 9"
        if month1 and month2:
            break

    assert month1
    assert month2


def test_no_days_before_min_date(seed_random):
    has_results = False
    for cpr in MonthGenerator(
        2007, Options(months=[3], days=[1, 2], min_date=date(2007, 3, 2))
    ):
        has_results = True
        assert cpr.day == 2
    assert has_results


def test_min_days_only_affect_correct_month(seed_random):
    has_results = False
    for cpr in MonthGenerator(
        2002, Options(months=[4, 5], days=[10], min_date=date(2002, 4, 20))
    ):
        has_results = True
        assert cpr.month == 5
    assert has_results


def test_min_date_choise_filter(seed_random):
    with pytest.raises(StopIteration):
        cpr = next(
            iter(
                MonthGenerator(
                    2002,
                    Options(
                        months=[4, 5], days=[10], min_date=date(2002, 5, 20)
                    ),
                )
            )
        )
        print(repr(cpr))


def test_min_days_only_affect_correct_year(seed_random):
    next(
        iter(
            MonthGenerator(
                1995, Options(months=[7], days=[5], min_date=date(1994, 7, 10))
            )
        )
    )


def test_no_days_after_max_date(seed_random):
    has_results = False
    for cpr in MonthGenerator(
        2007, Options(months=[3], days=[1, 2], max_date=date(2007, 3, 1))
    ):
        has_results = True
        assert cpr.day == 1
    assert has_results


def test_max_days_only_affect_correct_month(seed_random):
    has_results = False
    for cpr in MonthGenerator(
        2002, Options(months=[4, 5], days=[10], max_date=date(2002, 5, 5))
    ):
        has_results = True
        assert cpr.month == 4
    assert has_results


def test_max_date_choise_filter(seed_random):
    with pytest.raises(StopIteration):
        cpr = next(
            iter(
                MonthGenerator(
                    2002,
                    Options(
                        months=[4, 5], days=[10], max_date=date(2002, 4, 5)
                    ),
                )
            )
        )
        print(repr(cpr))


def test_max_day_only_affect_coorect_year(seed_random):
    next(
        iter(
            MonthGenerator(
                1995, Options(months=[7], days=[5], max_date=date(1994, 7, 10))
            )
        )
    )


def test_min_and_max_date(seed_random):
    min_date = date(1955, 10, 15)
    max_date = date(1955, 12, 15)
    seen_month_1 = False
    seen_month_2 = False
    seen_month_3 = False
    for cpr in MonthGenerator(
        1955,
        options=Options(
            months=[10, 11, 12],
            days=[10, 20],
            min_date=min_date,
            max_date=max_date,
        ),
    ):
        assert cpr.month is not None
        assert cpr.day is not None
        cpr_date = date(1955, cpr.month, cpr.day)
        assert cpr_date >= min_date
        assert cpr_date <= max_date
        match cpr.month:
            case 10:
                seen_month_1 = True
            case 11:
                seen_month_2 = True
            case 12:
                seen_month_3 = True
    assert seen_month_1
    assert seen_month_2
    assert seen_month_3
