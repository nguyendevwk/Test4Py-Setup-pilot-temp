import pytest
from dataclasses import dataclass, field
from typing import Dict

# Import the target module (assumed to be named `dataclasses_json.undefined`)
# Adjust the import path if necessary.
from dataclasses_json.undefined import (
    Undefined,
    _RaiseUndefinedParameters,
    UndefinedParameterError,
    _IgnoreUndefinedParameters,
    _CatchAllUndefinedParameters,
)

# ---------------------------------------------------------------------------

def test_undefined_enum_members_and_types():
    """
    Verify that the Undefined enum members are correctly associated with
    their handler classes and that the enum behaves as expected.
    """
    # The enum should have exactly three members
    assert set(Undefined.__members__.keys()) == {"INCLUDE", "RAISE", "EXCLUDE"}

    # Each member should be an instance of Undefined
    for member in Undefined:
        assert isinstance(member, Undefined)

    # The value of each member should be the corresponding handler class
    assert Undefined.INCLUDE.value is _CatchAllUndefinedParameters
    assert Undefined.RAISE.value is _RaiseUndefinedParameters
    assert Undefined.EXCLUDE.value is _IgnoreUndefinedParameters

    # The enum should be iterable and preserve order
    assert list(Undefined) == [
        Undefined.INCLUDE,
        Undefined.RAISE,
        Undefined.EXCLUDE,
    ]


def test_raise_undefined_parameters_raises_error():
    """
    Ensure that _RaiseUndefinedParameters.handle_from_dict raises
    UndefinedParameterError when unknown keys are present.
    """
    # Define a simple dataclass to use as the target class
    @dataclass
    class Sample:
        a: int
        b: str = field(default="default")

    # Known parameters only – should return unchanged dict
    known = {"a": 1, "b": "hello"}
    result = _RaiseUndefinedParameters.handle_from_dict(Sample, known)
    assert result == known

    # Unknown parameter present – should raise UndefinedParameterError
    with pytest.raises(UndefinedParameterError) as excinfo:
        _RaiseUndefinedParameters.handle_from_dict(Sample, {"a": 1, "c": 42})
    assert "undefined initialization arguments" in str(excinfo.value)
    assert "c" in str(excinfo.value)


def test_ignore_undefined_parameters_does_not_include_unknown():
    """
    Verify that _IgnoreUndefinedParameters.handle_from_dict discards
    unknown keys and that the resulting dict contains only known fields.
    """
    @dataclass
    class Sample:
        x: float
        y: int = 0

    # Input with an unknown key 'z'
    input_dict = {"x": 3.14, "z": "extra"}
    result = _IgnoreUndefinedParameters.handle_from_dict(Sample, input_dict)

    # The unknown key should be removed
    assert "z" not in result
    # Known keys should remain unchanged
    assert result == {"x": 3.14}
