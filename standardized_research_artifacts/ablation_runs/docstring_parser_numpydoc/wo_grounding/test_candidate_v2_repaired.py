import pytest
from docstring_parser.numpydoc import parse
from docstring_parser import Docstring


def test_parse_numpydoc_basic_and_none():
    doc = """This function does something.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str, optional
        The second parameter.

    Returns
    -------
    bool
        True if successful.
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    assert parsed.short_description == "This function does something."
    assert len(parsed.parameters) == 2

    x_param = parsed.parameters[0]
    assert x_param.name == "x"
    assert x_param.type_name == "int"
    assert x_param.description == "The first parameter."

    y_param = parsed.parameters[1]
    assert y_param.name == "y"
    assert y_param.type_name == "str, optional"
    assert y_param.description == "The second parameter."

    assert len(parsed.returns) == 1
    ret = parsed.returns[0]
    assert ret.type_name == "bool"
    assert ret.description == "True if successful."

    parsed_none = parse(None)
    assert isinstance(parsed_none, Docstring)
    assert parsed_none.short_description is None
