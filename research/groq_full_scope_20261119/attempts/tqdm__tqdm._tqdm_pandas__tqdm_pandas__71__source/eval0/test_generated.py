import sys
import io
import types
import pytest
from tqdm._tqdm_pandas import tqdm_pandas


class DummyClass:
    def __init__(self):
        self.pandas_called_with = None

    def pandas(self, **kwargs):
        self.pandas_called_with = kwargs


class DummyInstance:
    def __init__(self):
        self.fp = io.StringIO()
        self.pandas_called_with = None

    def pandas(self, **kwargs):
        self.pandas_called_with = kwargs


def test_tqdm_pandas_with_class_triggers_deprecation_and_calls_pandas(tmp_path):
    dummy = DummyClass()
    # Capture stderr to verify warning message
    stderr = io.StringIO()
    with pytest.raises(SystemExit) if hasattr(dummy, "pandas") else None:
        with pytest.redirect_stderr(stderr):
            tqdm_pandas(DummyClass, desc="test", total=10)
    # The warning should mention using tqdm.pandas
    warning_output = stderr.getvalue()
    assert "Please use `tqdm.pandas(...)" in warning_output
    # pandas should be called with the provided kwargs
    assert dummy.pandas_called_with == {"desc": "test", "total": 10}


def test_tqdm_pandas_with_instance_triggers_deprecation_and_calls_pandas(tmp_path):
    dummy = DummyInstance()
    stderr = io.StringIO()
    with pytest.redirect_stderr(stderr):
        tqdm_pandas(dummy, desc="instance", total=5)
    warning_output = stderr.getvalue()
    assert "Please use `tqdm.pandas(...)" in warning_output
    # pandas should be called with deprecated_t pointing to the instance
    assert dummy.pandas_called_with == {"deprecated_t": dummy}


def test_tqdm_pandas_with_nonclass_object_triggers_second_branch(tmp_path):
    class NonClass:
        def __init__(self):
            self.fp = io.StringIO()
            self.pandas_called_with = None

        def pandas(self, **kwargs):
            self.pandas_called_with = kwargs

    obj = NonClass()
    stderr = io.StringIO()
    with pytest.redirect_stderr(stderr):
        tqdm_pandas(obj, desc="nonclass", total=3)
    warning_output = stderr.getvalue()
    assert "Please use `tqdm.pandas(...)" in warning_output
    # pandas should be called with deprecated_t pointing to the object
    assert obj.pandas_called_with == {"deprecated_t": obj}
