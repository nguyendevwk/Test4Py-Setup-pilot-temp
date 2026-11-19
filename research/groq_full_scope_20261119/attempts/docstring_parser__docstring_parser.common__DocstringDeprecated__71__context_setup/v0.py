import pytest
from docstring_parser.common import DocstringDeprecated, DocstringMeta

def test_deprecated_initialization_with_values():
    """Verify that DocstringDeprecated stores provided args, description, and version."""
    args = ["param1", "param2"]
    description = "This function is deprecated."
    version = "2.0"
    dep = DocstringDeprecated(args, description, version)
    # Check that the base class attributes are set correctly
    assert isinstance(dep, DocstringMeta)
    assert dep.args == args
    assert dep.description == description
    # Check that the subclass attribute is set correctly
    assert dep.version == version

def test_deprecated_initialization_with_none():
    """Verify that DocstringDeprecated handles None for description and version."""
    args = ["only_arg"]
    dep = DocstringDeprecated(args, None, None)
    assert dep.args == args
    assert dep.description is None
    assert dep.version is None

def test_deprecated_inheritance_and_type():
    """Ensure that DocstringDeprecated is a subclass of DocstringMeta and behaves as expected."""
    dep = DocstringDeprecated([], "desc", "1.0")
    # isinstance checks
    assert isinstance(dep, DocstringDeprecated)
    assert isinstance(dep, DocstringMeta)
    # Ensure that accessing base class attributes works
    assert dep.args == []
    assert dep.description == "desc"
    # Ensure that subclass attribute is accessible
    assert dep.version == "1.0"
