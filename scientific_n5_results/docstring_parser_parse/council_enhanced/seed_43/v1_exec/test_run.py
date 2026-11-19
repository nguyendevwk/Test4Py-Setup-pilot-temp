import pytest
from docstring_parser.parser import parse, DocstringStyle
from docstring_parser.parsers import BaseParser
from docstring_parser.common import Docstring


def test_parse_behavior():
    text = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""
    # Dummy parser that returns a Docstring with a known style
    class DummyParser(BaseParser):
        def parse(self, txt: str) -> Docstring:
            return Docstring(style=DocstringStyle.GOOGLE)

    dummy = DummyParser()

    # 1. Passing a parser instance returns its result
    result = parse(text, style=dummy)
    assert isinstance(result, Docstring)
    assert result.style == DocstringStyle.GOOGLE

    # 2. Passing sections with a parser instance raises ValueError
    with pytest.raises(ValueError):
        parse(text, style=dummy, sections=[("param", "name")])

    # 3. Passing a style name string is converted to DocstringStyle
    result_str = parse(text, style="google")
    assert isinstance(result_str, Docstring)
    assert result_str.style == DocstringStyle.GOOGLE
    assert result_str.short_description == "Summary line."
    assert len(result_str.params) == 1
    assert result_str.params[0].arg_name == "name"
    assert result_str.params[0].description == "param desc"

    # 4. Passing a DocstringStyle enum directly yields the same result
    result_enum = parse(text, style=DocstringStyle.GOOGLE)
    assert result_enum.style == DocstringStyle.GOOGLE
    assert result_enum.short_description == "Summary line."
    assert len(result_enum.params) == 1
    assert result_enum.params[0].arg_name == "name"
    assert result_enum.params[0].description == "param desc"
