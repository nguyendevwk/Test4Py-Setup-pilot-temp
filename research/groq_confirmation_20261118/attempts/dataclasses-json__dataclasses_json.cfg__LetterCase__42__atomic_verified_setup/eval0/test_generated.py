import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_value_functions():
    # Each enum member should provide a callable that transforms a string
    assert callable(LetterCase.CAMEL.value)
    assert callable(LetterCase.KEBAB.value)
    assert callable(LetterCase.SNAKE.value)
    assert callable(LetterCase.PASCAL.value)

    # Verify that the transformations produce expected results
    assert LetterCase.CAMEL.value("hello_world") == "helloWorld"
    assert LetterCase.KEBAB.value("helloWorld") == "hello-world"
    assert LetterCase.SNAKE.value("helloWorld") == "hello_world"
    assert LetterCase.PASCAL.value("hello_world") == "HelloWorld"

def test_lettercase_iteration_and_lookup():
    # Iterating over the enum should yield all four members
    members = list(LetterCase)
    assert len(members) == 4
    assert set(members) == {LetterCase.CAMEL, LetterCase.KEBAB, LetterCase.SNAKE, LetterCase.PASCAL}

    # Lookup by name should return the correct member
    assert LetterCase["CAMEL"] is LetterCase.CAMEL
    assert LetterCase["KEBAB"] is LetterCase.KEBAB
    assert LetterCase["SNAKE"] is LetterCase.SNAKE
    assert LetterCase["PASCAL"] is LetterCase.PASCAL

def test_lettercase_invalid_access_raises():
    # Accessing a non-existent enum member should raise a KeyError
    with pytest.raises(KeyError):
        _ = LetterCase["INVALID"]
