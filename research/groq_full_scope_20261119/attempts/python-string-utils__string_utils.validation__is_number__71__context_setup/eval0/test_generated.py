import pytest
from string_utils.validation import is_number
from string_utils.errors import InvalidInputError


def test_is_number_valid_cases():
    """Valid numeric strings should return True."""
    valid_inputs = [
        "42",
        "0",
        "-7",
        "+3",
        "19.99",
        "-9.12",
        "+0.001",
        "1e3",
        "-2E-5",
        "+4.5e+2",
    ]
    for s in valid_inputs:
        assert is_number(s) is True, f"Expected True for {s!r}"


def test_is_number_invalid_cases():
    """Non‑numeric strings should return False."""
    invalid_inputs = [
        "",
        "   ",
        "1 2 3",
        "abc",
        "12a",
        "1e",
        "e5",
        "+-3",
        "++5",
        "--2",
        "5.6.7",
        "1e5.5",
    ]
    for s in invalid_inputs:
        assert is_number(s) is False, f"Expected False for {s!r}"


def test_is_number_invalid_type_raises():
    """Passing a non‑string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_number(123)          # int
    with pytest.raises(InvalidInputError):
        is_number(None)         # NoneType
    with pytest.raises(InvalidInputError):
        is_number(["1", "2"])   # list
