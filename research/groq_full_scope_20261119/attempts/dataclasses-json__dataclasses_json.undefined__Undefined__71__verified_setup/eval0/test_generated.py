import pytest
from dataclasses_json.undefined import Undefined

def test_undefined_enum_members():
    """The Undefined enum should contain exactly the three expected members."""
    expected_names = {"INCLUDE", "RAISE", "EXCLUDE"}
    actual_names = set(Undefined.__members__.keys())
    assert actual_names == expected_names, f"Expected members {expected_names}, got {actual_names}"

def test_undefined_enum_values_are_unique_and_not_none():
    """Each member should have a unique, non-None value."""
    values = [member.value for member in Undefined]
    assert len(values) == len(set(values)), "Enum member values are not unique"
    assert all(v is not None for v in values), "Enum member value is None"

def test_undefined_enum_member_access_and_str():
    """Accessing members by name should return the correct enum member and its string representation."""
    include = Undefined.INCLUDE
    raise_ = Undefined.RAISE
    exclude = Undefined.EXCLUDE

    assert isinstance(include, Undefined)
    assert isinstance(raise_, Undefined)
    assert isinstance(exclude, Undefined)

    assert include.name == "INCLUDE"
    assert raise_.name == "RAISE"
    assert exclude.name == "EXCLUDE"

    assert str(include) == "Undefined.INCLUDE"
    assert str(raise_) == "Undefined.RAISE"
    assert str(exclude) == "Undefined.EXCLUDE"
