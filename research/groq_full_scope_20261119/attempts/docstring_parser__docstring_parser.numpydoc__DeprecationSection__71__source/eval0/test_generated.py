import inspect
import pytest
from docstring_parser.numpydoc import DeprecationSection
from docstring_parser.common import DocstringDeprecated

def test_parse_single_line_deprecation():
    section = DeprecationSection(key="deprecated")
    text = "1.0.0\n"
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert isinstance(dep, DocstringDeprecated)
    assert dep.args == ["deprecated"]
    assert dep.version == "1.0.0"
    assert dep.description is None

def test_parse_multi_line_description():
    section = DeprecationSection(key="deprecated")
    text = "2.0.0\n    This function is deprecated.\n    Use `new_func` instead."
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    assert dep.version == "2.0.0"
    expected_desc = "This function is deprecated.\nUse `new_func` instead."
    assert dep.description == expected_desc

def test_parse_with_extra_newlines_and_whitespace():
    section = DeprecationSection(key="deprecated")
    text = "3.1.4\n\n    First line.\n\n    Second line.\n\n"
    result = list(section.parse(text))
    assert len(result) == 1
    dep = result[0]
    expected_desc = "First line.\n\nSecond line."
    assert dep.description == expected_desc
    assert dep.version == "3.1.4"
