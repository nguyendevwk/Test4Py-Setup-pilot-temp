import inspect
import pytest
from docstring_parser.numpydoc import DeprecationSection
from docstring_parser.numpydoc.common import DocstringDeprecated

def test_parse_normal_deprecation_section():
    """Test that a normal deprecation section is parsed correctly."""
    section = DeprecationSection(title="Deprecated", key="deprecated")
    raw_text = "1.0\n    This function is deprecated and will be removed in future releases."
    # cleandoc removes indentation
    parsed = list(section.parse(raw_text))
    assert len(parsed) == 1
    dep = parsed[0]
    assert isinstance(dep, DocstringDeprecated)
    assert dep.args == ["deprecated"]
    assert dep.version == "1.0"
    assert dep.description == "This function is deprecated and will be removed in future releases."

def test_parse_deprecation_section_without_description():
    """Test that a deprecation section with only a version line yields None description."""
    section = DeprecationSection(title="Deprecated", key="deprecated")
    raw_text = "2.5\n"
    parsed = list(section.parse(raw_text))
    assert len(parsed) == 1
    dep = parsed[0]
    assert dep.args == ["deprecated"]
    assert dep.version == "2.5"
    assert dep.description is None

def test_parse_deprecation_section_with_multiple_lines():
    """Test that only the first line is taken as the version and the rest is cleaned as description."""
    section = DeprecationSection(title="Deprecated", key="deprecated")
    raw_text = "3.0\n    First line of description.\n    Second line of description."
    parsed = list(section.parse(raw_text))
    assert len(parsed) == 1
    dep = parsed[0]
    assert dep.version == "3.0"
    # inspect.cleandoc removes common indentation and leading/trailing whitespace
    expected_desc = "First line of description.\nSecond line of description."
    assert dep.description == expected_desc
