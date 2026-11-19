import builtins
import importlib
import types
import pytest

# Import the target module
cookiecutter_prompt = importlib.import_module("cookiecutter.prompt")

def test_read_user_yes_no_uses_prompt_and_default(tmp_path):
    # Prepare a dummy YesNoPrompt with an ask method that records its arguments
    class DummyPrompt:
        def __init__(self):
            self.called_with = None
        def ask(self, question, default):
            self.called_with = (question, default)
            return True  # simulate user answering "yes"

    dummy = DummyPrompt()
    # Inject the dummy into the module namespace
    setattr(cookiecutter_prompt, "YesNoPrompt", dummy)

    # Call the function with a prompt dict
    result = cookiecutter_prompt.read_user_yes_no(
        var_name="test_var",
        default_value=False,
        prompts={"test_var": "Do you agree?"},
        prefix=">>> "
    )
    # Assert that the function returned the dummy's return value
    assert result is True
    # Assert that the question was constructed correctly
    assert dummy.called_with == (">>> Do you agree?", False)

def test_read_user_yes_no_uses_var_name_as_question_when_prompt_missing(tmp_path):
    # Prepare a dummy YesNoPrompt that simply returns the default value
    class DummyPrompt:
        def ask(self, question, default):
            return default

    dummy = DummyPrompt()
    setattr(cookiecutter_prompt, "YesNoPrompt", dummy)

    # Call the function without providing a prompt for the variable
    result = cookiecutter_prompt.read_user_yes_no(
        var_name="missing_prompt",
        default_value=True,
        prompts={},  # empty dict
        prefix=""
    )
    # The function should return the default value
    assert result is True

def test_read_user_yes_no_raises_name_error_when_prompt_missing(tmp_path):
    # Ensure YesNoPrompt is not defined in the module
    if hasattr(cookiecutter_prompt, "YesNoPrompt"):
        delattr(cookiecutter_prompt, "YesNoPrompt")

    # Calling the function should raise NameError because YesNoPrompt is undefined
    with pytest.raises(NameError):
        cookiecutter_prompt.read_user_yes_no(
            var_name="any_var",
            default_value=False,
            prompts={"any_var": "Question?"}
        )
