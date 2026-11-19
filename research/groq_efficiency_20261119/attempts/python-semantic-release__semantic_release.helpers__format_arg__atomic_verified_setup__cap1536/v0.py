import pytest
from semantic_release.helpers import format_arg


def test_format_arg_normal():
    """Normal string input should be quoted and stripped."""
    assert format_arg("hello") == "'hello'"
    assert format_arg("  world  ") == "'world'"


def test_format_arg_boundary():
    """Boundary cases: empty string, non-string types, and subclass of str."""
    # Empty string should be quoted as ''
    assert format_arg("") == "''"

    # Non-string types are converted via str()
    assert format_arg(123) == "123"
    assert format_arg([1, 2]) == "[1, 2]"

    # Subclass of str is not treated as str due to type check
    class MyStr(str):
        pass

    assert format_arg(MyStr("sub")) == "sub"  # no quotes


def test_format_arg_error():
    """Ensure that unexpected types do not raise exceptions."""
    # Passing a complex object should still return its string representation
    class Dummy:
        def __repr__(self):
            return "<DummyObject>"

    dummy = Dummy()
    assert format_arg(dummy) == "<DummyObject>"
