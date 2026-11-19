import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_default_application():
    # Schema with a required 'username' and an optional 'age' that defaults to 18
    schema = Schema(fields={"username": String(), "age": Integer(default=18)})

    # When 'age' is omitted, the default value should be applied
    result = schema.validate({"username": "alice"})
    assert result == {"username": "alice", "age": 18}

    # When 'age' is provided, the supplied value should be used
    result_with_age = schema.validate({"username": "bob", "age": 30})
    assert result_with_age == {"username": "bob", "age": 30}
