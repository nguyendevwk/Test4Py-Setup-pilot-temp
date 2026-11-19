import pytest
from typesystem.json_schema import from_json_schema, Any, NeverMatch, Choice, AllOf, Union, Const, Reference

def test_boolean_true_and_false():
    # True should map to Any
    field_true = from_json_schema(True)
    assert isinstance(field_true, Any)

    # False should map to NeverMatch
    field_false = from_json_schema(False)
    assert isinstance(field_false, NeverMatch)

def test_enum_and_const():
    # Enum schema should produce a Choice field with correct choices
    enum_schema = {"enum": ["red", "green", "blue"]}
    field_enum = from_json_schema(enum_schema)
    assert isinstance(field_enum, Choice)
    # Choices are tuples of (value, display)
    expected_choices = [("red", "red"), ("green", "green"), ("blue", "blue")]
    assert field_enum.choices == expected_choices

    # Const schema should produce a Const field with the given value
    const_schema = {"const": 42}
    field_const = from_json_schema(const_schema)
    assert isinstance(field_const, Const)
    assert field_const.const == 42

def test_all_of_and_reference():
    # allOf schema should produce an AllOf field containing the subfields
    sub_schema1 = {"type": "string"}
    sub_schema2 = {"type": "integer"}
    all_of_schema = {"allOf": [sub_schema1, sub_schema2]}
    field_all_of = from_json_schema(all_of_schema)
    assert isinstance(field_all_of, AllOf)
    # The AllOf should contain two fields: a String and an Integer
    types = [type(f) for f in field_all_of.all_of]
    from typesystem.fields import String, Integer
    assert String in types and Integer in types

    # Reference schema should produce a Reference field pointing to the correct ref
    ref_schema = {"$ref": "#/components/schemas/MyType"}
    field_ref = from_json_schema(ref_schema)
    assert isinstance(field_ref, Reference)
    assert field_ref.to == "#/components/schemas/MyType"
