import inspect
import pytest
from docstring_parser.numpydoc import DeprecationSection
from docstring_parser.common import DocstringDeprecated

def test_parse_normal_section():
    """Test parsing a typical deprecation section with version and description."""
    section = DeprecationSection(title="Deprecation", key="deprecated")
    text = "1.0\n    This feature is deprecated.\n    Use new_feature instead."
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert isinstance(dep, DocstringDeprecated)
    assert dep.args == ["deprecated"]
    assert dep.version == "1.0"
    # inspect.cleandoc removes indentation and trailing newlines
    assert dep.description == "This feature is deprecated.\nUse new_feature instead."

def test_parse_no_description():
    """Test parsing when only a version line is present (no description)."""
    section = DeprecationSection(title="Deprecation", key="deprecated")
    text = "2.5\n"
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert dep.args == ["deprecated"]
    assert dep.version == "2.5"
    assert dep.description is None

def test_parse_whitespace_and_empty_lines():
    """Test that leading/trailing whitespace and empty lines are cleaned correctly."""
    section = DeprecationSection(title="Deprecation", key="deprecated")
    text = "   3.1   \n\n    \n   Deprecated due to security issues.   \n"
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert dep.version == "3.1"
    # description should be cleaned of leading/trailing whitespace and empty lines
    assert dep.description == "Deprecated due to security issues."
