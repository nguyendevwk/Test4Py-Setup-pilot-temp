import inspect
import types
import pytest
from docstring_parser import parser
from docstring_parser.common import DocstringStyle, Docstring


def test_parse_from_object_with_class_attributes(tmp_path):
    # Create a class with a docstring and attribute docstrings
    class Sample:
        """Class docstring with a short description."""

        attr1 = 42
        """Attribute 1 description."""

        attr2 = "hello"
        """Attribute 2 description."""

    # Parse the class object
    result = parser.parse_from_object(Sample, style=DocstringStyle.GOOGLE)

    # The result should be a Docstring instance
    assert isinstance(result, Docstring)

    # The class docstring should be parsed correctly
    assert result.short_description == "Class docstring with a short description."

    # Attribute docstrings should be added to the result
    attr_docs = {attr.name: attr for attr in result.attributes}
    assert "attr1" in attr_docs
    assert "attr2" in attr_docs
    assert attr_docs["attr1"].description == "Attribute 1 description."
    assert attr_docs["attr2"].description == "Attribute 2 description."

    # No methods should be present
    assert len(result.methods) == 0


def test_parse_from_object_with_module_attributes(tmp_path):
    # Dynamically create a module with attributes and docstrings
    mod = types.ModuleType("dummy_module")
    mod.__doc__ = "Module docstring."
    mod.var1 = 10
    mod.var1.__doc__ = "Variable 1 description."
    mod.var2 = "world"
    mod.var2.__doc__ = "Variable 2 description."

    # Parse the module object
    result = parser.parse_from_object(mod, style=DocstringStyle.NUMPYDOC)

    # Verify module docstring
    assert result.short_description == "Module docstring."

    # Verify attribute docstrings
    attr_docs = {attr.name: attr for attr in result.attributes}
    assert "var1" in attr_docs
    assert "var2" in attr_docs
    assert attr_docs["var1"].description == "Variable 1 description."
    assert attr_docs["var2"].description == "Variable 2 description."


def test_parse_from_object_with_nonclass_nonmodule(tmp_path):
    # Create a simple function with a docstring
    def func(x: int) -> int:
        """Function docstring."""
        return x

    # Parse the function object
    result = parser.parse_from_object(func, style=DocstringStyle.REST)

    # Verify that the function docstring is parsed
    assert result.short_description == "Function docstring."

    # No attributes should be added for a function
    assert len(result.attributes) == 0

    # The function should have a signature parsed
    assert result.args[0].arg_name == "x"
    assert result.args[0].type_name == "int"
    assert result.return_type == "int"
