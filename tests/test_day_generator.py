from improbable_cpr.generators import DayGenerator, Gender

def test_single_day(seed_random):
    for cpr in DayGenerator([5], 2000, [Gender.MALE]):
        assert cpr.day == 5

def test_multiple_days(seed_random):
    day1 = False
    day2 = False
    for cpr in DayGenerator([10,15], 1990, [Gender.FEMALE]):
        if cpr.day == 10:
            day1 = True
        elif cpr.day == 15:
            day2 = True
        else:
            assert False, f"CPR.day {cpr.day} is not 10 or 15"