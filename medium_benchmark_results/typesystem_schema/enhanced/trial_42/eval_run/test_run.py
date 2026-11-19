import pytest
from typesystem.schemas import Schema
from typesystem.fields import Integer, String

def test_schema_applies_default_values_and_skips_read_only_fields():
    # Field 'a' has a default; field 'b' is read-only and should be ignored.
    schema = Schema(fields={"a": Integer(default=5), "b": String(read_only=True)})

    # Validate with no data: default for 'a' should be applied, 'b' omitted.
    result = schema.validate({})
    assert result == {"a": 5}

    # Validate with explicit value for 'a': default should be overridden.
    result = schema.validate({"a": 10})
    assert result == {"a": 10}

    # Validate with data for read-only field 'b': it should not appear in output.
    result = schema.validate({"b": "ignored"})
    assert result == {"a": 5}
