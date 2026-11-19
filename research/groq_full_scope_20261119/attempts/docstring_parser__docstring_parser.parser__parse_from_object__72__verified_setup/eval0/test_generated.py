import inspect
import pytest
from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError, Docstring


def test_parse_class_with_attribute_docstrings(tmp_path):
    # Create a class with an attribute and an attribute docstring
    class Sample:
        """Sample class docstring."""

        attr = 42
        """Attribute docstring for attr."""

    # Parse the class
    doc = parse_from_object(Sample)

    # The class docstring should be parsed correctly
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Sample class docstring."

    # The attribute docstring should be attached
    assert "attr" in doc.attributes
    attr_doc = doc.attributes["attr"]
    assert attr_doc.description == "Attribute docstring for attr."


def test_parse_function_without_attributes():
    def func(x: int) -> int:
        """Function docstring with a single parameter.

        :param x: an integer
        :return: the same integer
        """
        return x

    # Parse the function
    doc = parse_from_object(func)

    # No attributes should be present
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Function docstring with a single parameter."
    assert doc.params[0].arg_name == "x"
    assert doc.params[0].description == "an integer"
    assert doc.returns.description == "the same integer"
    assert not doc.attributes  # empty dict


def test_parse_invalid_style_raises_type_error():
    class Dummy:
        """Dummy class docstring."""

    # Passing an invalid style type should raise a TypeError
    with pytest.raises(TypeError):
        parse_from_object(Dummy, style="not_a_style")
