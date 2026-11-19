import pytest
from docstring_parser.common import Docstring, DocstringMeta, DocstringParam, DocstringRaises, DocstringReturns, DocstringDeprecated, DocstringExample

def test_description_property_combines_short_and_long():
    d = Docstring()
    d.short_description = "Short"
    d.long_description = "Long"
    d.blank_after_short_description = True
    assert d.description == "Short\n\nLong"

def test_params_and_raises_extraction():
    d = Docstring()
    d.meta.extend([
        DocstringParam("x", "int", "x value"),
        DocstringParam("y", "int", "y value"),
        DocstringRaises(ValueError, "bad value"),
        DocstringRaises(KeyError, "missing key")
    ])
    params = d.params
    raises = d.raises
    assert len(params) == 2
    assert all(isinstance(p, DocstringParam) for p in params)
    assert [p.name for p in params] == ["x", "y"]
    assert len(raises) == 2
    assert all(isinstance(r, DocstringRaises) for r in raises)
    assert [r.exception for r in raises] == [ValueError, KeyError]

def test_returns_and_deprecation_and_examples():
    d = Docstring()
    d.meta.extend([
        DocstringReturns("int", "result"),
        DocstringDeprecated("Use new_func instead."),
        DocstringExample("print(new_func(1))")
    ])
    assert isinstance(d.returns, DocstringReturns)
    assert d.returns.type == "int"
    assert d.deprecation is not None
    assert isinstance(d.deprecation, DocstringDeprecated)
    assert d.deprecation.message == "Use new_func instead."
    examples = d.examples
    assert len(examples) == 1
    assert isinstance(examples[0], DocstringExample)
    assert examples[0].example == "print(new_func(1))"
