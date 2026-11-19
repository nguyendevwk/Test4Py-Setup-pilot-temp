import pytest
from docstring_parser.parser import parse, DocstringStyle, BaseParser, Docstring


def test_parse_behavior_with_parser_and_style_and_error():
    # Sample docstring that matches Google style
    sample_doc = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""

    # Dummy parser that always returns a Docstring with Google style
    class DummyParser(BaseParser):
        def parse(self, text: str) -> Docstring:
            return Docstring(style=DocstringStyle.GOOGLE)

    dummy_parser = DummyParser()

    # 1. When style is a BaseParser instance, parse should delegate to it
    result_from_parser = parse(sample_doc, style=dummy_parser)
    assert isinstance(result_from_parser, Docstring)
    assert result_from_parser.style is DocstringStyle.GOOGLE

    # 2. When style is a string name, parse should resolve to the correct style
    result_from_string = parse(sample_doc, style="google")
    assert isinstance(result_from_string, Docstring)
    assert result_from_string.style is DocstringStyle.GOOGLE

    # 3. Passing sections with a BaseParser instance should raise ValueError
    with pytest.raises(ValueError, match="A parser has its sections"):
        parse(sample_doc, style=dummy_parser, sections=[("param", "name", "desc")])
