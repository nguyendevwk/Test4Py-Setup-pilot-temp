import pytest
from docstring_parser.common import Docstring, DocstringParam, DocstringRaises, DocstringReturns, DocstringDeprecated, DocstringExample

def test_description_construction():
    d = Docstring()
    d.short_description = "Short"
    d.long_description = "Long description."
    d.blank_after_short_description = True
    assert d.description == "Short\n\nLong description."

def test_meta_extraction():
    d = Docstring()
    d.meta = [
        DocstringParam("x", "int", "x value"),
        DocstringRaises(ValueError, "bad value"),
        DocstringReturns("int", "result"),
        DocstringDeprecated("Use new_func instead"),
        DocstringExample("print(foo())")
    ]
    assert d.params == [d.meta[0]]
    assert d.raises == [d.meta[1]]
    assert d.returns == d.meta[2]
    assert d.deprecation == d.meta[3]
    assert d.examples == [d.meta[4]]

def test_description_none_when_empty():
    d = Docstring()
    assert d.description is None
