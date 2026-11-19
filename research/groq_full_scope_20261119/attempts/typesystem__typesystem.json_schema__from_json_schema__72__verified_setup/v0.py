import pytest
from typesystem.json_schema import from_json_schema
from typesystem.fields import Any, Choice, Integer, String, AllOf, NeverMatch

def test_bool_true_returns_any():
    """from_json_schema should return an Any field when given True."""
    result = from_json_schema(True)
    assert isinstance(result, Any)
    # Ensure that the returned object behaves like Any
    assert result.validate(123) is None
    assert result.validate("abc") is None

def test_enum_schema_returns_choice_with_correct_options():
    """from_json_schema should create a Choice field for an enum schema."""
    enum_schema = {"enum": ["red", "green", "blue"]}
    result = from_json_schema(enum_schema)
    assert isinstance(result, Choice)
    # The Choice field should accept any of the enum values
    for value in ["red", "green", "blue"]:
        assert result.validate(value) is None
    # And reject values not in the enum
    with pytest.raises(ValueError):
        result.validate("yellow")

def test_all_of_schema_combines_multiple_constraints():
    """from_json_schema should combine constraints using AllOf."""
    all_of_schema = {
        "allOf": [
            {"type": "integer"},
            {"type": "string"}
        ]
    }
    result = from_json_schema(all_of_schema)
    assert isinstance(result, AllOf)
    # AllOf should contain both Integer and String fields
    types = {type(field) for field in result.constraints}
    assert Integer in types
    assert String in types
    # The combined field should reject values that don't satisfy all constraints
    with pytest.raises(ValueError):
        result.validate(123)  # integer but not string
    with pytest.raises(ValueError):
        result.validate("abc")  # string but not integer
    # It should accept values that satisfy both (none exist, but test that validation passes for a dummy)
    # Since no value can be both integer and string, we skip positive test
