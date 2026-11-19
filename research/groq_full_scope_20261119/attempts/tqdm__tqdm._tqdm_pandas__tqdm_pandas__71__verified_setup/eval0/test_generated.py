import warnings
import sys
import types
import pytest

from tqdm._tqdm_pandas import tqdm_pandas


def test_tqdm_pandas_with_class_triggers_deprecation_and_calls_pandas(tmp_path):
    """Passing a class with a name starting with 'tqdm_' should trigger the
    deprecation warning and call the class's pandas method."""
    class DummyTqdm:
        called = False

        @classmethod
        def pandas(cls, **kwargs):
            cls.called = True
            cls.kwargs = kwargs

    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        tqdm_pandas(DummyTqdm, desc="test", file=sys.stderr)

        # Verify deprecation warning was issued
        assert any(
            issubclass(exc.category, UserWarning) and
            "Please use `tqdm.pandas(...)`" in str(exc.message)
            for exc in w
        ), "Expected deprecation warning not found"

    # Verify pandas was called with the provided kwargs
    assert DummyTqdm.called is True
    assert DummyTqdm.kwargs == {"desc": "test", "file": sys.stderr}


def test_tqdm_pandas_with_instance_triggers_deprecation_and_calls_pandas(tmp_path):
    """Passing an instance with a 'fp' attribute should trigger the
    deprecation warning and call the instance's class pandas method."""
    class DummyTqdm:
        called = False

        @classmethod
        def pandas(cls, **kwargs):
            cls.called = True
            cls.kwargs = kwargs

    instance = DummyTqdm()
    instance.fp = sys.stderr

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        tqdm_pandas(instance, total=10)

        # Verify deprecation warning was issued
        assert any(
            issubclass(exc.category, UserWarning) and
            "Please use `tqdm.pandas(...)`" in str(exc.message)
            for exc in w
        ), "Expected deprecation warning not found"

    # Verify pandas was called on the class of the instance
    assert DummyTqdm.called is True
    assert DummyTqdm.kwargs == {"total": 10}


def test_tqdm_pandas_with_nonclass_and_noninstance_raises_attribute_error():
    """Passing an object that is neither a class nor an instance with a 'fp'
    attribute should raise an AttributeError when accessing 'fp'."""
    class Dummy:
        pass

    dummy = Dummy()
    # dummy has no 'fp' attribute; accessing it should raise AttributeError
    with pytest.raises(AttributeError):
        tqdm_pandas(dummy, total=5)
