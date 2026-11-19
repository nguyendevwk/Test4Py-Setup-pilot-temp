import inspect
import pytest
from docstring_parser.numpydoc import DeprecationSection
from docstring_parser.numpydoc.common import DocstringDeprecated

def test_parse_normal_deprecation_section():
    """Verify that a typical deprecation section is parsed correctly."""
    section = DeprecationSection(title="deprecation", key="deprecated")
    raw_text = """1.0
    This function is deprecated because it is slow."""
    # The parser expects the body to be already cleaned by inspect.cleandoc
    cleaned = inspect.cleandoc(raw_text)
    result = list(section.parse(cleaned))
    assert len(result) == 1
    dep = result[0]
    assert isinstance(dep, DocstringDeprecated)
    assert dep.args == ["deprecated"]
    assert dep.version == "1.0"
    assert dep.description == "This function is deprecated because it is slow."

def test_parse_deprecation_section_no_description():
    """When the description is missing, the parser should return None for it."""
    section = DeprecationSection(title="deprecation", key="deprecated")
    raw_text = "2.0\n"
    cleaned = inspect.cleandoc(raw_text)
    result = list(section.parse(cleaned))
    assert len(result) == 1
    dep = result[0]
    assert dep.description is None
    assert dep.version == "2.0"

def test_parse_deprecation_section_multiple_lines_description():
    """The parser should correctly handle multi‑line descriptions."""
    section = DeprecationSection(title="deprecation", key="deprecated")
    raw_text = """3.5
    First line of the deprecation notice.
    Second line continues the message."""
    cleaned = inspect.cleandoc(raw_text)
    result = list(section.parse(cleaned))
    assert len(result) == 1
    dep = result[0]
    expected_desc = "First line of the deprecation notice.\nSecond line continues the message."
    assert dep.description == expected_desc
    assert dep.version == "3.5"
