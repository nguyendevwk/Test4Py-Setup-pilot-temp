import pytest
from docstring_parser.numpydoc import Section
from docstring_parser.numpydoc.common import DocstringMeta

def test_title_pattern_matches_and_non_matches():
    """Verify that the title_pattern correctly matches the header and rejects wrong forms."""
    sec = Section("Parameters", "parameters")
    pattern = sec.title_pattern
    # Correct header: title followed by underline of same length
    assert pattern == r"^(Parameters)\s*?\n----------\s*$"
    # The regex should match the exact header
    assert re.match(pattern, "Parameters\n----------") is not None
    # It should not match if the underline length differs
    assert re.match(pattern, "Parameters\n-----") is None
    # It should not match if the title is different
    assert re.match(pattern, "Returns\n-------") is None

def test_parse_returns_docstringmeta_with_cleaned_description():
    """Ensure parse yields a DocstringMeta with cleaned description."""
    sec = Section("Returns", "returns")
    raw_text = "   This function returns a value.\n   It may be None.\n"
    # The parse method expects cleaned text; we simulate that by passing raw_text directly
    result = list(sec.parse(raw_text))
    assert len(result) == 1
    meta = result[0]
    assert isinstance(meta, DocstringMeta)
    # The description should be stripped of leading/trailing whitespace
    assert meta.args == ["returns"]
    assert meta.description == "This function returns a value.\nIt may be None."

def test_parse_empty_text_returns_none_description():
    """When the section body is empty or whitespace, description should be None."""
    sec = Section("Notes", "notes")
    empty_text = "   \n   "
    result = list(sec.parse(empty_text))
    assert len(result) == 1
    meta = result[0]
    assert meta.description is None
