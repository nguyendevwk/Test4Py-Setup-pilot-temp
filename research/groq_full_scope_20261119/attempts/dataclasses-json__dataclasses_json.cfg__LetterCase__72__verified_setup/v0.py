import pytest
from dataclasses_json.cfg import LetterCase

def test_lettercase_functions_are_callable_and_return_expected_strings(tmp_path):
    # Create a sample string to test each case conversion
    sample = "hello world"
    # Expected results for each case
    expected = {
        LetterCase.CAMEL: "helloWorld",
        LetterCase.KEBAB: "hello-world",
        LetterCase.SNAKE: "hello_world",
        LetterCase.PASCAL: "HelloWorld",
    }
    for case, func in expected.items():
        # The enum value is the conversion function
        result = case.value(sample)
        assert result == func, f"{case.name} conversion failed: {result} != {func}"

def test_lettercase_enum_members_exist_and_are_unique():
    # Ensure all expected members are present
    names = {member.name for member in LetterCase}
    assert names == {"CAMEL", "KEBAB", "SNAKE", "PASCAL"}
    # Ensure each member maps to a distinct function object
    values = {member.value for member in LetterCase}
    assert len(values) == 4, "LetterCase enum values are not unique"

def test_invalid_access_raises_attribute_error():
    # Accessing a non-existent enum member should raise AttributeError
    with pytest.raises(AttributeError):
        _ = LetterCase.NON_EXISTENT
