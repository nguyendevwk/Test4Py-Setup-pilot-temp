import pytest
import inspect
from docstring_parser import parser, epydoc, google, numpydoc, rest
from docstring_parser.common import DocstringStyle, RenderingStyle, ParseError

# Helper function to parse a docstring from a function
def get_parsed_docstring(func, style=DocstringStyle.AUTO):
    return parser.parse(inspect.getsource(func), style=style)

# 1. Normal rendering with default style and compact rendering
def test_compose_default_style_and_rendering():
    def sample_func(a, b):
        """
        :param a: first argument
        :type a: int
        :param b: second argument
        :type b: str
        :return: result
        :rtype: bool
        """
        return True

    parsed = get_parsed_docstring(sample_func)
    composed = parser.compose(parsed)
    # The composed string should contain the original tags in the same order
    assert ":param a:" in composed
    assert ":type a:" in composed
    assert ":param b:" in composed
    assert ":type b:" in composed
    assert ":return:" in composed
    assert ":rtype:" in composed
    # Compact rendering should not add extra blank lines
    assert "\n\n" not in composed

# 2. Rendering with explicit style override (google) and expanded rendering
def test_compose_explicit_google_style_and_expanded_rendering():
    def sample_func(x, y):
        """
        Args:
            x (int): first value
            y (str): second value

        Returns:
            bool: description
        """
        return False

    parsed = get_parsed_docstring(sample_func, style=DocstringStyle.GOOGLE)
    composed = parser.compose(parsed, style=DocstringStyle.GOOGLE, rendering_style=RenderingStyle.EXPANDED)
    # Expanded rendering should include a blank line after the description
    assert "\n\n" in composed
    # Google style tags should be present
    assert "Args:" in composed
    assert "Returns:" in composed
    # Ensure the tags are correctly formatted
    assert "x (int):" in composed
    assert "y (str):" in composed
    assert "bool:" in composed

# 3. Error handling: passing an invalid docstring object should raise TypeError
def test_compose_invalid_docstring_raises_type_error():
    with pytest.raises(TypeError):
        parser.compose(None)
