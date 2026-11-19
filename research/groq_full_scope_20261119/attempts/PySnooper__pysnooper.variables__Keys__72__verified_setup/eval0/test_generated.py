import pytest
from pysnooper.variables import Keys
from pysnooper import utils

def test_keys_and_formatting():
    """Verify that Keys correctly extracts keys and formats them."""
    data = {"a": 1, "b": 2}
    k = Keys()
    # _keys should return the dict's keys view
    keys_view = k._keys(data)
    assert isinstance(keys_view, dict_keys := type(data.keys()))
    assert set(keys_view) == {"a", "b"}
    # _format_key should wrap the shortish repr of the key
    formatted = k._format_key("a")
    assert formatted == "[a]"
    # Ensure that a non-string key is handled via utils.get_shortish_repr
    formatted_int = k._format_key(42)
    assert formatted_int == f"[{utils.get_shortish_repr(42)}]"

def test_get_value_and_missing_key():
    """Ensure _get_value returns the correct value and raises KeyError for missing keys."""
    data = {"x": 10}
    k = Keys()
    # Correct key retrieval
    assert k._get_value(data, "x") == 10
    # Missing key should raise KeyError
    with pytest.raises(KeyError):
        k._get_value(data, "y")

def test_empty_dict_behavior():
    """Test behavior when the main_value is an empty dictionary."""
    empty = {}
    k = Keys()
    # _keys should return an empty view
    assert list(k._keys(empty)) == []
    # _get_value should raise KeyError even though dict is empty
    with pytest.raises(KeyError):
        k._get_value(empty, "anything")
