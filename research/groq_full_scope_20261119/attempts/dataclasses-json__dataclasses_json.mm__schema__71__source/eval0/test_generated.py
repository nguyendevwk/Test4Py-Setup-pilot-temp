import dataclasses
import typing
import pytest
from dataclasses_json.mm import schema

# --------------------------------------------------------------------------- #
# Test 1: Normal dataclass with required and default fields
# --------------------------------------------------------------------------- #
def test_schema_basic_fields():
    @dataclasses.dataclass
    class Person:
        name: str
        age: int = 30

    result = schema(Person, mixin=None, infer_missing=True)
    # name is required because no default
    assert result["name"].required is True
    # age has default, so missing key should be 'default' and set to 30
    assert result["age"].default == 30
    # The schema should contain exactly two fields
    assert set(result.keys()) == {"name", "age"}

# --------------------------------------------------------------------------- #
# Test 2: Optional field handling
# --------------------------------------------------------------------------- #
def test_schema_optional_field():
    @dataclasses.dataclass
    class Item:
        id: int
        description: typing.Optional[str] = None

    result = schema(Item, mixin=None, infer_missing=False)
    # id is required
    assert result["id"].required is True
    # description is optional: allow_none True and default None
    assert result["description"].allow_none is True
    assert result["description"].default is None
    # Ensure the field is present
    assert "description" in result

# --------------------------------------------------------------------------- #
# Test 3: Error when passing a non-dataclass
# --------------------------------------------------------------------------- #
def test_schema_non_dataclass_raises():
    class NotADataclass:
        x: int

    with pytest.raises(TypeError):
        schema(NotADataclass, mixin=None, infer_missing=True)
