import pytest
from docstring_parser.parser import compose
from docstring_parser.common import Docstring, DocstringStyle, RenderingStyle


def test_compose_google_style_compact(tmp_path):
    """Compose a simple Google‑style docstring with compact rendering."""
    raw = """\
    This function does something.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: The result.
    """
    doc = Docstring(raw, style=DocstringStyle.GOOGLE)
    rendered = compose(doc, style=DocstringStyle.GOOGLE, rendering_style=RenderingStyle.COMPACT)
    # The compact rendering should preserve the original formatting
    assert rendered.strip() == raw.strip()
    # The summary line must be present
    assert "This function does something." in rendered


def test_compose_numpy_style_expanded(tmp_path):
    """Compose a NumPy‑style docstring with expanded rendering."""
    raw = """\
    Computes the sum of two numbers.

    Parameters
    ----------
    a : int
        First number.
    b : int
        Second number.

    Returns
    -------
    int
        Sum of a and b.
    """
    doc = Docstring(raw, style=DocstringStyle.NUMPYDOC)
    rendered = compose(doc, style=DocstringStyle.NUMPYDOC, rendering_style=RenderingStyle.EXPANDED)
    # Expanded rendering should include section headers
    assert "Parameters" in rendered
    assert "Returns" in rendered
    # The summary line must be present
    assert "Computes the sum of two numbers." in rendered


def test_compose_invalid_input_raises_type_error():
    """Passing a non‑Docstring instance should raise a TypeError."""
    with pytest.raises(TypeError):
        compose(123, style=DocstringStyle.AUTO, rendering_style=RenderingStyle.COMPACT)
