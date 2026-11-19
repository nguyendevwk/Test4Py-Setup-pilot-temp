import inspect
import pytest
from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError


def test_parse_from_object_parses_class_and_attributes(tmp_path):
    # Create a simple class with a docstring and an attribute docstring
    class Sample:
        """Sample class docstring.

        Attributes
        ----------
        value : int
            The integer value.
        """

        value = 42  # attribute with docstring defined in the class body

    # Parse the class object
    doc = parse_from_object(Sample)

    # The class docstring should be parsed correctly
    assert doc.short_description == "Sample class docstring."
    # The attribute docstring should be present in the parsed attributes
    attrs = {a.name: a for a in doc.attributes}
    assert "value" in attrs
    assert attrs["value"].type_name == "int"
    assert attrs["value"].description == "The integer value."


def test_parse_from_object_with_google_style(tmp_path):
    # Define a function with a Google style docstring
    def func(x: int, y: str) -> bool:
        """Return True if x is positive and y is not empty.

        Args:
            x (int): The first argument.
            y (str): The second argument.

        Returns:
            bool: The result.
        """
        return x > 0 and bool(y)

    # Parse the function with Google style explicitly
    doc = parse_from_object(func, style=DocstringStyle.GOOGLE)

    # Verify that the parsed arguments match the Google style
    assert len(doc.params) == 2
    assert doc.params[0].arg_name == "x"
    assert doc.params[0].type_name == "int"
    assert doc.params[0].description == "The first argument."
    assert doc.params[1].arg_name == "y"
    assert doc.params[1].type_name == "str"
    assert doc.params[1].description == "The second argument."

    # Verify return description
    assert doc.returns is not None
    assert doc.returns.type_name == "bool"
    assert doc.returns.description == "The result."


def test_parse_from_object_raises_on_invalid_docstring():
    # Define a class with an invalid docstring that cannot be parsed
    class BadDoc:
        """This is a malformed docstring
        that does not follow any known style and
        will cause the parser to raise an error."""

    # The parser should raise ParseError when encountering an invalid docstring
    with pytest.raises(ParseError):
        parse_from_object(BadDoc)
