import pytest
from docstring_parser import parser
from docstring_parser.common import Docstring, DocstringStyle, RenderingStyle


def test_compose_includes_short_and_long_descriptions(tmp_path):
    """Compose should render both short and long descriptions."""
    doc = Docstring(
        short_description="Short",
        long_description="Long",
        docstring_style=DocstringStyle.GOOGLE,
    )
    rendered = parser.compose(doc, style=DocstringStyle.GOOGLE)
    assert isinstance(rendered, str)
    assert "Short" in rendered
    assert "Long" in rendered


def test_compose_style_auto_uses_docstring_style(tmp_path):
    """When style is AUTO, the function should use the docstring's style."""
    doc = Docstring(
        short_description="Short",
        long_description="Long",
        docstring_style=DocstringStyle.GOOGLE,
    )
    rendered_auto = parser.compose(doc, style=DocstringStyle.AUTO)
    rendered_google = parser.compose(doc, style=DocstringStyle.GOOGLE)
    assert rendered_auto == rendered_google


def test_compose_invalid_style_raises_key_error(tmp_path):
    """Passing an invalid style should raise a KeyError."""
    doc = Docstring(
        short_description="Short",
        long_description="Long",
        docstring_style=None,  # No style set
    )
    with pytest.raises(KeyError):
        parser.compose(doc, style=DocstringStyle.AUTO)
