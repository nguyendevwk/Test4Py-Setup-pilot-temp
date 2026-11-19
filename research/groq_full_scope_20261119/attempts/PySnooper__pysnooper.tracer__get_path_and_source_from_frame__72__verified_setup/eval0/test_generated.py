import builtins
import inspect
import os
import types
import sys
import tempfile

import pytest

from pysnooper.tracer import get_path_and_source_from_frame, source_and_path_cache, UnavailableSource


def _make_function_from_source(source_code, globals_dict=None):
    """Create a function object from source code string."""
    module_name = "__temp_module__"
    code = compile(source_code, module_name, "exec")
    exec_namespace = {}
    if globals_dict:
        exec_namespace.update(globals_dict)
    exec(code, exec_namespace)
    # Return the first function defined in the namespace
    for obj in exec_namespace.values():
        if isinstance(obj, types.FunctionType):
            return obj
    raise RuntimeError("No function found in source")


def test_get_path_and_source_from_frame_reads_file(tmp_path):
    """Normal case: source read from a real file."""
    file_path = tmp_path / "sample.py"
    file_path.write_text("def foo():\n    return 42\n")
    func = _make_function_from_source("def foo():\n    return 42\n")
    frame = func.__code__.co_firstlineno
    # Get the frame object for the function
    frame_obj = inspect.getframeinfo(inspect.currentframe()).frame
    # Use the function's frame
    frame_obj = func.__code__.co_firstlineno
    # Actually we need a frame object; use inspect.currentframe() inside func
    def wrapper():
        return inspect.currentframe()
    wrapper_func = _make_function_from_source(
        "def wrapper():\n    return inspect.currentframe()", {"inspect": inspect}
    )
    wrapper_frame = wrapper_func()
    result_path, result_source = get_path_and_source_from_frame(wrapper_frame)
    assert result_path == wrapper_frame.f_code.co_filename
    assert isinstance(result_source, list)
    assert result_source[0].startswith("def wrapper():")
    # Ensure caching works
    cached = source_and_path_cache[(wrapper_frame.f_globals.get("__name__"), wrapper_frame.f_code.co_filename)]
    assert cached == (result_path, result_source)


def test_get_path_and_source_from_frame_handles_encoding(tmp_path):
    """Boundary case: file with encoding header."""
    file_path = tmp_path / "encoded.py"
    content = "# coding: latin-1\n" + "def bar():\n    return 'á'\n"
    file_path.write_text(content, encoding="latin-1")
    func = _make_function_from_source("def bar():\n    return 'á'\n")
    wrapper_func = _make_function_from_source(
        "def wrapper():\n    return inspect.currentframe()", {"inspect": inspect}
    )
    wrapper_frame = wrapper_func()
    path, source = get_path_and_source_from_frame(wrapper_frame)
    assert path == wrapper_frame.f_code.co_filename
    assert isinstance(source[0], str)
    assert "def wrapper()" in source[0]
    # The source should be decoded correctly
    assert any("á" in line for line in source)


def test_get_path_and_source_from_frame_fallback_to_unavailable(tmp_path):
    """Error case: loader raises ImportError, file missing, returns UnavailableSource."""
    # Create a dummy loader that raises ImportError
    class BadLoader:
        def get_source(self, name):
            raise ImportError("cannot load")

    globals_dict = {"__loader__": BadLoader(), "__name__": "__bad_module__"}
    func = _make_function_from_source("def bad():\n    return 1", globals_dict)
    wrapper_func = _make_function_from_source(
        "def wrapper():\n    return inspect.currentframe()", {"inspect": inspect}
    )
    wrapper_frame = wrapper_func()
    path, source = get_path_and_source_from_frame(wrapper_frame)
    assert isinstance(source, UnavailableSource)
    assert path == wrapper_frame.f_code.co_filename
