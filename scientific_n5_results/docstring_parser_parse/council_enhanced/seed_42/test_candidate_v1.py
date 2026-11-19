import pytest
from docstring_parser.parser import parse
from docstring_parser.common import Docstring, DocstringStyle
from docstring_parser.parsers import BaseParser

sample_doc = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""

class DummyParser(BaseParser):
    def parse(self, text):
        return Docstring(style=DocstringStyle.GOOGLE)

@pytest.mark.parametrize(
    "style,sections,expected_style,raises",
    [
        (DummyParser(), None, DocstringStyle.GOOGLE, None),
        (DummyParser(), ["param"], None, ValueError),
        ("google", None, DocstringStyle.GOOGLE, None),
        (DocstringStyle.GOOGLE, None, DocstringStyle.GOOGLE, None),
        ("invalid", None, None, ValueError),
    ],
)
def test_parse_behavior(style, sections, expected_style, raises):
    if raises:
        with pytest.raises(raises):
            parse(sample_doc, style=style, sections=sections)
    else:
        result = parse(sample_doc, style=style, sections=sections)
        assert isinstance(result, Docstring)
        assert result.style == expected_style
