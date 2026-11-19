import pytest
from cookiecutter.prompt import read_user_yes_no

def test_read_user_yes_no_raises_attribute_error():
    """read_user_yes_no should raise AttributeError because YesNoPrompt is undefined."""
    with pytest.raises(AttributeError):
        read_user_yes_no("var", True)

def test_read_user_yes_no_with_prompts_raises_attribute_error():
    """Providing a prompts dict still results in AttributeError."""
    prompts = {"var": "Do you want to continue?"}
    with pytest.raises(AttributeError):
        read_user_yes_no("var", False, prompts=prompts)

def test_read_user_yes_no_with_prefix_raises_attribute_error():
    """Adding a prefix does not change the AttributeError outcome."""
    with pytest.raises(AttributeError):
        read_user_yes_no("var", True, prefix=">>> ")
