import inspect
import pytest
from docstring_parser.numpydoc import DeprecationSection
from docstring_parser.common import DocstringDeprecated


def test_parse_normal_section():
    """Test parsing a typical deprecation section with version and description."""
    section = DeprecationSection(title="Deprecation", key="deprecated")
    text = """\
    1.0
    This function is deprecated and will be removed in future releases.
    """
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert isinstance(dep, DocstringDeprecated)
    assert dep.args == ["deprecated"]
    assert dep.version == "1.0"
    assert dep.description == "This function is deprecated and will be removed in future releases."


def test_parse_single_line_section():
    """Test parsing a deprecation section that contains only a version line."""
    section = DeprecationSection(title="Deprecation", key="deprecated")
    text = "2.5"
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert dep.args == ["deprecated"]
    assert dep.version == "2.5"
    assert dep.description is None


def test_parse_empty_section():
    """Test parsing an empty deprecation section."""
    section = DeprecationSection(title="Deprecation", key="deprecated")
    text = ""
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert dep.args == ["deprecated"]
    assert dep.version == ""
    assert dep.description is None
