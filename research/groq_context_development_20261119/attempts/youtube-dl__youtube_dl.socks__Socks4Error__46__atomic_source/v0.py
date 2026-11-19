import pytest
from youtube_dl.socks import Socks4Error

def test_socks4_error_constants():
    # Verify that the success code is correctly defined
    assert Socks4Error.ERR_SUCCESS == 90, "ERR_SUCCESS should be 90"

    # Verify that the error codes dictionary contains the expected keys and messages
    expected_codes = {
        91: 'request rejected or failed',
        92: 'request rejected because SOCKS server cannot connect to identd on the client',
        93: 'request rejected because the client program and identd report different user-ids'
    }
    assert Socks4Error.CODES == expected_codes, "CODES dictionary does not match expected mapping"

def test_socks4_error_inheritance_and_message():
    # Instantiate the error with a custom message
    msg = "Custom error message"
    error = Socks4Error(msg)

    # The error should be an instance of Exception and its base classes
    assert isinstance(error, Exception), "Socks4Error should inherit from Exception"
    assert isinstance(error, Socks4Error), "Socks4Error instance should be of its own type"

    # The message should be preserved
    assert str(error) == msg, "Error message should match the provided string"

def test_socks4_error_repr_and_str():
    # Create an error with a specific message
    error = Socks4Error("Test error")
    # The representation should include the class name and the message
    repr_str = repr(error)
    assert "Socks4Error" in repr_str, "repr should contain the class name"
    assert "Test error" in repr_str, "repr should contain the error message"

    # The string conversion should match the message
    assert str(error) == "Test error", "str() should return the error message"
