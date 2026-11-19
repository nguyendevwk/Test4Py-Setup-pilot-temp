import pytest
from typesystem.fields import Float, Integer, String, Array, Object
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
    field = from_json_schema_type(data, "number", allow_null=False, definitions=Definitions())
    assert isinstance(field, Float)
    assert field.minimum == 0
    assert field.maximum == 10
    assert field.exclusive_minimum == 1
    assert field.exclusive_maximum == 9
    assert field.multiple_of == 2
    assert field.default == 5
    assert field.allow_null is False

def test_array_with_list_of_items_and_additional_items():
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
    field = from_json_schema_type(data, "array", allow_null=False, definitions=Definitions())
    assert isinstance(field, Array)
    assert field.min_items == 2
    assert field.max_items == 5
    assert field.unique_items is True
    assert field.default == [1, "abc"]
    # items should be a list of Fields
    assert isinstance(field.items, list)
    assert len(field.items) == 2
    assert isinstance(field.items[0], Integer)
    assert isinstance(field.items[1], String)
    # additional_items should be a Field
    assert isinstance(field.additional_items, (Integer, String, Boolean))
    assert isinstance(field.additional_items, Boolean)

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
        "propertyNames": {"type": "string"},
        "minProperties": 1,
        "maxProperties": 3,
        "required": ["id"],
        "default": {"id": 0, "name": "default"}
    }
    field = from_json_schema_type(data, "object", allow_null=False, definitions=Definitions())
    assert isinstance(field, Object)
    assert field.min_properties == 1
    assert field.max_properties == 3
    assert field.required == ["id"]
    assert field.default == {"id": 0, "name": "default"}
    # properties dict
    assert isinstance(field.properties, dict)
    assert set(field.properties.keys()) == {"id", "name"}
    assert isinstance(field.properties["id"], Integer)
    assert isinstance(field.properties["name"], String)
    # pattern_properties dict
    assert isinstance(field.pattern_properties, dict)
    assert "^S_" in field.pattern_properties
    assert isinstance(field.pattern_properties["^S_"], String)
    # additional_properties should be False
    assert field.additional_properties is False
    # property_names should be a Field
    assert isinstance(field.property_names, String)
