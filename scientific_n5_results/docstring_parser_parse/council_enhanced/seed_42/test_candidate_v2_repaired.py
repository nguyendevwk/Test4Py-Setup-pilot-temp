import pytest
from docstring_parser.parser import parse
from docstring_parser.common import Docstring, DocstringStyle

sample_doc = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""

@pytest.mark.parametrize(
    "style,expected_style,raises",
    [
        (None, DocstringStyle.GOOGLE, None),
        ("google", DocstringStyle.GOOGLE, None),
        (DocstringStyle.GOOGLE, DocstringStyle.GOOGLE, None),
        ("invalid", None, ValueError),
    ],
)
def test_parse_behavior(style, expected_style, raises):
    if raises:
        with pytest.raises(raises):
            parse(sample_doc, style=style)
    else:
        result = parse(sample_doc, style=style)
        assert isinstance(result, Docstring)
        assert result.style == expected_style
