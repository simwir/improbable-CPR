import pytest
from improbable_cpr.generators import Gender
from improbable_cpr.generators import RunningNumberGenerator


def test_female(seed_random):
    for cpr in RunningNumberGenerator(2000, Gender.FEMALE):
        running_number = cpr.running_number
        assert running_number is not None
        assert running_number % 2 == 0


def test_male(seed_random):
    for cpr in RunningNumberGenerator(1950, Gender.MALE):
        running_number = cpr.running_number
        assert running_number is not None
        assert running_number % 2 != 0


def get_7_digit(num: int) -> int:
    if num < 1000:
        return 0
    else:
        return num // 1000


@pytest.mark.parametrize(
    "year,valid_digits",
    [
        (1858, [5, 6, 7, 8]),
        (1899, [5, 6, 7, 8]),
        (1900, [0, 1, 2, 3]),
        (1937, [0, 1, 2, 3, 4, 9]),
        (1999, [0, 1, 2, 3, 4, 9]),
        (2000, [4, 5, 6, 7, 8, 9]),
        (2036, [4, 5, 6, 7, 8, 9]),
        (2037, [5, 6, 7, 8]),
        (2057, [5, 6, 7, 8]),
    ],
)
def test_7_digit(year: int, valid_digits: list[int], seed_random):
    for cpr in RunningNumberGenerator(year, Gender.FEMALE):
        running_number = cpr.running_number
        assert running_number is not None
        assert get_7_digit(running_number) in valid_digits


@pytest.mark.parametrize("year", [(1857), (2058)])
def test_out_of_bounds(year: int, seed_random):
    assert len(list(RunningNumberGenerator(year, Gender.MALE))) == 0
