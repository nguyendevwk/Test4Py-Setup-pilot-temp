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
        result = case.value(sample)
        assert result == func, f"{case.name} transformation failed: {result} != {func}"

def test_lettercase_members_are_unique_and_accessible():
    # Ensure each enum member is unique and can be accessed by name
    names = [member.name for member in LetterCase]
    assert set(names) == {"CAMEL", "KEBAB", "SNAKE", "PASCAL"}
    # Access by name and verify the value is a callable
    for name in names:
        member = LetterCase[name]
        assert callable(member.value), f"{name} value is not callable"

def test_invalid_access_raises_key_error():
    # Accessing a non-existent enum member should raise KeyError
    with pytest.raises(KeyError):
        _ = LetterCase["INVALID"]
