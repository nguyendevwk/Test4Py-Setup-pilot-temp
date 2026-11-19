from docstring_parser.numpydoc import parse

def test_parse_numpydoc_sections():
    docstring = """Summary.

Parameters
----------
x : int
    Param x.
y : str, optional
    Param y.

Returns
-------
bool
    True if successful.

Raises
------
ValueError
    If invalid input.
"""
    doc = parse(docstring)
    assert doc.short_description == "Summary."
    assert len(doc.params) == 2
    p1, p2 = doc.params
    assert (p1.arg_name, p1.type_name, p1.description) == ("x", "int", "Param x.")
    assert (p2.arg_name, p2.type_name, p2.description) == ("y", "str, optional", "Param y.")
    assert doc.returns is not None
    assert (doc.returns.type_name, doc.returns.description) == ("bool", "True if successful.")
    assert len(doc.raises) == 1
    r = doc.raises[0]
    assert (r.type_name, r.description) == ("ValueError", "If invalid input.")
