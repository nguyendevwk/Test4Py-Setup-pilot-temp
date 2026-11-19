import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_missing_required():
    schema = Schema(fields={"name": String(), "age": Integer()})
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"name": "alice"})
    err = excinfo.value
    # The ValidationError should contain a Message for the missing 'age' key
    assert any(m.code == "required" and m.index == ["age"] for m in err.messages)
