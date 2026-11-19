import importlib.util
import inspect
import os
import sys
import types
import tempfile
import textwrap

import pytest

from docstring_parser.parser import parse_from_object
from docstring_parser.common import DocstringStyle, ParseError


def test_parse_from_object_with_class_and_attribute_docstrings(tmp_path):
    """Verify that attribute docstrings are added to a class."""
    # Create a temporary module file with a class that has an attribute docstring
    module_code = textwrap.dedent(
        """
        class MyClass:
            \"\"\"Class docstring.\"\"\"

            my_attr = 42
            \"\"\"The value of my_attr.\n\n            :type: int\"\"\"
        """
    )
    module_path = tmp_path / "mymodule.py"
    module_path.write_text(module_code)

    # Import the module
    spec = importlib.util.spec_from_file_location("mymodule", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mymodule"] = module
    spec.loader.exec_module(module)

    # Parse the class
    doc = parse_from_object(module.MyClass, style=DocstringStyle.AUTO)

    # The class docstring should be parsed
    assert doc.short_description == "Class docstring."
    # The attribute docstring should be present in the parsed attributes
    attr_docs = {a.name: a for a in doc.attributes}
    assert "my_attr" in attr_docs
    assert attr_docs["my_attr"].description == "The value of my_attr."
    assert attr_docs["my_attr"].type_name == "int"


def test_parse_from_object_auto_style_selection(tmp_path):
    """Ensure that AUTO style correctly selects the style based on the docstring."""
    # Create a temporary module with a function using Google style docstring
    module_code = textwrap.dedent(
        """
        def func(x, y):
            \"\"\"Compute something.\n\n            Args:\n                x (int): First value.\n                y (int): Second value.\n            Returns:\n                int: Result.\n            \"\"\"
            return x + y
        """
    )
    module_path = tmp_path / "google_module.py"
    module_path.write_text(module_code)

    # Import the module
    spec = importlib.util.spec_from_file_location("google_module", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["google_module"] = module
    spec.loader.exec_module(module)

    # Parse the function with AUTO style
    doc = parse_from_object(module.func, style=DocstringStyle.AUTO)

    # The parsed arguments should match the Google style
    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"x", "y"}
    assert doc.returns.type_name == "int"
    assert doc.returns.description == "Result."


def test_parse_from_object_invalid_style_raises_parse_error():
    """Passing an unsupported style should raise ParseError."""
    # Define a simple function with a docstring
    def dummy():
        """Just a docstring."""
        pass

    # Attempt to parse with an invalid style (not part of DocstringStyle enum)
    with pytest.raises(ParseError):
        parse_from_object(dummy, style="invalid_style")  # type: ignore[arg-type]
