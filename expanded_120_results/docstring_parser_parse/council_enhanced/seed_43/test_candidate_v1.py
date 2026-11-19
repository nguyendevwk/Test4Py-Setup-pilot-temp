import pytest
from docstring_parser.parser import parse, DocstringStyle, BaseParser
from docstring_parser.common import Docstring

SAMPLE_DOC = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""

class DummyParser(BaseParser):
    """Parser that returns a pre‑created Docstring instance."""
    def __init__(self, doc: Docstring):
        self._doc = doc

    def parse(self, text: str) -> Docstring:
        # Return the same instance regardless of input
        return self._doc

def test_parse_with_base_parser_behavior():
    # Prepare a Docstring that the dummy parser will return
    dummy_doc = Docstring(style=DocstringStyle.GOOGLE)
    dummy_parser = DummyParser(dummy_doc)

    # When a BaseParser instance is supplied, parse should delegate to it
    result = parse(SAMPLE_DOC, style=dummy_parser)
    assert result is dummy_doc
    assert result.style == DocstringStyle.GOOGLE

    # Supplying sections with a BaseParser should raise ValueError
    with pytest.raises(ValueError, match="A parser has its sections"):
        parse(SAMPLE_DOC, style=dummy_parser, sections=["param"])
