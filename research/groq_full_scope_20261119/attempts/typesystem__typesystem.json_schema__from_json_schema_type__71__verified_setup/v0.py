import pytest
from typesystem.json_schema import from_json_schema_type
from typesystem.fields import Float, Integer, String, Array, Object, NO_DEFAULT
from typesystem.schemas import Definitions

def test_number_field_with_constraints_and_default():
    data = {
        "minimum": 0,
        "maximum": 10,
        "exclusiveMinimum": 1,
        "exclusiveMaximum": 9,
        "multipleOf": 0.5,
        "default": 5.5,
    }
    field = from_json_schema_type(data, "number", allow_null=False, definitions=Definitions())
    assert isinstance(field, Float)
    assert field.minimum == 0
    assert field.maximum == 10
    assert field.exclusive_minimum == 1
    assert field.exclusive_maximum == 9
    assert field.multiple_of == 0.5
    assert field.default == 5.5
    assert field.allow_null is False
    assert field.coerce_types is False

def test_array_field_with_list_of_items_and_additional_items_schema():
    item_schema = {"type": "integer", "minimum": 1}
    additional_schema = {"type": "string", "maxLength": 3}
    data = {
        "items": [item_schema, item_schema],
        "additionalItems": additional_schema,
        "minItems": 2,
        "maxItems": 5,
        "uniqueItems": True,
        "default": [1, 2],
    }
    field = from_json_schema_type(data, "array", allow_null=True, definitions=Definitions())
    assert isinstance(field, Array)
    assert field.min_items == 2
    assert field.max_items == 5
    assert field.unique_items is True
    assert field.default == [1, 2]
    assert field.allow_null is True
    # items should be a list of Integer fields
    assert isinstance(field.items, list)
    assert all(isinstance(it, Integer) for it in field.items)
    # additional_items should be a String field
    assert isinstance(field.additional_items, String)
    assert field.additional_items.max_length == 3

def test_object_field_with_properties_and_pattern_properties():
    data = {
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string", "minLength": 1},
        },
        "patternProperties": {
            "^S_": {"type": "string"},
        },
        "additionalProperties": False,
        "propertyNames": {"type": "string", "minLength": 1},
        "minProperties": 1,
        "maxProperties": 3,
        "required": ["id"],
        "default": {"id": 0},
    }
    field = from_json_schema_type(data, "object", allow_null=False, definitions=Definitions())
    assert isinstance(field, Object)
    assert field.min_properties == 1
    assert field.max_properties == 3
    assert field.required == ["id"]
    assert field.default == {"id": 0}
    # properties dict
    assert isinstance(field.properties, dict)
    assert set(field.properties.keys()) == {"id", "name"}
    assert isinstance(field.properties["id"], Integer)
    assert isinstance(field.properties["name"], String)
    # pattern_properties dict
    assert isinstance(field.pattern_properties, dict)
    assert "^S_" in field.pattern_properties
    assert isinstance(field.pattern_properties["^S_"], String)
    # additional_properties is False
    assert field.additional_properties is False
    # property_names is a String field
    assert isinstance(field.property_names, String)
    assert field.property_names.min_length == 1
