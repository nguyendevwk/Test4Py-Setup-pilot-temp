import pytest
from docstring_parser.parser import parse, DocstringStyle, BaseParser
from docstring_parser.common import Docstring


class DummyParser(BaseParser):
    """A minimal BaseParser implementation for testing."""

    def parse(self, text: str) -> Docstring:
        doc = Docstring(style=DocstringStyle.GOOGLE)
        doc.short_description = "dummy"
        return doc


def test_parse_behavior():
    # 1. BaseParser instance path
    dummy = DummyParser()
    doc = parse("any text", style=dummy)
    assert isinstance(doc, Docstring)
    assert doc.style == DocstringStyle.GOOGLE
    assert doc.short_description == "dummy"

    # 2. Passing sections with a BaseParser should raise ValueError
    with pytest.raises(ValueError):
        parse("any text", style=dummy, sections=[("section", "type")])

    # 3. Style specified as a string should be converted to DocstringStyle
    doc_str = parse("any text", style="google")
    assert isinstance(doc_str, Docstring)
    assert doc_str.style == DocstringStyle.GOOGLE

    # 4. AUTO style with no sections should still return a Docstring
    doc_auto = parse("any text", style=DocstringStyle.AUTO)
    assert isinstance(doc_auto, Docstring)
