from improbable_cpr.generators import Gender
from improbable_cpr.generators import GenderGenerator


def test_female(seed_random):
    for cpr in GenderGenerator(1950, [Gender.FEMALE]):
        running_number = cpr.running_number
        assert running_number is not None
        assert running_number % 2 == 0


def test_male(seed_random):
    for cpr in GenderGenerator(1890, [Gender.MALE]):
        running_number = cpr.running_number
        assert running_number is not None
        assert running_number % 2 != 0


def test_both_gender(seed_random):
    female = False
    male = False
    for cpr in GenderGenerator(2035, [Gender.FEMALE, Gender.MALE]):
        assert cpr.running_number is not None
        if cpr.running_number % 2 == 0:
            female = True
        else:
            male = True
        if female and male:
            break
    assert female
    assert male
