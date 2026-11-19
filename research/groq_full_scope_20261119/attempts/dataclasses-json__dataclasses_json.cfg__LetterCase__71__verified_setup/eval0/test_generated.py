import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_values_are_callables():
    """Each LetterCase member should provide a callable that transforms a string."""
    for member in LetterCase:
        func = member.value
        assert callable(func), f"{member} value is not callable"
        # Test that the function returns a string and changes the case
        original = "TestString"
        transformed = func(original)
        assert isinstance(transformed, str), "Result is not a string"
        assert transformed != original, "Transformation did not change the string"

def test_lettercase_member_names_and_expected_functions():
    """Verify that each enum member name maps to the correct transformation function."""
    assert LetterCase.CAMEL.value("test_string") == "testString"
    assert LetterCase.KEBAB.value("testString") == "test-string"
    assert LetterCase.SNAKE.value("testString") == "test_string"
    assert LetterCase.PASCAL.value("test_string") == "TestString"

def test_lettercase_invalid_access_raises_attribute_error():
    """Accessing a non-existent member should raise AttributeError."""
    with pytest.raises(AttributeError):
        _ = LetterCase.NON_EXISTENT
