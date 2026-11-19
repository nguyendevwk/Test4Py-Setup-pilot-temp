import inspect
import pytest
from docstring_parser import parser
from docstring_parser.common import DocstringStyle, ParseError


def test_parse_from_object_with_attribute_docstrings(tmp_path):
    """When parsing a class, attribute docstrings are added to the result."""
    class Sample:
        """Class docstring."""

        attr1 = 1
        """Attribute 1 description."""

        attr2 = "value"
        """Attribute 2 description."""

    doc = parser.parse_from_object(Sample, style=DocstringStyle.GOOGLE)
    # The class docstring should be present
    assert doc.short_description == "Class docstring."
    # Attribute docstrings should be parsed and attached
    attr_docs = {a.name: a for a in doc.attributes}
    assert "attr1" in attr_docs
    assert attr_docs["attr1"].description == "Attribute 1 description."
    assert "attr2" in attr_docs
    assert attr_docs["attr2"].description == "Attribute 2 description."


def test_parse_from_object_with_no_docstring_returns_empty_docstring():
    """Parsing an object with no docstring yields an empty Docstring."""
    class EmptyDoc:
        pass

    doc = parser.parse_from_object(EmptyDoc)
    # No short description, no attributes, etc.
    assert doc.short_description is None
    assert doc.long_description is None
    assert doc.params == []
    assert doc.returns is None
    assert doc.raises == []
    assert doc.attributes == []


def test_parse_from_object_with_invalid_style_raises_parse_error():
    """Providing a style that cannot parse the docstring raises ParseError."""
    class BadDoc:
        """This docstring is not in any supported style."""

    with pytest.raises(ParseError):
        parser.parse_from_object(BadDoc, style=DocstringStyle.AUTO)
