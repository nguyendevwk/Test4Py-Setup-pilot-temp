import typing
import dataclasses
import pytest
from dataclasses import dataclass, field
from dataclasses_json import mm
from dataclasses_json.mm import schema as mm_schema
from marshmallow import fields

# Helper dataclass for testing
@dataclass
class TestData:
    # required field
    required_int: int
    # field with default
    default_str: str = "default"
    # field with default_factory
    default_list: typing.List[int] = dataclasses.field(default_factory=lambda: [1, 2, 3])
    # optional field
    optional_float: typing.Optional[float] = None
    # field with custom mm_field
    custom_field: int = dataclasses.field(metadata={"mm_field": fields.String()})
    # field with letter_case transformation
    camel_case: int = dataclasses.field(metadata={"letter_case": lambda name: name.replace("_", "")})
    # field with custom decoder
    decoded_field: int = dataclasses.field(metadata={"decoder": lambda x: x * 2})


def test_mm_schema_basic_fields(tmp_path):
    """Test that required, default, default_factory, and optional fields are handled correctly."""
    result = mm_schema(TestData, mixin=None, infer_missing=True)
    # required_int should be present and required
    assert "required_int" in result
    assert isinstance(result["required_int"], fields.Integer)
    assert result["required_int"].required is True
    # default_str should have default value
    assert result["default_str"].default == "default"
    # default_list should use default_factory value
    assert result["default_list"].default == [1, 2, 3]
    # optional_float should allow None and be optional
    assert result["optional_float"].allow_none is True
    assert result["optional_float"].required is False


def test_mm_schema_custom_mm_field_and_letter_case(tmp_path):
    """Test that custom mm_field and letter_case metadata are respected."""
    result = mm_schema(TestData, mixin=None, infer_missing=True)
    # custom_field should use the provided String field
    assert isinstance(result["custom_field"], fields.String)
    # camel_case should have data_key transformed
    assert result["camel_case"].data_key == "camelCase"


def test_mm_schema_custom_decoder(tmp_path):
    """Test that a custom decoder replaces the field's _deserialize method."""
    result = mm_schema(TestData, mixin=None, infer_missing=True)
    # decoded_field should have a custom _deserialize that doubles the value
    # We test by calling the method directly
    original_value = 5
    deserialized = result["decoded_field"]._deserialize(original_value, None, None)
    assert deserialized == original_value * 2
