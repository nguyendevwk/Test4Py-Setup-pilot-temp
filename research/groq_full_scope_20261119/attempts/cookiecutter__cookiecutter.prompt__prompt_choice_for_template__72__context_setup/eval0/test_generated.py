import pytest
from collections import OrderedDict
from cookiecutter.prompt import (
    prompt_choice_for_template,
    _prompts_from_options,
    read_user_choice,
)

def test_prompt_choice_for_template_no_input_returns_first(tmp_path):
    # Arrange: create a simple options dict
    options = {
        "template_a": {"title": "A", "description": "Desc A"},
        "template_b": {"title": "B", "description": "Desc B"},
    }
    # Act: call with no_input=True
    result = prompt_choice_for_template("templates", options, no_input=True)
    # Assert: the first key is returned
    assert result == "template_a"

def test_prompts_from_options_generates_expected_labels():
    # Arrange: options with varying title/description
    options = {
        "opt1": {"title": "Option 1", "description": "Option 1"},
        "opt2": {"title": "Option 2", "description": "Desc 2"},
        "opt3": {"title": "Option 3"},
    }
    # Act: generate prompts
    prompts = _prompts_from_options(options)
    # Assert: __prompt__ key exists
    assert "__prompt__" in prompts
    assert prompts["__prompt__"] == "Select a template"
    # Assert labels
    assert prompts["opt1"] == "Option 1"
    assert prompts["opt2"] == "Option 2 (Desc 2)"
    assert prompts["opt3"] == "Option 3"

def test_read_user_choice_raises_on_empty_options():
    # Arrange: empty options list
    options = []
    # Act & Assert: ValueError is raised
    with pytest.raises(ValueError):
        read_user_choice("var", options)
