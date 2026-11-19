import ast
import pytest
from py_backwards.transformers.string_types import StringTypesTransformer
from py_backwards.types import TransformationResult

def test_single_str_replacement(tmp_path):
    src = "x = str('hello')"
    tree = ast.parse(src)
    result: TransformationResult = StringTypesTransformer.transform(tree)
    assert result.changed is True
    new_src = ast.unparse(result.tree)
    assert "unicode('hello')" in new_src
    assert "str('hello')" not in new_src

def test_no_str_no_change(tmp_path):
    src = "x = int('123')"
    tree = ast.parse(src)
    result: TransformationResult = StringTypesTransformer.transform(tree)
    assert result.changed is False
    new_src = ast.unparse(result.tree)
    assert new_src == src

def test_multiple_str_replacement(tmp_path):
    src = """
def f():
    a = str('a')
    b = str('b')
    return a + b
"""
    tree = ast.parse(src)
    result: TransformationResult = StringTypesTransformer.transform(tree)
    assert result.changed is True
    new_src = ast.unparse(result.tree)
    assert new_src.count("unicode('a')") == 1
    assert new_src.count("unicode('b')") == 1
    assert "str('a')" not in new_src
    assert "str('b')" not in new_src
