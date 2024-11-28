from improbable_cpr.generators import MonthGenerator, Gender, Options
import pytest

@pytest.mark.parametrize(
        "month,num_days",
        [(1,31),(2,28),(3,31),(4,30),(5,31),(6,30),(7,31),(8,31),(9,30),(10,31),(11,30),(12,31)]
)
def test_entire_single_month(month, num_days, seed_random):
    days: dict[int, bool] = {i: False for i in range(1, num_days + 1)}
    for cpr in MonthGenerator(1995, Options(months=[month], genders=[Gender.FEMALE])):
        assert cpr.month == month
        assert cpr.day in days
        days[cpr.day] = True
        if all(days.values()):
            break

    for key, value in days.items():
        assert value, f"Day {key} not seen"

def test_date_interval(seed_random):
    days: dict[int, bool] = {i: False for i in range(20, 31)}
    for cpr in MonthGenerator(1998, Options(months=[6], genders=[Gender.MALE], days=list(range(20, 32)))):
        assert cpr.month == 6
        assert cpr.day in days
        days[cpr.day] = True

    for key, value in days.items():
        assert value, f"Day {key} not seen"

def test_multiple_months(seed_random):
    month1 = False
    month2 = False
    for cpr in MonthGenerator(2006, Options(months=[4,9], genders=[Gender.FEMALE])):
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