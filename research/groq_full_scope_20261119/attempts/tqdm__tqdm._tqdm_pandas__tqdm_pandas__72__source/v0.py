import sys
import io
import types
import pytest
from tqdm._tqdm_pandas import tqdm_pandas


class DummyClass:
    def __init__(self):
        self.pandas_called = False
        self.pandas_kwargs = None

    def pandas(self, **kwargs):
        self.pandas_called = True
        self.pandas_kwargs = kwargs


class DummyInstance:
    def __init__(self):
        self.fp = io.StringIO()
        self.pandas_called = False
        self.pandas_kwargs = None

    def pandas(self, **kwargs):
        self.pandas_called = True
        self.pandas_kwargs = kwargs


def test_tqdm_pandas_with_type_and_kwargs(tmp_path):
    """When tclass is a type, pandas is called with provided kwargs."""
    dummy = DummyClass()
    # Use a temporary file to capture warning output
    warning_file = tmp_path / "warning.txt"
    with warning_file.open("w") as f:
        tqdm_pandas(DummyClass, desc="test", file=f)
    # Verify pandas was called once with the kwargs
    assert dummy.pandas_called is False  # DummyClass.pandas not called on class
    # Instead, the class method should be called; we test by monkeypatching
    # the class's pandas method
    called = {"called": False, "kwargs": None}

    def fake_pandas(**kwargs):
        called["called"] = True
        called["kwargs"] = kwargs

    DummyClass.pandas = fake_pandas
    tqdm_pandas(DummyClass, desc="test", file=f)
    assert called["called"] is True
    assert called["kwargs"] == {"desc": "test"}


def test_tqdm_pandas_with_instance_and_fp(tmp_path):
    """When tclass is an instance with fp, pandas is called on its type."""
    instance = DummyInstance()
    warning_file = tmp_path / "warning.txt"
    with warning_file.open("w") as f:
        tqdm_pandas(instance, desc="inst_test", file=f)
    # Verify that the type's pandas was called with deprecated_t
    called = {"called": False, "kwargs": None}

    def fake_pandas(**kwargs):
        called["called"] = True
        called["kwargs"] = kwargs

    type(instance).pandas = fake_pandas
    tqdm_pandas(instance, desc="inst_test", file=f)
    assert called["called"] is True
    assert called["kwargs"] == {"deprecated_t": instance}


def test_tqdm_pandas_warning_output(tmp_path):
    """Ensure that the deprecation warning writes to the provided file."""
    dummy = DummyClass()
    warning_file = tmp_path / "warning.txt"
    with warning_file.open("w") as f:
        tqdm_pandas(DummyClass, desc="warn_test", file=f)
    # Read the warning file to confirm content
    content = warning_file.read_text()
    assert "Please use `tqdm.pandas(...)" in content
    assert "tqdm_pandas(tqdm, ...)" in content
