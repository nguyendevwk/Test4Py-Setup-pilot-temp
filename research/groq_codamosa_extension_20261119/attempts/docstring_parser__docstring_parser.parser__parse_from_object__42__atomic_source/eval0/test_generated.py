import importlib.util
import sys
import types
import inspect
import tempfile
import os
import pytest
from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError, Docstring

def test_parse_function_docstring():
    """Normal case: parse a simple function docstring."""
    def sample_func():
        """Short summary.

        Detailed description.
        """
        pass

    doc = parse_from_object(sample_func, style=DocstringStyle.AUTO)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short summary."
    assert doc.long_description == "Detailed description."

def test_parse_class_attribute_docstrings(tmp_path):
    """Boundary case: parse a class with attribute docstrings defined in source."""
    module_code = '''
class MyClass:
    """Class docstring."""
    attr1 = 1
    """Attribute 1 docstring."""
    attr2 = "two"
    """Attribute 2 docstring."""
'''
    module_file = tmp_path / "mymodule.py"
    module_file.write_text(module_code)
    spec = importlib.util.spec_from_file_location("mymodule", module_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mymodule"] = module
    spec.loader.exec_module(module)

    cls = module.MyClass
    doc = parse_from_object(cls, style=DocstringStyle.AUTO)
    assert isinstance(doc, Docstring)
    # Class docstring
    assert doc.short_description == "Class docstring."
    # Attribute docstrings should be added
    attr_docs = {ad.name: ad.description for ad in doc.attribute_docs}
    assert attr_docs["attr1"] == "Attribute 1 docstring."
    assert attr_docs["attr2"] == "Attribute 2 docstring."

def test_parse_invalid_docstring_raises():
    """Error case: passing an object with an unparsable docstring raises ParseError."""
    class BadDoc:
        """This is a bad docstring that will cause a ParseError because it contains
        an unmatched bracket [.
        """
    with pytest.raises(ParseError):
        parse_from_object(BadDoc, style=DocstringStyle.AUTO)
