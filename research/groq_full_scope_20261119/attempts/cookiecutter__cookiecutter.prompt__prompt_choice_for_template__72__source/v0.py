import pytest
from cookiecutter.prompt import prompt_choice_for_template

def test_no_input_returns_first_option(tmp_path):
    # Arrange: create a simple options dict
    options = {"option_a": {"description": "A"}, "option_b": {"description": "B"}}
    # Act: call with no_input=True
    result = prompt_choice_for_template("templates", options, no_input=True)
    # Assert: the first key is returned
    assert result == "option_a"

def test_no_input_with_empty_options_raises_index_error():
    # Arrange: empty options dict
    options = {}
    # Act & Assert: accessing first element should raise IndexError
    with pytest.raises(IndexError):
        prompt_choice_for_template("templates", options, no_input=True)

def test_prompt_choice_for_template_without_no_input_raises_name_error():
    # Arrange: simple options dict
    options = {"opt1": {"desc": "desc"}}
    # Act & Assert: since read_user_choice is not defined, a NameError should be raised
    with pytest.raises(NameError):
        prompt_choice_for_template("templates", options, no_input=False)
