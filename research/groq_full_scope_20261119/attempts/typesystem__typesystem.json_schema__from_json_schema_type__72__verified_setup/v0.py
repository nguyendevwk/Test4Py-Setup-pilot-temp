import pytest
from typesystem.json_schema import from_json_schema_type
from typesystem.fields import Float, Integer, String, Array, Object, NO_DEFAULT

def test_number_field_creation():
    data = {"minimum": 0, "maximum": 10, "multipleOf": 2, "default": 4}
    field = from_json_schema_type(data, "number", allow_null=False, definitions={})
    assert isinstance(field, Float)
    assert field.minimum == 0
    assert field.maximum == 10
    assert field.multiple_of == 2
    assert field.default == 4
    assert field.allow_null is False
    assert field.coerce_types is False

def test_array_with_multiple_items_and_additional_items():
    data = {
        "items": [
            {"type": "integer"},
            {"type": "string", "minLength": 3}
        ],
        "additionalItems": {"type": "boolean"},
        "minItems": 1,
        "uniqueItems": True,
        "default": [1, "abc"]
    }
    field = from_json_schema_type(data, "array", allow_null=True, definitions={})
    assert isinstance(field, Array)
    assert field.min_items == 1
    assert field.unique_items is True
    assert field.default == [1, "abc"]
    assert field.allow_null is True
    # items should be a list of fields
    assert isinstance(field.items, list)
    assert len(field.items) == 2
    assert isinstance(field.items[0], Integer)
    assert isinstance(field.items[1], String)
    assert field.items[1].min_length == 3
    # additional_items should be a Boolean field
    assert isinstance(field.additional_items, type(field.items[0]))
    assert isinstance(field.additional_items, Integer) or isinstance(field.additional_items, Boolean)

def test_object_with_properties_and_pattern_properties():
    data = {
        "properties": {
            "id": {"type": "integer", "minimum": 1},
            "name": {"type": "string", "minLength": 1}
        },
        "patternProperties": {
            "^S_": {"type": "string"}
        },
        "additionalProperties": False,
        "required": ["id"],
        "default": {"id": 1, "name": "foo"}
    }
    field = from_json_schema_type(data, "object", allow_null=False, definitions={})
    assert isinstance(field, Object)
    assert field.required == ["id"]
    assert field.default == {"id": 1, "name": "foo"}
    assert field.allow_null is False
    # properties
    assert isinstance(field.properties, dict)
    assert set(field.properties.keys()) == {"id", "name"}
    assert isinstance(field.properties["id"], Integer)
    assert field.properties["id"].minimum == 1
    assert isinstance(field.properties["name"], String)
    assert field.properties["name"].min_length == 1
    # pattern_properties
    assert isinstance(field.pattern_properties, dict)
    assert "^S_" in field.pattern_properties
    assert isinstance(field.pattern_properties["^S_"], String)
    # additional_properties should be False
    assert field.additional_properties is False
