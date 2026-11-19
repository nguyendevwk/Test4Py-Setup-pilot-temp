import re
import inspect
import pytest
from docstring_parser.numpydoc import Section
from docstring_parser.common import DocstringMeta

def test_title_pattern_matches_and_non_matches():
    """Verify that the title_pattern correctly matches the section header
    and does not match unrelated text."""
    section = Section("Parameters", "parameters")
    pattern = section.title_pattern
    # The pattern should match the header exactly
    header = "Parameters\n----------"
    assert re.match(pattern, header)
    # It should not match if the underline length differs
    bad_header = "Parameters\n--------"
    assert not re.match(pattern, bad_header)
    # It should not match if the title is different
    other_header = "Returns\n-------"
    assert not re.match(pattern, other_header)

def test_parse_returns_docstringmeta_with_cleaned_description():
    """Ensure that parse yields a DocstringMeta with the key and cleaned
    description. The description should have leading/trailing whitespace
    removed and internal indentation collapsed."""
    section = Section("Returns", "returns")
    raw_text = """
        This function returns a value.

        The value is an integer.
    """
    cleaned = inspect.cleandoc(raw_text)
    meta_iter = section.parse(cleaned)
    meta = next(meta_iter)
    assert isinstance(meta, DocstringMeta)
    assert meta.args == ["returns"]
    # The description should be a single string with no leading/trailing
    # whitespace and internal indentation removed
    expected_description = "This function returns a value.\n\nThe value is an integer."
    assert meta.description == expected_description
    # No more items should be yielded
    with pytest.raises(StopIteration):
        next(meta_iter)

def test_parse_with_empty_body_returns_empty_description():
    """When the section body is empty, the description should be an empty
    string and no error should be raised."""
    section = Section("Notes", "notes")
    empty_text = ""
    meta_iter = section.parse(empty_text)
    meta = next(meta_iter)
    assert meta.args == ["notes"]
    assert meta.description == ""
    with pytest.raises(StopIteration):
        next(meta_iter)
