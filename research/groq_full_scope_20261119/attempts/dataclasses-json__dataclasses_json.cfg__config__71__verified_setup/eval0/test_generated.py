import pytest
from dataclasses_json.cfg import config, UndefinedParameterError
from marshmallow.fields import Field as MarshmallowField

def test_field_name_override_with_letter_case():
    # Define a simple letter case function that uppercases the input
    def upper_case(s: str) -> str:
        return s.upper()

    # Use config to set a field_name and a letter_case
    metadata = config(
        metadata={},
        field_name="my_field",
        letter_case=upper_case
    )

    # The resulting metadata should contain a 'letter_case' key
    assert "dataclasses_json" in metadata
    assert "letter_case" in metadata["dataclasses_json"]

    # The letter_case function should transform the field name to uppercase
    letter_case_func = metadata["dataclasses_json"]["letter_case"]
    assert letter_case_func(None) == "MY_FIELD"

def test_invalid_undefined_raises_error():
    # Passing an invalid undefined string should raise UndefinedParameterError
    with pytest.raises(UndefinedParameterError) as excinfo:
        config(undefined="nonexistent_action")

    # The error message should list the valid actions
    valid_actions = ["IGNORE", "FAIL", "DEFAULT"]
    for action in valid_actions:
        assert action in str(excinfo.value)

def test_exclude_function_is_stored_and_callable():
    # Define an exclude function that excludes fields starting with underscore
    def exclude_fn(field):
        return field.name.startswith("_")

    metadata = config(exclude=exclude_fn)

    # The exclude function should be stored in the metadata
    assert "exclude" in metadata["dataclasses_json"]
    stored_fn = metadata["dataclasses_json"]["exclude"]
    assert stored_fn is exclude_fn

    # Test that the function behaves as expected
    class DummyField:
        def __init__(self, name):
            self.name = name

    assert stored_fn(DummyField("_private")) is True
    assert stored_fn(DummyField("public")) is False
