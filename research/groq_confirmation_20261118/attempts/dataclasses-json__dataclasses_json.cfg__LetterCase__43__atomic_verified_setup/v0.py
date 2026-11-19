import pytest
from dataclasses_json.cfg import LetterCase


def test_lettercase_value_functions():
    """Each LetterCase member should provide a callable that transforms a string."""
    # Test camel case
    assert LetterCase.CAMEL.value("hello_world") == "helloWorld"
    # Test kebab case
    assert LetterCase.KEBAB.value("HelloWorld") == "hello-world"
    # Test snake case
    assert LetterCase.SNAKE.value("helloWorld") == "hello_world"
    # Test pascal case
    assert LetterCase.PASCAL.value("hello_world") == "HelloWorld"


def test_lettercase_member_access_and_identity():
    """Accessing members by name should return the same enum instance."""
    assert LetterCase["CAMEL"] is LetterCase.CAMEL
    assert LetterCase["KEBAB"] is LetterCase.KEBAB
    assert LetterCase["SNAKE"] is LetterCase.SNAKE
    assert LetterCase["PASCAL"] is LetterCase.PASCAL


def test_invalid_lettercase_access_raises():
    """Accessing a non‑existent LetterCase member should raise KeyError."""
    with pytest.raises(KeyError):
        _ = LetterCase["INVALID"]
