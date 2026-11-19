import re
import inspect
import pytest
from docstring_parser.numpydoc import Section
from docstring_parser.numpydoc.common import DocstringMeta

def test_section_title_pattern_matches_and_does_not_match_wrong():
    """The title_pattern should match the exact header format and reject variations."""
    sec = Section("Parameters", "parameters")
    pattern = sec.title_pattern
    # Correct header: title on one line, underline of same length on next line
    header = "Parameters\n----------"
    assert re.match(pattern, header)
    # Header with extra spaces after underline should not match
    bad_header = "Parameters\n----------   "
    assert not re.match(pattern, bad_header)
    # Header with different title should not match
    assert not re.match(pattern, "Returns\n-------")

def test_section_parse_returns_docstringmeta_with_cleaned_description():
    """Parsing should yield a DocstringMeta with the key and cleaned description."""
    sec = Section("Returns", "returns")
    raw_text = "   This function returns a value.\n\n   It may raise errors."
    cleaned = inspect.cleandoc(raw_text)
    meta_iter = sec.parse(cleaned)
    meta_list = list(meta_iter)
    assert len(meta_list) == 1
    meta = meta_list[0]
    assert isinstance(meta, DocstringMeta)
    assert meta.args == ["returns"]
    # The description should be cleaned: leading/trailing whitespace removed, internal
    # blank lines preserved as single newlines
    expected_description = "This function returns a value.\n\nIt may raise errors."
    assert meta.description == expected_description

def test_section_parse_with_empty_body_returns_empty_description():
    """Parsing an empty section body should produce a DocstringMeta with an empty description."""
    sec = Section("Notes", "notes")
    empty_text = ""
    meta_iter = sec.parse(empty_text)
    meta_list = list(meta_iter)
    assert len(meta_list) == 1
    meta = meta_list[0]
    assert meta.args == ["notes"]
    assert meta.description == ""
