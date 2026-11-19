import importlib.util
import inspect
import sys
import types
import pytest
from docstring_parser import parse_from_object, DocstringStyle, ParseError

def test_parse_function_docstring():
    """Verify that a simple function's docstring is parsed correctly."""
    def sample_func(a, b):
        """Adds two numbers.

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
        return a + b

    doc = parse_from_object(sample_func, style=DocstringStyle.GOOGLE)
    assert doc.short_description == "Adds two numbers."
    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"a", "b"}
    assert doc.returns is not None
    assert doc.returns.type_name == "int"

def test_parse_class_attribute_docstrings(tmp_path):
    """Verify that attribute docstrings defined in a module are parsed."""
    module_code = '''
    """Module docstring."""

    class MyClass:
        """Class docstring."""
        attr1 = 1
        """Attribute 1 description."""
        attr2 = "two"
        """Attribute 2 description."""
    '''
    module_file = tmp_path / "temp_module.py"
    module_file.write_text(module_code)
    spec = importlib.util.spec_from_file_location("temp_module", module_file)
    temp_module = importlib.util.module_from_spec(spec)
    sys.modules["temp_module"] = temp_module
    spec.loader.exec_module(temp_module)

    doc = parse_from_object(temp_module, style=DocstringStyle.AUTO)
    # Module docstring should be parsed
    assert doc.short_description == "Module docstring."
    # Attribute docstrings should be added
    attr_docs = {attr.name: attr.description for attr in doc.attributes}
    assert attr_docs["attr1"] == "Attribute 1 description."
    assert attr_docs["attr2"] == "Attribute 2 description."

def test_invalid_style_raises():
    """Verify that passing an invalid style raises ParseError."""
    def dummy():
        """Dummy docstring."""
        pass

    with pytest.raises(ParseError):
        parse_from_object(dummy, style="not_a_style")
