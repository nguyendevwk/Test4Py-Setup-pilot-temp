import warnings
import pytest
from tqdm._tqdm_pandas import tqdm_pandas
from tqdm import TqdmDeprecationWarning


def test_tqdm_pandas_with_class_triggers_deprecation_and_pandas_call(tmp_path):
    # Dummy class that mimics a tqdm class with a pandas method
    class DummyTqdm:
        called = False

        @classmethod
        def pandas(cls, **kwargs):
            cls.called = True
            cls.kwargs = kwargs

    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", TqdmDeprecationWarning)
        tqdm_pandas(DummyTqdm, desc="test", total=10)

        # Verify deprecation warning was issued
        assert any(
            issubclass(exc.category, TqdmDeprecationWarning)
            and "Please use `tqdm.pandas(...)" in str(exc.message)
            for exc in w
        )

    # Verify pandas was called with the provided kwargs
    assert DummyTqdm.called is True
    assert DummyTqdm.kwargs == {"desc": "test", "total": 10}


def test_tqdm_pandas_with_instance_triggers_deprecation_and_pandas_call(tmp_path):
    # Dummy instance with fp attribute having write method
    class DummyFP:
        def write(self, msg):
            self.last_msg = msg

    class DummyInstance:
        fp = DummyFP()

        @classmethod
        def pandas(cls, deprecated_t=None):
            cls.called = True
            cls.deprecated_t = deprecated_t

    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", TqdmDeprecationWarning)
        tqdm_pandas(DummyInstance(), bar_format="{}")

        # Verify deprecation warning was issued
        assert any(
            issubclass(exc.category, TqdmDeprecationWarning)
            and "Please use `tqdm.pandas(...)" in str(exc.message)
            for exc in w
        )

    # Verify pandas was called on the class with deprecated_t argument
    assert DummyInstance.called is True
    assert isinstance(DummyInstance.deprecated_t, DummyInstance)


def test_tqdm_pandas_with_invalid_instance_raises_attribute_error():
    # Instance lacking fp attribute should raise AttributeError
    class BadInstance:
        pass

    with pytest.raises(AttributeError):
        tqdm_pandas(BadInstance())
