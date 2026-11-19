import pytest
from docstring_parser.common import DocstringParam

def test_normal_initialization():
    """Verify that a DocstringParam instance stores all provided values correctly."""
    args = ["x", "y"]
    description = "Parameters for the function."
    arg_name = "x"
    type_name = "int"
    is_optional = False
    default = "0"

    param = DocstringParam(args, description, arg_name, type_name, is_optional, default)

    assert param.args == args
    assert param.description == description
    assert param.arg_name == arg_name
    assert param.type_name == type_name
    assert param.is_optional is is_optional
    assert param.default == default

def test_boundary_values():
    """Test initialization with boundary (empty or None) values."""
    args = []
    description = None
    arg_name = "param"
    type_name = None
    is_optional = None
    default = None

    param = DocstringParam(args, description, arg_name, type_name, is_optional, default)

    assert param.args == args
    assert param.description is None
    assert param.arg_name == arg_name
    assert param.type_name is None
    assert param.is_optional is None
    assert param.default is None

def test_invalid_args_type_raises():
    """Passing a non-list to args should raise a TypeError."""
    with pytest.raises(TypeError):
        # args should be a list; passing an int should cause a TypeError when
        # the superclass or this class attempts to iterate over it.
        DocstringParam(1, "desc", "name", "type", False, "default")
