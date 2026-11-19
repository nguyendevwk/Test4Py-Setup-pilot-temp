import pytest
from youtube_dl.socks import Socks4Error

def test_default_success_code_has_no_error_message():
    """Socks4Error with the success code should not raise an exception and have an empty message."""
    err = Socks4Error(code=Socks4Error.ERR_SUCCESS)
    # The success code should not be considered an error; the message should be empty.
    assert err.code == Socks4Error.ERR_SUCCESS
    assert err.msg == ""

def test_known_error_codes_return_expected_messages():
    """Known error codes should map to the correct human‑readable messages."""
    for code, expected_msg in Socks4Error.CODES.items():
        err = Socks4Error(code=code)
        assert err.code == code
        # The message should be the mapping from CODES.
        assert err.msg == expected_msg

def test_unknown_error_code_falls_back_to_default_message():
    """An unknown error code should result in a generic message containing the code."""
    unknown_code = 999
    err = Socks4Error(code=unknown_code)
    assert err.code == unknown_code
    # The default message should include the numeric code.
    assert str(unknown_code) in err.msg
