import pytest
from docstring_parser.numpydoc import parse
from docstring_parser import Docstring

def test_parse_numpydoc_basic():
    docstring = (
        "Short description.\n"
        "\n"
        "This is a long description.\n"
        "\n"
        "Parameters\n"
        "----------\n"
        "param1 : int\n"
        "    The first parameter.\n"
        "\n"
        "Returns\n"
        "-------\n"
        "int\n"
        "    The return value.\n"
        "\n"
        "Examples\n"
        "--------\n"
        ">>> foo(1)\n"
        "2\n"
    )
    result = parse(docstring)
    assert isinstance(result, Docstring)
    assert result.short_description == "Short description."
    assert result.long_description == "This is a long description."
    assert len(result.parameters) == 1
    param = result.parameters[0]
    assert param.name == "param1"
    assert param.type_name == "int"
    assert param.description == "The first parameter."
    assert result.returns.type_name == "int"
    assert result.returns.description == "The return value."
    assert len(result.examples) == 1
    example = result.examples[0]
    assert example.source.strip() == ">>> foo(1)"
    assert example.description.strip() == "2"
