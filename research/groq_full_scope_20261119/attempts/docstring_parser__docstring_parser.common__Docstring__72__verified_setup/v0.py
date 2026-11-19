import pytest
from docstring_parser.common import Docstring, DocstringMeta, DocstringParam, DocstringRaises, DocstringReturns, DocstringDeprecated, DocstringExample

def test_description_with_blank_and_long():
    d = Docstring()
    d.short_description = "Short"
    d.blank_after_short_description = True
    d.long_description = "Long description."
    assert d.description == "Short\n\nLong description."

def test_params_extraction_and_order():
    d = Docstring()
    d.meta.append(DocstringMeta(name="a", type="int", description="first"))
    d.meta.append(DocstringMeta(name="b", type="str", description="second"))
    # Only DocstringParam instances should be returned
    d.meta.append(DocstringParam(name="c", type="float", description="third"))
    params = d.params
    assert len(params) == 1
    assert params[0].name == "c"
    assert params[0].type == "float"

def test_returns_and_raises_single_and_multiple():
    d = Docstring()
    d.meta.append(DocstringReturns(type="int", description="return int"))
    d.meta.append(DocstringRaises(type="ValueError", description="bad value"))
    d.meta.append(DocstringRaises(type="TypeError", description="bad type"))
    # returns property returns first DocstringReturns
    assert isinstance(d.returns, DocstringReturns)
    assert d.returns.type == "int"
    # many_returns returns all DocstringReturns
    assert d.many_returns == [d.returns]
    # raises property returns all DocstringRaises
    raises = d.raises
    assert len(raises) == 2
    assert {r.type for r in raises} == {"ValueError", "TypeError"}
