import pytest
from typesystem.composites import OneOf

class DummyField:
    def __init__(self, match_func):
        self.match_func = match_func

    def validate_or_error(self, value):
        if self.match_func(value):
            return value, None
        return None, "error"

def test_oneof_multiple_matches_raises():
    field1 = DummyField(lambda v: isinstance(v, int))
    field2 = DummyField(lambda v: isinstance(v, int))
    oneof = OneOf(one_of=[field1, field2])
    with pytest.raises(Exception) as excinfo:
        oneof.validate(42)
    assert "Matched more than one type." in str(excinfo.value)
