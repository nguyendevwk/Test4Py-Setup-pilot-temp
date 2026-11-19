import pytest
import warnings
from tqdm._tqdm_pandas import tqdm_pandas
from tqdm import TqdmDeprecationWarning


class DummyClass:
    def __init__(self):
        self.pandas_called = False
        self.pandas_kwargs = None

    def pandas(self, **kwargs):
        self.pandas_called = True
        self.pandas_kwargs = kwargs


class DummyInstance:
    def __init__(self):
        self.fp = DummyFile()
        self.deprecated_t = None

    def pandas(self, **kwargs):
        # This method should not be called for instance case
        raise RuntimeError("Instance pandas should not be called")


class DummyFile:
    def __init__(self):
        self.written = []

    def write(self, msg):
        self.written.append(msg)


def test_tqdm_pandas_with_class_triggers_warning_and_calls_pandas(tmp_path):
    dummy = DummyClass()
    with pytest.warns(TqdmDeprecationWarning, match="Please use `tqdm.pandas`"):
        tqdm_pandas(DummyClass, desc="test")
    assert dummy.pandas_called, "pandas method on class was not called"
    assert dummy.pandas_kwargs == {"desc": "test"}


def test_tqdm_pandas_with_instance_triggers_warning_and_calls_pandas_on_type(tmp_path):
    dummy = DummyInstance()
    with pytest.warns(TqdmDeprecationWarning, match="Please use `tqdm.pandas`"):
        tqdm_pandas(dummy, total=10)
    # The instance's pandas should not be called; instead type(dummy).pandas is called
    # Since DummyInstance has no pandas on type, we expect no error but no call
    # Ensure no exception and warning emitted
    assert dummy.deprecated_t is None, "deprecated_t should remain None"


def test_tqdm_pandas_with_nonclass_noninstance_triggers_warning_and_calls_type_pandas(tmp_path):
    class Custom:
        def __init__(self):
            self.fp = DummyFile()
            self.deprecated_t = None

        def pandas(self, **kwargs):
            self.deprecated_t = kwargs

    custom = Custom()
    with pytest.warns(TqdmDeprecationWarning, match="Please use `tqdm.pandas`"):
        tqdm_pandas(custom, bar_format="{}")
    assert custom.deprecated_t == {"bar_format": "{}"}, "type pandas was not called with correct kwargs"
