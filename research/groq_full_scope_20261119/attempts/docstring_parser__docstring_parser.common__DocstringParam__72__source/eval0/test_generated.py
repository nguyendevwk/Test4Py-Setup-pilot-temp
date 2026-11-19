import pytest
from docstring_parser.common import DocstringParam


def test_docstring_param_basic_initialization():
    """Verify that a DocstringParam instance stores all provided values correctly."""
    args = ["arg1", "arg2"]
    description = "This is a test parameter."
    arg_name = "param"
    type_name = "int"
    is_optional = True
    default = "0"

    param = DocstringParam(
        args=args,
        description=description,
        arg_name=arg_name,
        type_name=type_name,
        is_optional=is_optional,
        default=default,
    )

    # Check that the base class attributes are set
    assert param.args == args
    assert param.description == description

    # Check that the DocstringParam specific attributes are set
    assert param.arg_name == arg_name
    assert param.type_name == type_name
    assert param.is_optional is is_optional
    assert param.default == default


def test_docstring_param_with_empty_and_none_values():
    """Test initialization when optional values are omitted or empty."""
    param = DocstringParam(
        args=[],
        description=None,
        arg_name="empty",
        type_name=None,
        is_optional=None,
        default=None,
    )

    # Base class attributes
    assert param.args == []
    assert param.description is None

    # Specific attributes
    assert param.arg_name == "empty"
    assert param.type_name is None
    assert param.is_optional is None
    assert param.default is None


def test_docstring_param_type_name_and_default_handling():
    """Ensure that type_name and default are stored as strings when provided."""
    param = DocstringParam(
        args=["x"],
        description="Parameter x",
        arg_name="x",
        type_name="str",
        is_optional=False,
        default="'default_value'",
    )

    # type_name should be the exact string passed
    assert isinstance(param.type_name, str)
    assert param.type_name == "str"

    # default should be stored as a string, even if it looks like a literal
    assert isinstance(param.default, str)
    assert param.default == "'default_value'"
