import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_values_are_callables_and_transform_strings():
    """Each LetterCase member should be a callable that transforms a string."""
    sample = "hello world"
    # CAMEL case
    camel = LetterCase.CAMEL.value(sample)
    assert camel == "helloWorld"
    # KEBAB case
    kebab = LetterCase.KEBAB.value(sample)
    assert kebab == "hello-world"
    # SNAKE case
    snake = LetterCase.SNAKE.value(sample)
    assert snake == "hello_world"
    # PASCAL case
    pascal = LetterCase.PASCAL.value(sample)
    assert pascal == "HelloWorld"

def test_lettercase_members_are_unique_and_accessible():
    """All expected members should exist and be unique."""
    names = {member.name for member in LetterCase}
    assert names == {"CAMEL", "KEBAB", "SNAKE", "PASCAL"}
    # Ensure each member is distinct
    values = {member.value for member in LetterCase}
    assert len(values) == 4

def test_invalid_access_raises_attribute_error():
    """Accessing a non-existent LetterCase member should raise AttributeError."""
    with pytest.raises(AttributeError):
        _ = LetterCase.NON_EXISTENT
