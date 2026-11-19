import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.utils.snippet import VariablesReplacer

def test_replace_name_and_attribute():
    # Original code with a variable and an attribute
    src = "x = y\nobj.attr = z"
    tree = typed_ast.parse(src)

    # Mapping: replace 'y' with 'y_unique', 'z' with 'z_unique', and 'attr' with 'attr_unique'
    mapping = {"y": "y_unique", "z": "z_unique", "attr": "attr_unique"}
    VariablesReplacer.replace(tree, mapping)

    # Verify that the Name node 'y' was replaced
    assign = tree.body[0]
    assert isinstance(assign, typed_ast.Assign)
    assert isinstance(assign.value, typed_ast.Name)
    assert assign.value.id == "y_unique"

    # Verify that the Attribute node 'attr' was replaced
    assign2 = tree.body[1]
    assert isinstance(assign2, typed_ast.Assign)
    assert isinstance(assign2.value, typed_ast.Attribute)
    assert assign2.value.attr == "attr_unique"

def test_replace_import_from_and_alias():
    # Original code with an ImportFrom and alias
    src = "from mod.sub import foo as bar\nfrom mod import baz"
    tree = typed_ast.parse(src)

    # Mapping: replace module parts and alias names
    mapping = {"mod": "mod_unique", "foo": "foo_unique", "bar": "bar_unique", "baz": "baz_unique"}
    VariablesReplacer.replace(tree, mapping)

    # Check first ImportFrom: module should be replaced
    imp1 = tree.body[0]
    assert isinstance(imp1, typed_ast.ImportFrom)
    assert imp1.module == "mod_unique.sub"

    # Check alias inside first ImportFrom
    alias1 = imp1.names[0]
    assert alias1.name == "foo_unique"
    assert alias1.asname == "bar_unique"

    # Check second ImportFrom: module should be replaced
    imp2 = tree.body[1]
    assert isinstance(imp2, typed_ast.ImportFrom)
    assert imp2.module == "mod_unique"
    assert imp2.names[0].name == "baz_unique"

def test_no_replacement_for_unmapped_names():
    # Original code with names that are not in the mapping
    src = "a = b\nc.d = e"
    tree = typed_ast.parse(src)

    # Empty mapping: nothing should change
    mapping = {}
    VariablesReplacer.replace(tree, mapping)

    # Verify that names remain unchanged
    assign1 = tree.body[0]
    assert isinstance(assign1, typed_ast.Assign)
    assert assign1.value.id == "b"

    assign2 = tree.body[1]
    assert isinstance(assign2, typed_ast.Assign)
    assert assign2.value.attr == "d"
    assert assign2.value.value.id == "c"
