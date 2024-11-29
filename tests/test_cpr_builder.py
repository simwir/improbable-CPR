from datetime import date
import pytest

from improbable_cpr import cpr_builder

@pytest.fixture
def override_today_func(request):
    old_func = cpr_builder.today_func
    cpr_builder.today_func = lambda: request.param
    yield request.param
    cpr_builder.today_func = old_func

@pytest.mark.parametrize("override_today_func,max_date,min_date",
                         [
                             (date(2022, 6, 7), date(2012, 6 ,7), date(2011, 6, 8)),
                             (date(2010, 4, 1), date(2000, 4, 1), date(1999, 4, 2)),
                             (date(2011, 1, 31), date(2001, 1, 31), date(2000, 2, 1)),
                             (date(2011, 12, 31), date(2001, 12, 31), date(2001, 1, 1))
                         ],
                         indirect=["override_today_func"]
                         )
def test_age(override_today_func, min_date: date, max_date: date):
    builder = cpr_builder.CprBuilder()
    builder.with_age(10)
    assert builder.options.min_date == min_date
    assert builder.options.max_date == max_date