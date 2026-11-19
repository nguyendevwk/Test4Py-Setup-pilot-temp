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
    """Accessing the same member should return the same enum instance."""
    camel1 = LetterCase.CAMEL
    camel2 = LetterCase["CAMEL"]
    assert camel1 is camel2
    assert camel1.name == "CAMEL"
    assert camel1.value is LetterCase.CAMEL.value  # same callable object


def test_invalid_lettercase_access_raises():
    """Accessing a non‑existent LetterCase member should raise AttributeError."""
    with pytest.raises(AttributeError):
        _ = LetterCase["INVALID"]
