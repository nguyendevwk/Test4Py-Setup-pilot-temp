import pytest
from docstring_parser.common import DocstringDeprecated


def test_init_sets_attributes():
    """DocstringDeprecated should store args, description, and version correctly."""
    args = ["param1", "param2"]
    description = "Deprecated because of new API."
    version = "2.0"
    dep = DocstringDeprecated(args, description, version)

    # The instance should expose the same values
    assert dep.args == args
    assert dep.description == description
    assert dep.version == version

    # The base class may store args in a different attribute; ensure it matches
    assert getattr(dep, "args", None) == args


def test_description_none_and_version_none():
    """Passing None for description and version should be preserved."""
    args = ["foo"]
    dep = DocstringDeprecated(args, None, None)

    assert dep.args == args
    assert dep.description is None
    assert dep.version is None


def test_empty_args_list():
    """An empty args list should be accepted and stored."""
    dep = DocstringDeprecated([], "No parameters", "1.5")

    assert dep.args == []
    assert dep.description == "No parameters"
    assert dep.version == "1.5"
