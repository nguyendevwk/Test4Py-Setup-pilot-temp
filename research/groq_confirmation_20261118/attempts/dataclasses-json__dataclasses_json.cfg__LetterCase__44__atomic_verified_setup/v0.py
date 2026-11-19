import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_value_functions():
    """Each LetterCase member should provide a callable that transforms a string."""
    # Test CAMEL case
    camel = LetterCase.CAMEL.value
    assert callable(camel)
    assert camel("hello_world") == "helloWorld"
    # Test KEBAB case
    kebab = LetterCase.KEBAB.value
    assert callable(kebab)
    assert kebab("HelloWorld") == "hello-world"
    # Test SNAKE case
    snake = LetterCase.SNAKE.value
    assert callable(snake)
    assert snake("helloWorld") == "hello_world"
    # Test PASCAL case
    pascal = LetterCase.PASCAL.value
    assert callable(pascal)
    assert pascal("hello_world") == "HelloWorld"

def test_lettercase_iteration_and_members():
    """Iterating over LetterCase should yield all defined members."""
    names = {member.name for member in LetterCase}
    expected = {"CAMEL", "KEBAB", "SNAKE", "PASCAL"}
    assert names == expected
    # Ensure each member is unique
    values = {member.value for member in LetterCase}
    assert len(values) == 4

def test_invalid_lettercase_creation():
    """Creating a LetterCase with an invalid value should raise ValueError."""
    with pytest.raises(ValueError):
        LetterCase("invalid_value")
