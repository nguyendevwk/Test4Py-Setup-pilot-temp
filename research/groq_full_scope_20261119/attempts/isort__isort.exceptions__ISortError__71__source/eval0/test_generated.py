import pytest
from isort.exceptions import ISortError


def test_isort_error_inherits_exception_and_carries_message():
    """ISortError should be a subclass of Exception and preserve its message."""
    err = ISortError("sample error")
    assert isinstance(err, Exception)
    assert str(err) == "sample error"
    assert err.args == ("sample error",)


def test_isort_error_reduce_and_reconstruct():
    """The __reduce__ method should allow pickling and reconstruction of the error."""
    original = ISortError("reconstruct me")
    # Simulate pickling by calling __reduce__ and then reconstructing
    constructor, args = original.__reduce__()
    reconstructed = constructor(*args)
    assert isinstance(reconstructed, ISortError)
    assert str(reconstructed) == "reconstruct me"
    assert reconstructed.args == original.args


def test_isort_error_without_message():
    """ISortError can be instantiated without a message and still behaves like Exception."""
    err = ISortError()
    assert isinstance(err, Exception)
    assert str(err) == ""
    assert err.args == ()
