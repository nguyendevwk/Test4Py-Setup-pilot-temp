import pytest
from typesystem.fields import Float, Integer, String, Array, Object, Any, NeverMatch
from typesystem.schemas import Definitions
from typesystem.json_schema import from_json_schema_type, from_json_schema

def test_number_field_constraints():
    data = {
        "minimum": 0,
        "maximum": 10,
        "exclusiveMinimum": 1,
        "exclusiveMaximum": 9,
        "multipleOf": 2,
        "default": 5,
    }
    field = from_json_schema_type(data, type_string="number", allow_null=False, definitions=Definitions())
    assert isinstance(field, Float)
    assert field.minimum == 0
    assert field.maximum == 10
    assert field.exclusive_minimum == 1
    assert field.exclusive_maximum == 9
    assert field.multiple_of == 2
    assert field.default == 5
    assert field.allow_null is False

def test_array_with_multiple_items_and_additional_items():
    data = {
        "items": [
            {"type": "integer"},
            {"type": "string", "minLength": 3}
        ],
        "additionalItems": {"type": "boolean"},
        "minItems": 2,
        "maxItems": 5,
        "uniqueItems": True,
        "default": [1, "abc"]
    }
    field = from_json_schema_type(data, type_string="array", allow_null=False, definitions=Definitions())
    assert isinstance(field, Array)
    assert field.min_items == 2
    assert field.max_items == 5
    assert field.unique_items is True
    assert field.default == [1, "abc"]
    # items should be a list of fields
    assert isinstance(field.items, list)
    assert len(field.items) == 2
    assert isinstance(field.items[0], Integer)
    assert isinstance(field.items[1], String)
    assert field.items[1].min_length == 3
    # additional_items should be a field
    assert isinstance(field.additional_items, Any) or isinstance(field.additional_items, Boolean)

def test_object_with_properties_and_pattern_properties():
    data = {
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string", "minLength": 1}
        },
        "patternProperties": {
            "^S_": {"type": "string"}
        },
        "additionalProperties": False,
        "propertyNames": {"type": "string", "minLength": 2},
        "minProperties": 1,
        "maxProperties": 3,
        "required": ["id"],
        "default": {"id": 1, "name": "x"}
    }
    field = from_json_schema_type(data, type_string="object", allow_null=False, definitions=Definitions())
    assert isinstance(field, Object)
    assert field.min_properties == 1
    assert field.max_properties == 3
    assert field.required == ["id"]
    assert field.default == {"id": 1, "name": "x"}
    # properties
    assert isinstance(field.properties, dict)
    assert "id" in field.properties and isinstance(field.properties["id"], Integer)
    assert "name" in field.properties and isinstance(field.properties["name"], String)
    assert field.properties["name"].min_length == 1
    # pattern_properties
    assert isinstance(field.pattern_properties, dict)
    assert "^S_" in field.pattern_properties and isinstance(field.pattern_properties["^S_"], String)
    # additional_properties
    assert field.additional_properties is False
    # property_names
    assert isinstance(field.property_names, String)
    assert field.property_names.min_length == 2
