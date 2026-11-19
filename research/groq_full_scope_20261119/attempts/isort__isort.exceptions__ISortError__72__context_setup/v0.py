import pytest
from isort.exceptions import ISortError
from functools import partial
import pickle

def test_isort_error_message_and_inheritance():
    """Verify that ISortError behaves like a normal exception with a custom message."""
    msg = "Custom error message"
    exc = ISortError(msg)
    # The exception should store the message in its args
    assert exc.args == (msg,)
    # It should be an instance of Exception and ISortError
    assert isinstance(exc, Exception)
    assert isinstance(exc, ISortError)
    # Raising and catching should preserve the message
    with pytest.raises(ISortError) as excinfo:
        raise exc
    assert str(excinfo.value) == msg

def test_isort_error_reduce_and_pickle():
    """Ensure that ISortError can be pickled and unpickled correctly via __reduce__."""
    original = ISortError("Pickle test")
    # Pickle the exception
    data = pickle.dumps(original)
    # Unpickle to get a new instance
    restored = pickle.loads(data)
    # The restored instance should be equal in type and message
    assert isinstance(restored, ISortError)
    assert restored.args == original.args
    # The __reduce__ method should return a callable that recreates the instance
    reduce_call, reduce_args = original.__reduce__()
    # The callable should be a partial of the exception type
    assert isinstance(reduce_call, partial)
    assert reduce_call.func is type(original)
    # Calling the partial should produce an equivalent exception
    recreated = reduce_call(*reduce_args)
    assert isinstance(recreated, ISortError)
    assert recreated.args == original.args

def test_isort_error_boundary_empty_message():
    """Test the boundary case where the exception is instantiated with no message."""
    exc = ISortError()
    # The args tuple should be empty
    assert exc.args == ()
    # The string representation should be empty
    assert str(exc) == ""
    # Pickling and unpickling should preserve the empty state
    data = pickle.dumps(exc)
    restored = pickle.loads(data)
    assert isinstance(restored, ISortError)
    assert restored.args == ()
