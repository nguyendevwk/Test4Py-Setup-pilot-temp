import pytest
from docstring_parser.common import DocstringParam, DocstringMeta


def test_docstringparam_initialization_normal():
    """Verify that DocstringParam stores all provided values correctly."""
    args = ["arg1", "arg2"]
    description = "This is a test parameter."
    param = DocstringParam(
        args=args,
        description=description,
        arg_name="param_name",
        type_name="int",
        is_optional=False,
        default="0",
    )
    # Base class attributes
    assert isinstance(param, DocstringMeta)
    assert param.args == args
    assert param.description == description
    # Specific attributes
    assert param.arg_name == "param_name"
    assert param.type_name == "int"
    assert param.is_optional is False
    assert param.default == "0"


def test_docstringparam_initialization_boundary():
    """Test boundary conditions: empty args list and None values."""
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
    # Specific attributes
    assert param.arg_name == ""
    assert param.type_name is None
    assert param.is_optional is None
    assert param.default is None


def test_docstringparam_invalid_args_type():
    """Passing a non-list to args should raise a TypeError when accessed as list."""
    # The constructor does not enforce type, but accessing as list should work.
    # We test that providing a string instead of a list leads to a TypeError when
    # the code expects a list (e.g., iterating over it).
    param = DocstringParam(
        args="not-a-list",
        description="desc",
        arg_name="name",
        type_name="str",
        is_optional=False,
        default="",
    )
    # Accessing args as a list should raise TypeError when iterated
    with pytest.raises(TypeError):
        for _ in param.args:
            pass
