import pytest
from docstring_parser.parser import parse, DocstringStyle, BaseParser, Docstring


def test_parse_with_base_parser_and_style_string():
    # Dummy parser that returns a Docstring with a known style
    class DummyParser(BaseParser):
        def parse(self, text: str) -> Docstring:
            return Docstring(style=DocstringStyle.GOOGLE)

    dummy = DummyParser()

    # 1. Passing a BaseParser instance returns its parse result
    result = parse("any text", style=dummy)
    assert isinstance(result, Docstring)
    assert result.style == DocstringStyle.GOOGLE

    # 2. Providing sections with a BaseParser raises ValueError
    with pytest.raises(ValueError, match="A parser has its sections"):
        parse("any text", style=dummy, sections=["param"])

    # 3. Passing a style name string yields a Docstring with that style
    result_str = parse("any text", style="google")
    assert isinstance(result_str, Docstring)
    assert result_str.style == DocstringStyle.GOOGLE

    # 4. Passing a DocstringStyle enum yields the same style
    result_enum = parse("any text", style=DocstringStyle.GOOGLE)
    assert isinstance(result_enum, Docstring)
    assert result_enum.style == DocstringStyle.GOOGLE
