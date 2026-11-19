import ast
import types
import builtins
import sys
import importlib
import pytest
from py_backwards.transformers.return_from_generator import ReturnFromGeneratorTransformer
from typed_ast import ast3 as typed_ast

def _parse(code: str) -> typed_ast.AST:
    """Parse source code into a typed_ast AST."""
    return typed_ast.parse(code)

def _transform_and_exec(code: str, globals_dict=None):
    """Transform the code with ReturnFromGeneratorTransformer and execute it."""
    tree = _parse(code)
    transformer = ReturnFromGeneratorTransformer()
    transformed = transformer.visit(tree)
    # Compile the transformed AST to a code object
    compiled = typed_ast.compile(transformed, filename="<ast>", mode="exec")
    exec(compiled, globals_dict or {})

def test_generator_with_return_raises_stopiteration():
    """A generator that returns a value should raise StopIteration with that value."""
    code = """
def gen():
    yield 1
    return 42
"""
    globals_dict = {}
    _transform_and_exec(code, globals_dict)
    gen = globals_dict["gen"]
    # The generator should yield 1 and then raise StopIteration with value 42
    it = gen()
    assert next(it) == 1
    with pytest.raises(StopIteration) as excinfo:
        next(it)
    assert excinfo.value.args[0] == 42

def test_generator_without_return_remains_unchanged():
    """A generator without a return should be unchanged by the transformer."""
    code = """
def gen():
    yield 1
    yield 2
"""
    globals_dict = {}
    _transform_and_exec(code, globals_dict)
    gen = globals_dict["gen"]
    it = gen()
    assert list(it) == [1, 2]

def test_return_without_value_is_ignored():
    """A return without a value should not be transformed and should raise StopIteration normally."""
    code = """
def gen():
    yield 1
    return
"""
    globals_dict = {}
    _transform_and_exec(code, globals_dict)
    gen = globals_dict["gen"]
    it = gen()
    assert next(it) == 1
    with pytest.raises(StopIteration) as excinfo:
        next(it)
    # StopIteration should have no arguments
    assert excinfo.value.args == ()
