import pytest
from collections import OrderedDict

from cookiecutter.prompt import prompt_choice_for_template, read_user_choice


def test_prompt_choice_for_template_no_input_returns_first_option(tmp_path):
    """When no_input is True, the function should return the first key of options."""
    options = {"foo": {"title": "Foo"}, "bar": {"title": "Bar"}}
    result = prompt_choice_for_template("templates", options, no_input=True)
    assert result == "foo"


def test_read_user_choice_returns_first_option_when_no_input(tmp_path):
    """read_user_choice should return the first option when no user input is provided."""
    options = ["alpha", "beta", "gamma"]
    # The default choice is the first key in the OrderedDict created inside the function.
    result = read_user_choice("var", options, prompts=None, prefix="")
    assert result == "alpha"


def test_read_user_choice_raises_value_error_on_empty_options(tmp_path):
    """read_user_choice should raise ValueError if the options list is empty."""
    with pytest.raises(ValueError):
        read_user_choice("var", [], prompts=None, prefix="")
