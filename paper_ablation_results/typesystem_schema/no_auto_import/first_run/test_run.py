import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_default_and_read_only_behavior():
    # Field 'a' has a default, field 'b' is read-only
    schema = Schema(fields={"a": String(default="foo"), "b": Integer(read_only=True)})

    # No input: default for 'a' should be used, 'b' ignored
    result = schema.validate({})
    assert result == {"a": "foo"}
    assert "b" not in result

    # Providing a value for 'b' should not affect the result
    result = schema.validate({"b": 42})
    assert result == {"a": "foo"}
    assert "b" not in result

    # Providing a value for 'a' overrides the default
    result = schema.validate({"a": "bar"})
    assert result == {"a": "bar"}
