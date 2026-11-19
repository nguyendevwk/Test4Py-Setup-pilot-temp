import pytest
from docstring_parser.common import DocstringParam, DocstringMeta

def test_docstringparam_basic_initialization(tmp_path):
    """Verify that a DocstringParam instance stores all provided values correctly."""
    args = ["arg1", "arg2"]
    description = "This is a test description."
    arg_name = "test_param"
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
    assert isinstance(param, DocstringMeta)
    assert param.args == args
    assert param.description == description

    # Check that the subclass attributes are set
    assert param.arg_name == arg_name
    assert param.type_name == type_name
    assert param.is_optional is is_optional
    assert param.default == default

def test_docstringparam_edge_cases():
    """Test initialization with minimal and empty values."""
    # Minimal values: empty args list, None description, empty strings for others
    param = DocstringParam(
        args=[],
        description=None,
        arg_name="",
        type_name=None,
        is_optional=None,
        default=None,
    )

    # Base class attributes
    assert param.args == []
    assert param.description is None

    # Subclass attributes
    assert param.arg_name == ""
    assert param.type_name is None
    assert param.is_optional is None
    assert param.default is None

def test_docstringparam_type_consistency():
    """Ensure that the type annotations are respected and that the instance
    behaves like a normal Python object."""
    param = DocstringParam(
        args=["x"],
        description="x parameter",
        arg_name="x",
        type_name="float",
        is_optional=False,
        default="1.0",
    )

    # The instance should be an instance of both classes
    assert isinstance(param, DocstringParam)
    assert isinstance(param, DocstringMeta)

    # The attributes should be accessible and of the expected types
    assert isinstance(param.args, list)
    assert isinstance(param.description, str)
    assert isinstance(param.arg_name, str)
    assert isinstance(param.type_name, str)
    assert isinstance(param.is_optional, bool)
    assert isinstance(param.default, str)
