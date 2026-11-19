import pytest
from dataclasses_json.undefined import Undefined

def test_enum_members_exist_and_unique():
    # The enum should contain exactly the three expected members
    expected_names = {"INCLUDE", "RAISE", "EXCLUDE"}
    assert set(Undefined.__members__.keys()) == expected_names
    # Each member should be a distinct instance of Undefined
    members = list(Undefined)
    assert len(members) == 3
    assert len(set(members)) == 3

def test_enum_value_is_callable_and_unique():
    # The value of each enum member should be a callable (class) that can be instantiated
    for member in Undefined:
        value = member.value
        # The value should be a type (class)
        assert isinstance(value, type)
        # Instantiating the value should not raise an exception
        instance = value()
        # The instance should be of the same type as the value
        assert isinstance(instance, value)

def test_enum_comparison_and_hashing():
    # Members should compare equal to themselves and not to others
    include = Undefined.INCLUDE
    raise_ = Undefined.RAISE
    exclude = Undefined.EXCLUDE
    assert include == Undefined.INCLUDE
    assert raise_ == Undefined.RAISE
    assert exclude == Undefined.EXCLUDE
    assert include != raise_
    assert include != exclude
    # Hashing should be consistent with equality
    assert hash(include) == hash(Undefined.INCLUDE)
    assert hash(raise_) == hash(Undefined.RAISE)
    assert hash(exclude) == hash(Undefined.EXCLUDE)
