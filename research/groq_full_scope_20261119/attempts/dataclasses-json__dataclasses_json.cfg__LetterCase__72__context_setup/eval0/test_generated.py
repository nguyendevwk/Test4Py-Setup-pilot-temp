import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_functions_are_callable_and_return_expected_strings(tmp_path):
    # Create a sample string to test each case transformation
    sample = "hello world"
    # Expected results using the imported functions
    expected = {
        LetterCase.CAMEL: "helloWorld",
        LetterCase.KEBAB: "hello-world",
        LetterCase.SNAKE: "hello_world",
        LetterCase.PASCAL: "HelloWorld",
    }
    for case, func in expected.items():
        # The enum value is the function itself
        assert callable(case.value)
        # Apply the function and compare to expected string
        assert case.value(sample) == func

def test_lettercase_members_are_unique_and_accessible():
    # Ensure each enum member is unique and can be accessed by name
    names = ["CAMEL", "KEBAB", "SNAKE", "PASCAL"]
    members = [LetterCase[name] for name in names]
    # All members should be distinct objects
    assert len(set(members)) == len(members)
    # Verify that accessing by value returns the same member
    for member in members:
        assert LetterCase(member.value) is member

def test_lettercase_invalid_access_raises_key_error():
    # Accessing a non-existent enum member should raise KeyError
    with pytest.raises(KeyError):
        _ = LetterCase["INVALID"]
