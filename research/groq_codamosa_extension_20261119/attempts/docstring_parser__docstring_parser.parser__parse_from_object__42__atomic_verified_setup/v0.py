import inspect
import pytest
from docstring_parser import parser
from docstring_parser.common import ParseError, DocstringStyle


def test_parse_function_docstring():
    """Normal case: parse a simple function docstring."""
    def sample_func(x, y):
        """Adds two numbers.

        Parameters
        ----------
        x : int
            First number.
        y : int
            Second number.

        Returns
        -------
        int
            Sum of x and y.
        """
        return x + y

    doc = parser.parse_from_object(sample_func, style=DocstringStyle.GOOGLE)
    assert doc.short_description == "Adds two numbers."
    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"x", "y"}
    assert doc.returns is not None
    assert doc.returns.type_name == "int"
    assert doc.returns.description == "Sum of x and y."


def test_parse_class_attribute_docstrings(tmp_path):
    """Boundary case: parse attribute docstrings defined in a class."""
    # Create a temporary module file with a class that has attribute docstrings.
    module_code = '''
class MyClass:
    """Example class with attributes."""

    attr1 = 10  # The first attribute.
    attr2 = "hello"  # The second attribute.
'''
    module_file = tmp_path / "mymodule.py"
    module_file.write_text(module_code)

    # Import the temporary module dynamically.
    import importlib.util
    spec = importlib.util.spec_from_file_location("mymodule", str(module_file))
    mymodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mymodule)

    cls = mymodule.MyClass
    doc = parser.parse_from_object(cls, style=DocstringStyle.AUTO)

    # The class docstring should be parsed.
    assert doc.short_description == "Example class with attributes."

    # Attribute docstrings should be present.
    attr_docs = {attr.name: attr for attr in doc.attributes}
    assert "attr1" in attr_docs
    assert "attr2" in attr_docs
    assert attr_docs["attr1"].description == "The first attribute."
    assert attr_docs["attr2"].description == "The second attribute."


def test_parse_object_without_docstring_raises():
    """Error case: parsing an object with no docstring should raise ParseError."""
    class NoDoc:
        pass

    with pytest.raises(ParseError):
        parser.parse_from_object(NoDoc)
