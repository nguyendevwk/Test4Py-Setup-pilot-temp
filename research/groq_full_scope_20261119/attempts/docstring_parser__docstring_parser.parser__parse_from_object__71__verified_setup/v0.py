import inspect
import types
import pytest
from docstring_parser import epydoc, google, numpydoc, rest
from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, Docstring


def test_parse_class_with_attribute_docstring(tmp_path):
    # Create a class with a docstring and an attribute docstring
    class MyClass:
        """This is the class docstring."""

        my_attr = 42
        """Attribute docstring for my_attr."""

    # Parse the class
    parsed = parse_from_object(MyClass, style=DocstringStyle.AUTO)

    # The class docstring should be parsed
    assert parsed.short_description == "This is the class docstring."

    # The attribute docstring should be present
    assert any(
        param.name == "my_attr" and param.description == "Attribute docstring for my_attr."
        for param in parsed.params
    ), "Attribute docstring not found in parsed params"


def test_parse_module_with_attribute_docstring(tmp_path):
    # Dynamically create a module with an attribute docstring
    mod = types.ModuleType("temp_mod")
    mod.__doc__ = "Module docstring."
    mod.some_var = "value"
    mod.some_var.__doc__ = "Docstring for some_var."

    # Parse the module
    parsed = parse_from_object(mod, style=DocstringStyle.AUTO)

    # Module docstring should be parsed
    assert parsed.short_description == "Module docstring."

    # Attribute docstring should be present
    assert any(
        param.name == "some_var" and param.description == "Docstring for some_var."
        for param in parsed.params
    ), "Attribute docstring not found in parsed params"


def test_parse_object_without_docstring(tmp_path):
    # An integer has no docstring (None)
    obj = 123

    # Parsing should not raise and return an empty Docstring
    parsed = parse_from_object(obj, style=DocstringStyle.AUTO)

    assert isinstance(parsed, Docstring)
    assert parsed.short_description == ""
    assert parsed.long_description == ""
    assert parsed.params == []
    assert parsed.returns is None
