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

def test_include_behavior_with_extra_field(tmp_path):
    # Define a simple dataclass that accepts an extra field via INCLUDE
    from dataclasses import dataclass
    from dataclasses_json import dataclass_json

    @dataclass_json(undefined=Undefined.INCLUDE)
    @dataclass
    class Sample:
        a: int

    # When deserializing JSON with an unknown key, it should be stored in _extra
    data = {"a": 1, "b": 2}
    obj = Sample.from_dict(data)
    # The known field is set correctly
    assert obj.a == 1
    # The unknown field is captured in _extra
    assert hasattr(obj, "_extra")
    assert obj._extra == {"b": 2}

def test_raise_behavior_with_missing_field():
    # Define a dataclass that requires a field
    from dataclasses import dataclass
    from dataclasses_json import dataclass_json

    @dataclass_json(undefined=Undefined.RAISE)
    @dataclass
    class Sample:
        a: int

    # Deserializing JSON missing the required field should raise ValidationError
    data = {"b": 2}
    with pytest.raises(ValidationError) as excinfo:
        Sample.from_dict(data)
    # The error message should mention the missing field
    assert "Missing required field" in str(excinfo.value) or "a" in str(excinfo.value)
