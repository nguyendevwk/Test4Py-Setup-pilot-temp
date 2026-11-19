import inspect
import re
import pytest
from docstring_parser.numpydoc import Section
from docstring_parser.common import DocstringMeta

def test_title_pattern_matches_header():
    """The title_pattern should match a header consisting of the title and a line of dashes."""
    sec = Section("Parameters", "parameters")
    pattern = sec.title_pattern
    header = "Parameters\n----------\n"
    assert re.match(pattern, header) is not None
    # Ensure the captured group is the title
    match = re.match(pattern, header)
    assert match.group(1) == "Parameters"

def test_parse_returns_cleaned_description():
    """parse should yield a DocstringMeta with the cleaned description."""
    sec = Section("Returns", "returns")
    raw = "   This function returns a value.\n\n    It can be None."
    cleaned = inspect.cleandoc(raw)
    meta_iter = sec.parse(raw)
    meta = next(meta_iter)
    assert isinstance(meta, DocstringMeta)
    assert meta.args == ["returns"]
    # The description should be cleaned (no leading indentation, no trailing newlines)
    assert meta.description == cleaned
    # No more items
    with pytest.raises(StopIteration):
        next(meta_iter)

def test_parse_raises_on_non_string_input():
    """parse should raise a TypeError when called with a non-string argument."""
    sec = Section("Examples", "examples")
    with pytest.raises(TypeError):
        # Passing an integer should trigger a TypeError because the function expects a string
        list(sec.parse(123))
