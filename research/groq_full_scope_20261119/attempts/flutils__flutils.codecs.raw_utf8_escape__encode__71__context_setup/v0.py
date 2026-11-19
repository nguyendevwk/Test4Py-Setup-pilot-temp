import pytest
from flutils.codecs.raw_utf8_escape import encode

def test_encode_ascii():
    # Plain ASCII text should be returned unchanged as escaped bytes
    text = "Hello, World!"
    out_bytes, consumed = encode(text)
    # The output should be the same string encoded in UTF‑8
    assert out_bytes == text.encode("utf-8")
    # All characters should be consumed
    assert consumed == len(text)

def test_encode_unicode():
    # Unicode characters should be converted to escaped UTF‑8 hex
    text = "Café"  # 'é' is U+00E9
    out_bytes, consumed = encode(text)
    # The output should contain the escaped hex for 'é' (\xc3\xa9)
    assert b"Caf\\xc3\\xa9" == out_bytes
    # All characters should be consumed
    assert consumed == len(text)

def test_encode_invalid_escape():
    # An invalid escape sequence should raise UnicodeEncodeError
    text = "Bad\\xZZ"  # \xZZ is not a valid hex escape
    with pytest.raises(UnicodeEncodeError):
        encode(text)
