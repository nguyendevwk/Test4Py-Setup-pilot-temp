import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring


def test_parse_google_style_docstring_parsing_and_sections():
    # Normal Google‑style docstring with short, long, Args and Returns sections
    text = """Short summary line.

Long description line 1.
Long description line 2.

Args:
    param1 (int): description.

Returns:
    bool: True if successful.
"""
    doc = parse(text)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short summary line."
    assert doc.long_description == "Long description line 1.\nLong description line 2."
    assert doc.blank_after_short_description is True
    assert doc.blank_after_long_description is False
    assert doc.description == (
        "Short summary line.\n\nLong description line 1.\nLong description line 2."
    )
    assert len(doc.params) == 1
    assert doc.params_by_name["param1"].arg_name == "param1"

    # When no sections are recognised, params should be empty
    doc_no_sections = parse(text, sections=())
    assert len(doc_no_sections.params) == 0

    # Parsing None or an empty string yields a Docstring with no description
    doc_none = parse(None)
    assert doc_none.description is None
    doc_empty = parse("")
    assert doc_empty.description is None
