import os
import types
import inspect
import pytest
from pysnooper.tracer import get_path_and_source_from_frame, UnavailableSource

def test_get_path_and_source_from_frame_reads_file(tmp_path):
    # Create a temporary Python file with known content
    py_file = tmp_path / "sample.py"
    content = "def foo():\n    return 42\n"
    py_file.write_text(content, encoding="utf-8")

    # Define a function in that file and get its frame
    def load_and_call():
        # Import the temporary module
        import importlib.util
        spec = importlib.util.spec_from_file_location("sample", str(py_file))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.foo()

    # Execute the function to get a frame
    try:
        load_and_call()
    except Exception:
        # Capture the frame from the exception
        frame = inspect.currentframe()
    else:
        # If no exception, get the frame of the function itself
        frame = load_and_call.__code__.co_firstlineno

    # Use the actual frame object
    frame_obj = inspect.currentframe()
    # Find the frame where foo was defined
    while frame_obj and frame_obj.f_code.co_name != "foo":
        frame_obj = frame_obj.f_back
    assert frame_obj is not None

    file_name, source = get_path_and_source_from_frame(frame_obj)
    assert file_name == str(py_file)
    assert isinstance(source, list)
    assert source[0].strip() == "def foo():"
    assert source[1].strip() == "return 42"

def test_get_path_and_source_from_frame_handles_bytes_source(tmp_path):
    # Create a temporary file with bytes content
    py_file = tmp_path / "bytes.py"
    content_bytes = b"def bar():\n    return 'hello'\n"
    py_file.write_bytes(content_bytes)

    # Define a function that reads this file and returns its frame
    def read_and_call():
        with open(py_file, "rb") as f:
            exec(f.read(), {})
        return 0

    # Execute to get a frame
    try:
        read_and_call()
    except Exception:
        frame = inspect.currentframe()
    else:
        frame = read_and_call.__code__.co_firstlineno

    # Find the frame of the exec'ed function
    frame_obj = inspect.currentframe()
    while frame_obj and frame_obj.f_code.co_name != "<module>":
        frame_obj = frame_obj.f_back
    assert frame_obj is not None

    file_name, source = get_path_and_source_from_frame(frame_obj)
    assert file_name == str(py_file)
    assert isinstance(source, list)
    assert all(isinstance(line, str) for line in source)
    assert source[0].strip() == "def bar():"
    assert source[1].strip() == "return 'hello'"

def test_get_path_and_source_from_frame_returns_unavailable_on_missing_file():
    # Create a dummy code object with a non-existent filename
    code = types.CodeType(
        0, 0, 0, 0, 0, b"", (), (), (), (), "nonexistent.py", "nonexistent.py", 0, b""
    )
    dummy_func = types.FunctionType(code, {})
    frame = dummy_func.__code__.co_firstlineno
    # Build a fake frame object
    fake_frame = types.SimpleNamespace(
        f_globals={}, f_code=code, f_back=None
    )
    file_name, source = get_path_and_source_from_frame(fake_frame)
    assert file_name == "nonexistent.py"
    assert isinstance(source, UnavailableSource)
