import pytest
from docstring_parser.common import DocstringDeprecated, DocstringMeta

def test_deprecated_initialization_basic():
    """Verify that a DocstringDeprecated instance stores its arguments correctly."""
    args = ["param1", "param2"]
    description = "This is deprecated."
    version = "2.0"
    dep = DocstringDeprecated(args, description, version)
    assert isinstance(dep, DocstringDeprecated)
    assert isinstance(dep, DocstringMeta)
    assert dep.args == args
    assert dep.description == description
    assert dep.version == version

def test_deprecated_with_none_and_empty():
    """Test boundary conditions: empty args list and None values."""
    dep = DocstringDeprecated([], None, None)
    assert dep.args == []
    assert dep.description is None
    assert dep.version is None

def test_deprecated_attribute_overwrite():
    """Ensure that DocstringDeprecated correctly overwrites the description attribute."""
    base = DocstringMeta(["x"], "original")
    # Create a subclass instance that sets a different description
    dep = DocstringDeprecated(["x"], "new", "1.0")
    # The base description should not be the same as the subclass's
    assert dep.description == "new"
    assert dep.description != base.description
