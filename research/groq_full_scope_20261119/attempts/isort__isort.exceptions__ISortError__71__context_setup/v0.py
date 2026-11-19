import pytest
from isort.exceptions import ISortError

def test_isort_error_inherits_exception_and_carries_message():
    """ISortError should inherit from Exception and store the message."""
    err = ISortError("test message")
    assert isinstance(err, Exception)
    assert str(err) == "test message"
    assert err.args == ("test message",)

def test_isort_error_reduce_and_pickle_roundtrip(tmp_path):
    """The __reduce__ method should allow pickling and unpickling to preserve state."""
    import pickle
    original = ISortError("pickle test")
    # Pickle the exception
    data = pickle.dumps(original)
    # Unpickle to a new instance
    restored = pickle.loads(data)
    assert isinstance(restored, ISortError)
    assert str(restored) == "pickle test"
    assert restored.args == original.args

def test_isort_error_with_multiple_arguments():
    """ISortError should accept multiple arguments and store them correctly."""
    err = ISortError("first", 42, {"key": "value"})
    assert isinstance(err, Exception)
    assert err.args == ("first", 42, {"key": "value"})
    assert str(err) == "('first', 42, {'key': 'value'})"
