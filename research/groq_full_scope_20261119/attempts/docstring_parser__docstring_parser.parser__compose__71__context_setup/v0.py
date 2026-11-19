import pytest
from docstring_parser import parser
from docstring_parser.common import DocstringStyle, RenderingStyle, ParseError
from docstring_parser import epydoc, google, numpydoc, rest
from docstring_parser.attrdoc import add_attribute_docstrings

# Helper function to create a simple function with a Google‑style docstring
def _make_func_with_google_docstring():
    def sample(a, b):
        """
        Short description.

        Args:
            a (int): First argument.
            b (int): Second argument.

        Returns:
            int: Sum of a and b.
        """
        return a + b
    return sample

# Helper function to create a function with an empty docstring
def _make_func_with_empty_docstring():
    def empty():
        """ """
        return None
    return empty

def test_compose_google_style_renders_expected_output(tmp_path):
    """Test that compose renders a Google‑style docstring correctly."""
    func = _make_func_with_google_docstring()
    # Parse the function's docstring
    parsed = parser.parse(func)
    # Compose the docstring back to text
    rendered = parser.compose(parsed, style=DocstringStyle.GOOGLE, rendering_style=RenderingStyle.COMPACT, indent="    ")
    # The rendered output should contain the original description and sections
    assert "Short description." in rendered
    assert "Args:" in rendered
    assert "a (int): First argument." in rendered
    assert "b (int): Second argument." in rendered
    assert "Returns:" in rendered
    assert "int: Sum of a and b." in rendered
    # The indentation should be exactly four spaces
    assert rendered.startswith("    Short description.")

def test_compose_empty_docstring_returns_empty_string(tmp_path):
    """Test that compose returns an empty string for an empty docstring."""
    func = _make_func_with_empty_docstring()
    parsed = parser.parse(func)
    rendered = parser.compose(parsed, style=DocstringStyle.AUTO, rendering_style=RenderingStyle.COMPACT, indent="    ")
    # An empty docstring should result in an empty string
    assert rendered == ""

def test_compose_invalid_style_raises_key_error(tmp_path):
    """Test that passing an unsupported style raises a KeyError."""
    func = _make_func_with_google_docstring()
    parsed = parser.parse(func)
    # Use an invalid style value that is not in the _STYLE_MAP
    class FakeStyle:
        pass
    with pytest.raises(KeyError):
        parser.compose(parsed, style=FakeStyle, rendering_style=RenderingStyle.COMPACT, indent="    ")
