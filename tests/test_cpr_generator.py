from improbable_cpr.generators import CprGenerator
from improbable_cpr.cpr import Cpr
import pytest

@pytest.mark.parametrize(
        "cpr,valid",
        [("2110625629", True), ("0707614285", True), ("2110625624", False), ("0707614288", False)]
)
def test_cpr_control_digit_validation(cpr: str, valid: bool):
    assert CprGenerator.validateControlDigit(Cpr.from_str(cpr)) == valid