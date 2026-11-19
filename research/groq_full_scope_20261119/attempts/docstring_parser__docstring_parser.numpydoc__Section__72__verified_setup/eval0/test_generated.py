import re
import pytest
from docstring_parser.numpydoc import Section
from docstring_parser.common import DocstringMeta

def test_title_pattern_matches_and_non_matches():
    """The title_pattern property should match the exact header format."""
    sec = Section("Parameters", "parameters")
    pattern = sec.title_pattern
    # Should match a correct header
    header = "Parameters\n----------"
    assert re.match(pattern, header)
    # Should not match if dashes are missing or title differs
    assert not re.match(pattern, "Parameters\n-----")
    assert not re.match(pattern, "Params\n-----")
    # Should not match if there is trailing whitespace after dashes
    assert not re.match(pattern, "Parameters\n----------   ")

def test_parse_returns_docstringmeta_with_cleaned_description():
    """parse should yield a DocstringMeta with the key and cleaned description."""
    sec = Section("Returns", "returns")
    raw_text = "   This function returns a value.\n   It may raise errors."
    # cleandoc would strip leading indentation; we simulate that
    cleaned = "This function returns a value.\nIt may raise errors."
    meta_iter = sec.parse(cleaned)
    meta = next(meta_iter)
    assert isinstance(meta, DocstringMeta)
    assert meta.args == ["returns"]
    assert meta.description == cleaned
    # No more items
    with pytest.raises(StopIteration):
        next(meta_iter)

def test_parse_with_empty_text_yields_empty_description():
    """When the section body is empty, description should be an empty string."""
    sec = Section("Notes", "notes")
    meta_iter = sec.parse("")
    meta = next(meta_iter)
    assert meta.args == ["notes"]
    assert meta.description == ""
    with pytest.raises(StopIteration):
        next(meta_iter)
