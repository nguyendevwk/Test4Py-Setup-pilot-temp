import inspect
import types
import pytest
from docstring_parser import epydoc, google, numpydoc, rest
from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError, Docstring

# --------------------------------------------------------------------------- #
# Test 1: Parsing a class with attribute docstrings
# --------------------------------------------------------------------------- #
def test_parse_class_attributes(tmp_path):
    # Define a class with a docstring and attribute docstrings
    class Sample:
        """Sample class docstring."""
        x: int = 1
        """Attribute x docstring."""
        y: str = "hello"
        """Attribute y docstring."""

    # Parse the class
    result: Docstring = parse_from_object(Sample, style=DocstringStyle.AUTO)

    # The class docstring should be parsed
    assert result.short_description == "Sample class docstring."

    # Attribute docstrings should be present
    attrs = {a.name: a for a in result.params}
    assert "x" in attrs
    assert attrs["x"].description == "Attribute x docstring."
    assert "y" in attrs
    assert attrs["y"].description == "Attribute y docstring."

# --------------------------------------------------------------------------- #
# Test 2: Parsing a module with attribute docstrings
# --------------------------------------------------------------------------- #
def test_parse_module_attributes(tmp_path):
    # Create a temporary module file with attribute docstrings
    module_code = '''
    """Module docstring."""
    a = 10
    """Attribute a docstring."""
    b = "world"
    """Attribute b docstring."""
    '''
    module_path = tmp_path / "mymodule.py"
    module_path.write_text(module_code)

    # Import the module dynamically
    import importlib.util
    spec = importlib.util.spec_from_file_location("mymodule", str(module_path))
    mymodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mymodule)

    # Parse the module
    result: Docstring = parse_from_object(mymodule, style=DocstringStyle.AUTO)

    # Module docstring should be parsed
    assert result.short_description == "Module docstring."

    # Attribute docstrings should be present
    attrs = {a.name: a for a in result.params}
    assert "a" in attrs
    assert attrs["a"].description == "Attribute a docstring."
    assert "b" in attrs
    assert attrs["b"].description == "Attribute b docstring."

# --------------------------------------------------------------------------- #
# Test 3: Error handling when the object's __doc__ is not a string
# --------------------------------------------------------------------------- #
def test_parse_error_on_non_string_doc():
    # Create an object with __doc__ set to an integer
    class BadDoc:
        __doc__ = 42  # non-string docstring

    # Parsing should raise a ParseError because the docstring is invalid
    with pytest.raises(ParseError):
        parse_from_object(BadDoc, style=DocstringStyle.AUTO)
