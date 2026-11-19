import pytest
from httpie.uploads import as_bytes

def test_as_bytes_with_string_encodes_to_bytes():
    """String input should be encoded to UTF‑8 bytes."""
    original = "hello, 世界"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == original.encode("utf-8")
    # Ensure the original string is unchanged
    assert original == "hello, 世界"

def test_as_bytes_with_bytes_returns_same_object():
    """Bytes input should be returned unchanged and preserve identity."""
    original = b"binary data"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == original
    # Identity check: the same object should be returned
    assert result is original

def test_as_bytes_with_invalid_type_returns_input_unmodified():
    """Passing a non‑str/bytes type should return the input unchanged."""
    class Dummy:
        pass
    dummy = Dummy()
    result = as_bytes(dummy)
    assert result is dummy
    # The function does not raise an exception for unsupported types
    with pytest.raises(TypeError):
        # Force a type error by attempting to use the result as bytes
        dummy_bytes = result + b"extra"
