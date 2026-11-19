import importlib.util
import inspect
import sys
import types
import tempfile
import textwrap
import os

import pytest

from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError


def test_parse_function_google_style():
    """Verify that a function with a Google style docstring is parsed correctly."""
    def sample_func(a, b):
        """Calculate the sum of two numbers.

        Args:
            a (int): The first number.
            b (int): The second number.

        Returns:
            int: The sum of a and b.
        """
        return a + b

    doc = parse_from_object(sample_func, style=DocstringStyle.GOOGLE)
    assert doc.short_description == "Calculate the sum of two numbers."
    assert len(doc.params) == 2
    assert doc.params[0].arg_name == "a"
    assert doc.params[0].type_name == "int"
    assert doc.params[0].description == "The first number."
    assert doc.params[1].arg_name == "b"
    assert doc.params[1].type_name == "int"
    assert doc.params[1].description == "The second number."
    assert doc.returns.type_name == "int"
    assert doc.returns.description == "The sum of a and b."


def test_parse_class_attribute_docstrings(tmp_path):
    """Verify that attribute docstrings defined in a class are parsed."""
    module_code = textwrap.dedent(
        """
        class MyClass:
            """ + '"""Class docstring."""' + """
            attr1 = 1
            """ + '"""Attribute 1 description."""' + """
            attr2 = "foo"
            """ + '"""Attribute 2 description."""'
    )
    module_file = tmp_path / "mymodule.py"
    module_file.write_text(module_code)

    spec = importlib.util.spec_from_file_location("mymodule", module_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["mymodule"] = mod
    spec.loader.exec_module(mod)

    cls = mod.MyClass
    doc = parse_from_object(cls, style=DocstringStyle.AUTO)
    assert doc.short_description == "Class docstring."
    # Attribute docstrings are added as attributes in the Docstring object
    assert hasattr(doc, "attributes")
    attrs = doc.attributes
    assert "attr1" in attrs
    assert attrs["attr1"].description == "Attribute 1 description."
    assert "attr2" in attrs
    assert attrs["attr2"].description == "Attribute 2 description."


def test_parse_module_attribute_docstrings(tmp_path):
    """Verify that attribute docstrings defined at module level are parsed."""
    module_code = textwrap.dedent(
        """
        """ + '"""Module docstring."""' + """
        var1 = 42
        """ + '"""Variable 1 description."""' + """
        var2 = "bar"
        """ + '"""Variable 2 description."""'
    )
    module_file = tmp_path / "mymodule2.py"
    module_file.write_text(module_code)

    spec = importlib.util.spec_from_file_location("mymodule2", module_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["mymodule2"] = mod
    spec.loader.exec_module(mod)

    doc = parse_from_object(mod, style=DocstringStyle.AUTO)
    assert doc.short_description == "Module docstring."
    assert hasattr(doc, "attributes")
    attrs = doc.attributes
    assert "var1" in attrs
    assert attrs["var1"].description == "Variable 1 description."
    assert "var2" in attrs
    assert attrs["var2"].description == "Variable 2 description."
