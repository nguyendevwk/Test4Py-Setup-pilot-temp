import pytest
from dataclasses import dataclass, field
from dataclasses_json.undefined import (
    Undefined,
    _IgnoreUndefinedParameters,
    _RaiseUndefinedParameters,
    UndefinedParameterError,
)
from dataclasses import fields


def test_ignore_undefined_parameters_filters_unknown():
    @dataclass
    class Sample:
        x: int
        y: str = field(default="default")

    # Provide both known and unknown keys
    input_dict = {"x": 10, "y": "hello", "z": 99}
    # _IgnoreUndefinedParameters should drop the unknown key 'z'
    filtered = _IgnoreUndefinedParameters.handle_from_dict(Sample, input_dict)
    assert filtered == {"x": 10, "y": "hello"}
    # Ensure the unknown key is not present
    assert "z" not in filtered


def test_raise_undefined_parameters_raises_on_unknown():
    @dataclass
    class Sample:
        a: int
        b: str

    # Provide an unknown key 'c'
    input_dict = {"a": 1, "b": "test", "c": 42}
    with pytest.raises(UndefinedParameterError) as excinfo:
        _RaiseUndefinedParameters.handle_from_dict(Sample, input_dict)
    # The error message should mention the unknown key
    assert "c" in str(excinfo.value)


def test_undefined_enum_mapping_to_action_classes():
    # The Undefined enum should map to the correct action classes
    assert Undefined.INCLUDE.__name__ == "_CatchAllUndefinedParameters"
    assert Undefined.RAISE.__name__ == "_RaiseUndefinedParameters"
    assert Undefined.EXCLUDE.__name__ == "_IgnoreUndefinedParameters"
    # Verify that the mapped classes are indeed the ones imported
    assert Undefined.INCLUDE is _CatchAllUndefinedParameters
    assert Undefined.RAISE is _RaiseUndefinedParameters
    assert Undefined.EXCLUDE is _IgnoreUndefinedParameters
