import pytest
from docstring_parser.common import DocstringParam, DocstringMeta

def test_docstring_param_basic_initialization():
    """Test that a DocstringParam instance stores all provided attributes correctly."""
    args = ["arg1", "arg2"]
    description = "This is a test description."
    arg_name = "my_arg"
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

    # Verify that the base class attributes are set
    assert isinstance(param, DocstringMeta)
    assert param.args == args
    assert param.description == description

    # Verify that the DocstringParam specific attributes are set
    assert param.arg_name == arg_name
    assert param.type_name == type_name
    assert param.is_optional is is_optional
    assert param.default == default

def test_docstring_param_with_empty_and_none_values():
    """Test initialization with empty list and None values for optional fields."""
    args = []
    description = None
    arg_name = "empty_arg"
    type_name = None
    is_optional = None
    default = None

    param = DocstringParam(
        args=args,
        description=description,
        arg_name=arg_name,
        type_name=type_name,
        is_optional=is_optional,
        default=default,
    )

    # Base class attributes
    assert param.args == args
    assert param.description is None

    # Specific attributes
    assert param.arg_name == arg_name
    assert param.type_name is None
    assert param.is_optional is None
    assert param.default is None

def test_docstring_param_attribute_mutation_and_identity():
    """Test that attributes can be mutated after creation and that identity is preserved."""
    param = DocstringParam(
        args=["x"],
        description="desc",
        arg_name="x",
        type_name="str",
        is_optional=False,
        default="",
    )

    # Mutate attributes
    param.args.append("y")
    param.description = "new desc"
    param.arg_name = "y"
    param.type_name = "int"
    param.is_optional = True
    param.default = "42"

    # Verify mutations
    assert param.args == ["x", "y"]
    assert param.description == "new desc"
    assert param.arg_name == "y"
    assert param.type_name == "int"
    assert param.is_optional is True
    assert param.default == "42"

    # Ensure the object identity remains the same
    assert isinstance(param, DocstringParam)
