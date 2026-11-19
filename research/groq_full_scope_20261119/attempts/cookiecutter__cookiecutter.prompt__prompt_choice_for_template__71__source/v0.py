import pytest
from collections import OrderedDict
from cookiecutter.prompt import prompt_choice_for_template

def test_no_input_returns_first_option():
    options = {"alpha": {"description": "first"}, "beta": {"description": "second"}}
    result = prompt_choice_for_template("template", options, no_input=True)
    assert result == "alpha", "When no_input is True, the first key should be returned"

def test_empty_options_raises_index_error():
    options = {}
    with pytest.raises(IndexError):
        prompt_choice_for_template("template", options, no_input=True)

def test_options_order_is_preserved_in_return():
    # Use an OrderedDict to ensure insertion order
    options = OrderedDict([("first", {"desc": "1"}), ("second", {"desc": "2"}), ("third", {"desc": "3"})])
    result = prompt_choice_for_template("template", options, no_input=True)
    assert result == "first", "The function should return the first key in insertion order"
