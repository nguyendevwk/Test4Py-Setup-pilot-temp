import pytest
from typesystem.composites import OneOf

class DummyField:
    def __init__(self, should_match, validated_value):
        self.should_match = should_match
        self.validated_value = validated_value

    def validate_or_error(self, value):
        if self.should_match:
            return self.validated_value, None
        return None, "error"

def test_oneof_validate_returns_candidate_when_exactly_one_match():
    matching = DummyField(True, "matched")
    non_matching = DummyField(False, None)
    field = OneOf([matching, non_matching])
    result = field.validate("any_value")
    assert result == "matched"
