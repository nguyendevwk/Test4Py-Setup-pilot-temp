import inspect
import types
import textwrap

import pytest

from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError


def test_parse_from_object_with_google_style_docstring(tmp_path):
    """Verify that a Google‑style docstring is parsed correctly and
    attribute docstrings are added for a class."""
    # Create a temporary module with a Google‑style docstring
    module_code = textwrap.dedent(
        """
        \"\"\"Module docstring.

        Args:
            x (int): The first argument.
        \"\"\"

        class MyClass:
            \"\"\"Class docstring.

            Attributes:
                attr1 (str): Description of attr1.
                attr2 (int): Description of attr2.
            \"\"\"

            attr1 = "value1"
            attr2 = 42
        """
    )
    module_path = tmp_path / "mymodule.py"
    module_path.write_text(module_code)

    # Import the module dynamically
    import importlib.util
    spec = importlib.util.spec_from_file_location("mymodule", str(module_path))
    mymodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mymodule)

    # Parse the module docstring
    module_doc = parse_from_object(mymodule, style=DocstringStyle.GOOGLE)
    assert module_doc.short_description == "Module docstring."
    assert len(module_doc.params) == 1
    assert module_doc.params[0].arg_name == "x"

    # Parse the class docstring and check that attribute docs are added
    class_doc = parse_from_object(mymodule.MyClass, style=DocstringStyle.GOOGLE)
    assert class_doc.short_description == "Class docstring."
    # Attributes are parsed as attributes of the class
    attr_names = {attr.attr_name for attr in class_doc.attributes}
    assert {"attr1", "attr2"} == attr_names
    # Verify that the attribute descriptions are correct
    attr_desc = {attr.attr_name: attr.description for attr in class_doc.attributes}
    assert attr_desc["attr1"] == "Description of attr1."
    assert attr_desc["attr2"] == "Description of attr2."


def test_parse_from_object_with_missing_docstring_raises():
    """Passing an object without a docstring should raise ParseError."""
    class NoDoc:
        pass

    # Remove the __doc__ attribute to simulate missing docstring
    NoDoc.__doc__ = None

    with pytest.raises(ParseError):
        parse_from_object(NoDoc)


def test_parse_from_object_auto_style_falls_back_to_google(tmp_path):
    """When style is AUTO and the docstring matches Google style,
    the parser should correctly interpret it."""
    # Create a temporary module with a Google‑style docstring
    module_code = textwrap.dedent(
        """
        \"\"\"Short description.

        Args:
            a (int): first argument.
            b (str): second argument.
        \"\"\"
        """
    )
    module_path = tmp_path / "google_module.py"
    module_path.write_text(module_code)

    # Import the module dynamically
    import importlib.util
    spec = importlib.util.spec_from_file_location("google_module", str(module_path))
    google_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(google_module)

    # Parse with AUTO style
    doc = parse_from_object(google_module, style=DocstringStyle.AUTO)
    assert doc.short_description == "Short description."
    assert len(doc.params) == 2
    assert doc.params[0].arg_name == "a"
    assert doc.params[1].arg_name == "b"
