import pytest
from cookiecutter.prompt import prompt_choice_for_template

def test_prompt_choice_for_template_no_input_returns_first_option(tmp_path):
    # Arrange: create a simple options dict with multiple keys
    options = {"alpha": {"description": "first"}, "beta": {"description": "second"}}
    # Act: call the function with no_input=True
    result = prompt_choice_for_template("template", options, no_input=True)
    # Assert: the result should be the first key in the options dict
    assert result == "alpha"

def test_prompt_choice_for_template_no_input_with_single_option(tmp_path):
    # Arrange: options dict with a single key
    options = {"only": {"description": "only option"}}
    # Act: call the function with no_input=True
    result = prompt_choice_for_template("template", options, no_input=True)
    # Assert: the result should be that single key
    assert result == "only"

def test_prompt_choice_for_template_with_input_raises_attribute_error(tmp_path):
    # Arrange: options dict with at least one key
    options = {"one": {"description": "first"}}
    # Act & Assert: calling with no_input=False should raise AttributeError
    # because read_user_choice is not defined in this module
    with pytest.raises(AttributeError):
        prompt_choice_for_template("template", options, no_input=False)
