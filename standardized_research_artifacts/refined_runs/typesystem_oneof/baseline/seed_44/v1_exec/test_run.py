import pytest
from typesystem.composites import OneOf

class DummyField:
    def __init__(self, name, match_value, validated_value):
        self.name = name
        self.match_value = match_value
        self.validated_value = validated_value

    def validate_or_error(self, value):
        if value == self.match_value:
            return (self.validated_value, None)
        return (None, f"{self.name}_error")

def test_oneof_validate_single_match_returns_candidate():
    field_a = DummyField("a", 1, "validated_a")
    field_b = DummyField("b", 2, "validated_b")
    oneof = OneOf([field_a, field_b])
    assert oneof.validate(1) == "validated_a"
    assert oneof.validate(2) == "validated_b"
