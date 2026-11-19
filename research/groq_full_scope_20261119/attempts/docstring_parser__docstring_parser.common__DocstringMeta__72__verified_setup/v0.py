import pytest
from docstring_parser.common import DocstringMeta


def test_init_with_valid_args_and_description():
    """DocstringMeta stores provided args and description correctly."""
    args = ["arg1", "arg2"]
    description = "This is a test description."
    meta = DocstringMeta(args, description)

    assert meta.args == args
    assert meta.description == description
    assert isinstance(meta.args, list)
    assert isinstance(meta.description, str)


def test_init_with_none_description():
    """DocstringMeta accepts None as description and stores it."""
    args = ["param"]
    meta = DocstringMeta(args, None)

    assert meta.args == args
    assert meta.description is None


def test_init_with_empty_args():
    """DocstringMeta handles an empty args list without error."""
    meta = DocstringMeta([], "Empty args list")

    assert meta.args == []
    assert meta.description == "Empty args list"
