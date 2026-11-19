import pytest
from tornado.escape import parse_qs_bytes

def test_parse_qs_bytes_basic():
    qs = b"foo=bar&baz=qux&foo=baz"
    result = parse_qs_bytes(qs)
    assert result == {
        "foo": [b"bar", b"baz"],
        "baz": [b"qux"],
    }

def test_parse_qs_bytes_blank_and_strict():
    qs = b"empty=&no_value"
    # keep_blank_values=True allows empty string values
    result = parse_qs_bytes(qs, keep_blank_values=True)
    assert result == {"empty": [b""], "no_value": [b""]}

    # strict_parsing=True raises ValueError for missing '='
    with pytest.raises(ValueError):
        parse_qs_bytes(qs, strict_parsing=True)

def test_parse_qs_bytes_max_num_fields():
    qs = b"a=1&b=2&c=3"
    # max_num_fields=2 should raise ValueError
    with pytest.raises(ValueError):
        parse_qs_bytes(qs, max_num_fields=2)

    # max_num_fields=3 should succeed
    result = parse_qs_bytes(qs, max_num_fields=3)
    assert result == {"a": [b"1"], "b": [b"2"], "c": [b"3"]}
