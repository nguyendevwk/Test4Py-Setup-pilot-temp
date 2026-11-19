import pytest
from dataclasses_json.undefined import Undefined
from dataclasses_json.utils import CatchAllVar
from dataclasses_json.exceptions import UndefinedParameterError

def test_undefined_enum_members():
    # The enum should expose exactly the three expected members
    assert set(Undefined.__members__.keys()) == {"INCLUDE", "RAISE", "EXCLUDE"}
    # Each member should be an instance of Undefined
    for member in Undefined:
        assert isinstance(member, Undefined)
    # The value of each member should be a class (the handler)
    assert isinstance(Undefined.INCLUDE.value, type)
    assert isinstance(Undefined.RAISE.value, type)
    assert isinstance(Undefined.EXCLUDE.value, type)

def test_include_behavior_accepts_undefined():
    # When INCLUDE is used, undefined parameters should be stored as CatchAllVar
    handler_cls = Undefined.INCLUDE.value
    handler = handler_cls()
    # Simulate passing an undefined key
    result = handler.handle("foo", "bar")
    # The result should be a CatchAllVar instance containing the value
    assert isinstance(result, CatchAllVar)
    assert result.value == "bar"

def test_raise_behavior_raises_error():
    # When RAISE is used, an undefined parameter should raise UndefinedParameterError
    handler_cls = Undefined.RAISE.value
    handler = handler_cls()
    with pytest.raises(UndefinedParameterError) as excinfo:
        handler.handle("foo", "bar")
    # The exception message should mention the undefined key
    assert "foo" in str(excinfo.value)
