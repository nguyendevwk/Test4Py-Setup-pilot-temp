import inspect
import types
import pytest
from docstring_parser.parser import parse_from_object
from docstring_parser.common import Docstring, DocstringStyle, ParseError


def test_parse_from_object_function_docstring():
    """Normal case: parse a simple function docstring."""
    def sample_func(x, y):
        """Return the sum of x and y.

        Parameters
        ----------
        x : int
            First number.
        y : int
            Second number.

        Returns
        -------
        int
            The sum of x and y.
        """
        return x + y

    doc = parse_from_object(sample_func, style=DocstringStyle.GOOGLE)
    assert isinstance(doc, Docstring)
    assert doc.summary == "Return the sum of x and y."
    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"x", "y"}
    assert doc.returns is not None
    assert doc.returns.type_name == "int"


def test_parse_from_object_class_attribute_docstrings(tmp_path):
    """Boundary case: parse a class with attribute docstrings defined in source."""
    # Create a temporary module file with a class that has attribute docstrings.
    module_code = '''
class MyClass:
    """A simple class with attributes."""

    attr1 = 1  # :type int: The first attribute.
    attr2 = "two"  # :type str: The second attribute.
'''
    module_path = tmp_path / "mymodule.py"
    module_path.write_text(module_code)

    # Dynamically import the module
    spec = types.ModuleType("mymodule")
    with open(module_path, "r") as f:
        exec(f.read(), spec.__dict__)

    # Parse the class object
    doc = parse_from_object(spec.MyClass, style=DocstringStyle.AUTO)
    assert isinstance(doc, Docstring)
    # The class docstring should be parsed
    assert doc.summary == "A simple class with attributes."
    # Attribute docstrings should be added to the docstring's meta
    # The meta dict keys are attribute names
    assert "attr1" in doc.meta
    assert "attr2" in doc.meta
    # The attribute docs should contain the type information
    assert doc.meta["attr1"].type_name == "int"
    assert doc.meta["attr2"].type_name == "str"


def test_parse_from_object_missing_docstring_raises():
    """Error case: passing an object with no docstring should raise ParseError."""
    class NoDoc:
        pass

    # Remove the __doc__ attribute to simulate missing docstring
    NoDoc.__doc__ = None

    with pytest.raises(ParseError):
        parse_from_object(NoDoc, style=DocstringStyle.AUTO)
