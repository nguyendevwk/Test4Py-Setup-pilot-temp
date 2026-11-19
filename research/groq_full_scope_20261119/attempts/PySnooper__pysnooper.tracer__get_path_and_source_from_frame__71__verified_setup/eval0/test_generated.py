import builtins
import inspect
import os
import sys
import types
import tempfile
import importlib.util
import importlib.machinery
import importlib
import pytest

from pysnooper.tracer import get_path_and_source_from_frame, UnavailableSource, source_and_path_cache


def create_module_with_source(tmp_path, name, source_code):
    """Create a temporary module file and import it."""
    file_path = tmp_path / f"{name}.py"
    file_path.write_text(source_code)
    spec = importlib.util.spec_from_file_location(name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module, file_path


def test_get_path_and_source_from_frame_reads_file_source(tmp_path):
    """Frame from a function defined in a real file should return that file path and source lines."""
    source_code = "def foo():\n    return 42\n"
    module, file_path = create_module_with_source(tmp_path, "temp_module", source_code)

    def wrapper():
        return module.foo()

    frame = inspect.currentframe()
    # Move to the frame of wrapper
    while frame.f_code.co_name != "wrapper":
        frame = frame.f_back
    path, source = get_path_and_source_from_frame(frame)
    assert path == str(file_path)
    assert isinstance(source, list)
    assert source[0].strip() == "def foo():"
    assert source[1].strip() == "return 42"


def test_get_path_and_source_from_frame_handles_bytes_source(tmp_path):
    """If the source is read as bytes, it should be decoded correctly."""
    # Create a file with a specific encoding declaration
    source_code = "# coding: latin-1\n" + "def bar():\n    return 'á'\n"
    module, file_path = create_module_with_source(tmp_path, "latin_module", source_code)

    def wrapper():
        return module.bar()

    frame = inspect.currentframe()
    while frame.f_code.co_name != "wrapper":
        frame = frame.f_back
    path, source = get_path_and_source_from_frame(frame)
    assert path == str(file_path)
    assert isinstance(source, list)
    # The decoded string should contain the accented character
    assert source[1].strip() == "return 'á'"


def test_get_path_and_source_from_frame_unavailable_source(tmp_path):
    """When the file cannot be read, an UnavailableSource instance is returned."""
    # Create a module but delete its file to simulate missing source
    module, file_path = create_module_with_source(tmp_path, "missing_module", "def baz():\n    pass\n")
    os.remove(file_path)

    def wrapper():
        return module.baz()

    frame = inspect.currentframe()
    while frame.f_code.co_name != "wrapper":
        frame = frame.f_back
    path, source = get_path_and_source_from_frame(frame)
    assert path == str(file_path)
    assert isinstance(source, UnavailableSource)
