from docstring_parser.numpydoc import parse

def test_parse_numpydoc_sections():
    docstring = (
        "Summary.\n\n"
        "Parameters\n"
        "----------\n"
        "x : int\n"
        "    Param x.\n\n"
        "Returns\n"
        "-------\n"
        "int\n"
        "    Return value.\n\n"
        "Raises\n"
        "------\n"
        "ValueError\n"
        "    If something goes wrong.\n"
    )
    doc = parse(docstring)

    assert doc.short_description == "Summary."
    assert doc.long_description is None

    assert len(doc.params) == 1
    param = doc.params[0]
    assert param.arg_name == "x"
    assert param.type_name == "int"
    assert param.description == "Param x."

    assert doc.returns.type_name == "int"
    assert doc.returns.description == "Return value."

    assert doc.raises.type_name == "ValueError"
    assert doc.raises.description == "If something goes wrong."
