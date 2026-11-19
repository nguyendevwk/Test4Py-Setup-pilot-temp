import pytest
from docstring_parser.parser import parse, DocstringStyle, BaseParser
from docstring_parser.common import Docstring
from docstring_parser.google_parser import GoogleParser

SAMPLE_DOC = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""

def test_parse_google_and_base_parser_behavior():
    # Parse with explicit Google style string
    doc_google = parse(SAMPLE_DOC, style="google")
    assert isinstance(doc_google, Docstring)
    assert doc_google.style == DocstringStyle.GOOGLE

    # Retrieve a concrete parser instance for Google style
    google_parser = GoogleParser()
    doc_from_parser = parse(SAMPLE_DOC, style=google_parser)
    assert isinstance(doc_from_parser, Docstring)
    assert doc_from_parser.style == DocstringStyle.GOOGLE

    # Passing sections with a BaseParser instance should raise ValueError
    with pytest.raises(ValueError):
        parse(SAMPLE_DOC, style=google_parser, sections=[])
