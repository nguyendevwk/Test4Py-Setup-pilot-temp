import pytest
from docstring_parser.common import DocstringParam


def test_docstringparam_basic():
    """Verify that a normal DocstringParam instance stores all attributes correctly."""
    args = ["x", "y"]
    description = "Parameters x and y."
    arg_name = "x"
    type_name = "int"
    is_optional = False
    default = None

    param = DocstringParam(args, description, arg_name, type_name, is_optional, default)

    # Basic attribute checks
    assert param.args == args
    assert param.description == description
    assert param.arg_name == arg_name
    assert param.type_name == type_name
    assert param.is_optional is is_optional
    assert param.default == default

    # Ensure that the parent class attributes are also set
    assert hasattr(param, "args") and hasattr(param, "description")


def test_docstringparam_empty_and_none():
    """Test boundary conditions: empty args list and None description."""
    args = []
    description = None
    arg_name = "empty"
    type_name = None
    is_optional = True
    default = "0"

    param = DocstringParam(args, description, arg_name, type_name, is_optional, default)

    assert param.args == args
    assert param.description is None
    assert param.arg_name == arg_name
    assert param.type_name is None
    assert param.is_optional is True
    assert param.default == default


def test_docstringparam_invalid_args_type():
    """Passing a non-list to args should raise a TypeError due to super().__init__ expectations."""
    args = "not-a-list"  # invalid type
    description = "Invalid args type"
    arg_name = "invalid"
    type_name = "str"
    is_optional = False
    default = None

    with pytest.raises(TypeError):
        DocstringParam(args, description, arg_name, type_name, is_optional, default)
