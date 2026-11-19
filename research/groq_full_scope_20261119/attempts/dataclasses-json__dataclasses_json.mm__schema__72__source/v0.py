import dataclasses
import typing
import pytest
from dataclasses_json.mm import schema
from marshmallow import fields, Schema

# Helper dataclass for testing
@dataclasses.dataclass
class TestData:
    required: int
    optional: typing.Optional[str] = None
    default: float = 3.14
    custom: int = dataclasses.field(metadata={"dataclasses_json": {"mm_field": fields.String()}})

def test_schema_basic_fields(tmp_path):
    """Verify that required, optional, default and custom fields are correctly
    represented in the generated schema."""
    result = schema(TestData, mixin=Schema, infer_missing=True)
    # required field should be present and not marked as required
    assert "required" in result
    assert isinstance(result["required"], fields.Integer)
    assert result["required"].required is False
    # optional field should allow None and be optional
    assert "optional" in result
    assert isinstance(result["optional"], fields.String)
    assert result["optional"].allow_none is True
    assert result["optional"].required is False
    # default field should have default value set
    assert "default" in result
    assert isinstance(result["default"], fields.Float)
    assert result["default"].default == 3.14
    # custom field should use the provided mm_field
    assert "custom" in result
    assert isinstance(result["custom"], fields.String)

def test_schema_missing_and_allow_none(tmp_path):
    """Test that fields without defaults are marked required and that
    None is allowed when appropriate."""
    @dataclasses.dataclass
    class NoDefault:
        a: int
        b: typing.Optional[int] = None
    result = schema(NoDefault, mixin=Schema, infer_missing=False)
    # 'a' has no default, should be required
    assert result["a"].required is True
    # 'b' is optional, should allow None
    assert result["b"].allow_none is True
    assert result["b"].required is False

def test_schema_infer_missing_false(tmp_path):
    """When infer_missing is False, fields with defaults should not be
    marked as required and should use the default value."""
    @dataclasses.dataclass
    class WithDefault:
        x: int = 42
    result = schema(WithDefault, mixin=Schema, infer_missing=False)
    assert result["x"].required is False
    assert result["x"].default == 42
