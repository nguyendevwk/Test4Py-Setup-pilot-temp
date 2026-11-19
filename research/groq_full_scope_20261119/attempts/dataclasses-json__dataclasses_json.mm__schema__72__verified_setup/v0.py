import typing
import dataclasses
import pytest
from dataclasses import dataclass, field
from dataclasses_json.mm import schema
from marshmallow import fields

# Helper dataclass for testing
@dataclass
class TestData:
    a: int
    b: str = "default"
    c: typing.Optional[float] = None
    d: typing.List[int] = field(default_factory=list)
    e: typing.Any = field(metadata={"dataclasses_json": {"mm_field": fields.String()}})

def test_schema_basic_fields():
    """Verify that required, default, optional and list fields are correctly represented."""
    result = schema(TestData, mixin=None, infer_missing=False)
    # Required field 'a' should be present and of type Integer
    assert "a" in result
    assert isinstance(result["a"], fields.Integer)
    # Field 'b' has a default, so it should not be required
    assert "b" in result
    assert result["b"].required is False
    assert result["b"].missing == "default"
    # Optional field 'c' should allow None
    assert "c" in result
    assert result["c"].allow_none is True
    # List field 'd' should be a List field
    assert "d" in result
    assert isinstance(result["d"], fields.List)
    assert isinstance(result["d"].inner, fields.Integer)
    # Field 'e' uses a custom mm_field
    assert "e" in result
    assert result["e"] is fields.String()

def test_schema_infer_missing():
    """When infer_missing is True, missing defaults should be inferred as None."""
    result = schema(TestData, mixin=None, infer_missing=True)
    # Field 'b' should now be required because infer_missing=True
    assert result["b"].required is True
    # Optional field 'c' should still allow None
    assert result["c"].allow_none is True
    # Field 'd' should be required
    assert result["d"].required is True

def test_schema_missing_and_none_behavior():
    """Ensure that fields with None default are marked allow_none and missing correctly."""
    @dataclass
    class NoneDefault:
        x: typing.Optional[int] = None
        y: typing.Optional[str] = field(default_factory=lambda: None)

    result = schema(NoneDefault, mixin=None, infer_missing=False)
    # Both fields should allow None
    assert result["x"].allow_none is True
    assert result["y"].allow_none is True
    # Both should be required because no default value is provided
    assert result["x"].required is True
    assert result["y"].required is True
