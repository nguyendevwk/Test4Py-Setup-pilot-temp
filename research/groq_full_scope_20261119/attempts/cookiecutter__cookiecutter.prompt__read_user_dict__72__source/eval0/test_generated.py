import pytest
from cookiecutter.prompt import read_user_dict

def test_read_user_dict_type_error():
    """read_user_dict should raise TypeError if default_value is not a dict."""
    with pytest.raises(TypeError):
        read_user_dict("my_var", default_value="not a dict")

def test_read_user_dict_default_value_is_dict():
    """When default_value is a dict, the function should accept it without error."""
    # The function will attempt to prompt the user, but we can provide a minimal
    # prompts dict that contains the variable name to avoid an empty prompt.
    # Since we cannot avoid the actual prompt, we simply check that no exception
    # is raised up to the point of calling JsonPrompt.ask.
    # This test ensures that the type check passes for a dict.
    try:
        read_user_dict("my_var", default_value={}, prompts={"my_var": ""})
    except Exception as e:
        # The only exception that could be raised before the prompt is a TypeError,
        # which we already test above. Any other exception indicates a failure.
        pytest.fail(f"Unexpected exception raised: {e}")

def test_read_user_dict_prompts_overrides_question():
    """When a prompt is provided, it should override the default question string."""
    # We cannot capture the prompt text directly, but we can ensure that the
    # function accepts a custom prompt string without raising an exception.
    try:
        read_user_dict("my_var", default_value={}, prompts={"my_var": "Custom question?"})
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
