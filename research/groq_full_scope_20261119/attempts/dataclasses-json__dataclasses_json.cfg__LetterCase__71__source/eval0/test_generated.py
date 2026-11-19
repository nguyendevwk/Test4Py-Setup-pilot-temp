import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_values_are_callables_and_transform():
    """Each LetterCase member should be a callable that transforms a string."""
    sample = "hello world"
    assert LetterCase.CAMEL.value(sample) == "helloWorld"
    assert LetterCase.KEBAB.value(sample) == "hello-world"
    assert LetterCase.SNAKE.value(sample) == "hello_world"
    assert LetterCase.PASCAL.value(sample) == "HelloWorld"

def test_lettercase_members_exist_and_are_unique():
    """All expected LetterCase members should exist and have unique values."""
    names = {"CAMEL", "KEBAB", "SNAKE", "PASCAL"}
    assert set(LetterCase.__members__.keys()) == names
    values = {member.value for member in LetterCase}
    assert len(values) == len(LetterCase)  # no duplicate functions

def test_invalid_member_access_raises_attribute_error():
    """Accessing a non-existent LetterCase member should raise AttributeError."""
    with pytest.raises(AttributeError):
        getattr(LetterCase, "UNKNOWN")
