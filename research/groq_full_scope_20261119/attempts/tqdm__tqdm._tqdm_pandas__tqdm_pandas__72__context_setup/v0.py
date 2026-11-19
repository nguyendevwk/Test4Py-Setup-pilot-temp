import sys
import pytest
from tqdm._tqdm_pandas import tqdm_pandas
from tqdm import TqdmDeprecationWarning

class DummyTqdmType:
    def __init__(self):
        self.pandas_called_with = None

    @classmethod
    def pandas(cls, **kwargs):
        cls.pandas_called_with = kwargs

class DummyInstance:
    def __init__(self):
        self.pandas_called_with = None

    def pandas(self, **kwargs):
        self.pandas_called_with = kwargs

def test_tqdm_pandas_with_type(tmp_path):
    """When tclass is a type, pandas is called on the class with kwargs."""
    dummy_file = tmp_path / "log.txt"
    dummy_file.write_text("")
    kwargs = {"file": dummy_file.open("w"), "desc": "test"}
    with pytest.warns(TqdmDeprecationWarning) as record:
        tqdm_pandas(DummyTqdmType, **kwargs)
    # Ensure warning message is correct
    assert any("Please use `tqdm.pandas(...)" in str(w.message) for w in record)
    # Verify pandas was called on the class with the same kwargs
    assert DummyTqdmType.pandas_called_with == kwargs
    # Ensure the file write function used in warning is the same as provided
    assert record[0].fp_write == kwargs["file"].write

def test_tqdm_pandas_with_instance(tmp_path):
    """When tclass is an instance, pandas is called on the instance with kwargs."""
    dummy_file = tmp_path / "log2.txt"
    dummy_file.write_text("")
    kwargs = {"file": dummy_file.open("w"), "desc": "instance"}
    instance = DummyInstance()
    with pytest.warns(TqdmDeprecationWarning) as record:
        tqdm_pandas(instance, **kwargs)
    # Ensure warning message is correct
    assert any("Please use `tqdm.pandas(...)" in str(w.message) for w in record)
    # Verify pandas was called on the instance with the same kwargs
    assert instance.pandas_called_with == kwargs
    # Ensure the file write function used in warning is the same as provided
    assert record[0].fp_write == kwargs["file"].write

def test_tqdm_pandas_missing_pandas():
    """If tclass lacks a pandas method, AttributeError is raised."""
    class NoPandas:
        pass
    with pytest.raises(AttributeError):
        tqdm_pandas(NoPandas())
