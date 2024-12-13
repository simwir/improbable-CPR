from improbable_cpr.cpr import Cpr


def test_cpr_constructor():
    cpr = Cpr.from_str("1005746804")
    assert cpr.day == 10
    assert cpr.month == 5
    assert cpr.year == 1874
    assert cpr.running_number == 6804
