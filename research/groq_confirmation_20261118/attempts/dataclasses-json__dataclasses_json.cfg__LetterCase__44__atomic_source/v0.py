import pytest
from dataclasses_json.cfg import LetterCase


def test_lettercase_values_are_callables_and_transform_correctly():
    """Each LetterCase member should be a callable that transforms a string."""
    sample = "hello world"
    assert LetterCase.CAMEL.value(sample) == "helloWorld"
    assert LetterCase.KEBAB.value(sample) == "hello-world"
    assert LetterCase.SNAKE.value(sample) == "hello_world"
    assert LetterCase.PASCAL.value(sample) == "HelloWorld"
    # Ensure the values are indeed callables
    for member in LetterCase:
        assert callable(member.value)


def test_lettercase_iteration_and_membership():
    """Iterating over LetterCase should yield all defined members."""
    names = {member.name for member in LetterCase}
    expected = {"CAMEL", "KEBAB", "SNAKE", "PASCAL"}
    assert names == expected
    # Membership test
    assert LetterCase.CAMEL in LetterCase
    assert LetterCase("CAMEL") == LetterCase.CAMEL
    with pytest.raises(ValueError):
        LetterCase("INVALID")  # invalid name should raise ValueError


def test_lettercase_invalid_access_and_type_errors():
    """Accessing LetterCase with an invalid key or wrong type should raise appropriate errors."""
    with pytest.raises(AttributeError):
        getattr(LetterCase, "NON_EXISTENT")
    with pytest.raises(TypeError):
        # Enum members are not subscriptable by integer
        LetterCase[0]  # type: ignore
