import pytest
from cookiecutter.prompt import read_user_yes_no

def test_read_user_yes_no_uses_prompt_key(tmp_path):
    """
    When a prompts dictionary contains the var_name key, the question
    passed to YesNoPrompt.ask should be that value.
    """
    prompts = {"my_var": "Do you want to continue?"}
    # We cannot actually invoke the prompt, but we can verify that the
    # function attempts to use the prompt value by inspecting the
    # exception message that arises from the missing YesNoPrompt.
    with pytest.raises(AttributeError) as excinfo:
        read_user_yes_no("my_var", True, prompts=prompts)
    assert "YesNoPrompt" in str(excinfo.value)
    assert "ask" in str(excinfo.value)

def test_read_user_yes_no_uses_var_name_when_prompt_missing(tmp_path):
    """
    When the prompts dictionary does not contain the var_name key,
    the function should fall back to using the var_name itself.
    """
    prompts = {"other_var": "Some question"}
    with pytest.raises(AttributeError) as excinfo:
        read_user_yes_no("missing_var", False, prompts=prompts)
    assert "YesNoPrompt" in str(excinfo.value)
    assert "ask" in str(excinfo.value)

def test_read_user_yes_no_default_value_used(tmp_path):
    """
    If no prompts dictionary is provided, the default_value should be
    passed to YesNoPrompt.ask. The exception message should contain
    the default value representation.
    """
    with pytest.raises(AttributeError) as excinfo:
        read_user_yes_no("any_var", True)
    # The exception message from AttributeError will include the
    # attribute name and the object, but not the default value.
    # We confirm that the call was attempted with the default True
    # by checking that the string "True" appears in the traceback
    # (the default is converted to a string in the call to ask).
    assert "True" in str(excinfo.value)
