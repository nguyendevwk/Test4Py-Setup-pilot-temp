import pytest
from typesystem.json_schema import from_json_schema
from typesystem.fields import Any, NeverMatch, Choice, AllOf, Union, Const

def test_boolean_input_returns_correct_field():
    # True should return Any field
    field_true = from_json_schema(True)
    assert isinstance(field_true, Any)

    # False should return NeverMatch field
    field_false = from_json_schema(False)
    assert isinstance(field_false, NeverMatch)

def test_enum_schema_creates_choice_field_with_correct_choices():
    enum_schema = {"enum": ["red", "green", "blue"]}
    field = from_json_schema(enum_schema)
    assert isinstance(field, Choice)
    # Choices should be tuples of (value, display)
    expected_choices = [("red", "red"), ("green", "green"), ("blue", "blue")]
    assert field.choices == expected_choices

def test_all_of_schema_composes_multiple_constraints():
    # Define a schema that requires a string of minLength 3 and a number >= 10
    schema = {
        "allOf": [
            {"type": "string", "minLength": 3},
            {"type": "number", "minimum": 10}
        ]
    }
    field = from_json_schema(schema)
    assert isinstance(field, AllOf)
    # AllOf should contain two constraints: a String field and a Number field
    types = [type(subfield) for subfield in field.all_of]
    from typesystem.fields import String, Number
    assert String in types
    assert Number in types
    # The String constraint should enforce minLength
    string_field = next(f for f in field.all_of if isinstance(f, String))
    assert string_field.min_length == 3
    # The Number constraint should enforce minimum
    number_field = next(f for f in field.all_of if isinstance(f, Number))
    assert number_field.minimum == 10
