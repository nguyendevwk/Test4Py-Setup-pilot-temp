import inspect
import pytest
from docstring_parser.numpydoc import DeprecationSection
from docstring_parser.common import DocstringDeprecated

def test_parse_single_line_deprecation():
    """Test parsing of a simple deprecation section with only a version line."""
    section = DeprecationSection()
    text = "1.0.0"
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert isinstance(dep, DocstringDeprecated)
    assert dep.args == ["deprecation"]
    assert dep.description is None
    assert dep.version == "1.0.0"

def test_parse_multi_line_deprecation():
    """Test parsing of a deprecation section with a version and a multi‑line description."""
    section = DeprecationSection()
    text = """2.1.3
    This function is deprecated.
    Use `new_func` instead."""
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert dep.args == ["deprecation"]
    assert dep.description == "This function is deprecated.\nUse `new_func` instead."
    assert dep.version == "2.1.3"

def test_parse_with_extra_newlines_and_whitespace():
    """Test that leading/trailing whitespace and empty lines are ignored correctly."""
    section = DeprecationSection()
    text = """
    3.0.0

    Deprecated due to performance issues.

    """
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    # The description should be cleaned of leading/trailing blank lines
    assert dep.description == "Deprecated due to performance issues."
    assert dep.version == "3.0.0"
