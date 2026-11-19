import json
import pytest
from httpie.utils import JsonDictPreservingDuplicateKeys

def test_preserve_duplicate_keys_and_dump():
    # Create a dict with duplicate keys
    items = [("a", 1), ("b", 2), ("a", 3)]
    jd = JsonDictPreservingDuplicateKeys(items)
    # items() should return the original list including duplicates
    assert jd.items() == items
    # json.dumps should preserve the order and duplicates
    dumped = json.dumps(jd, separators=(",", ":"))
    # The output must contain both "a" keys in order
    assert dumped == '{"a":1,"b":2,"a":3}'
    # The hack key should not appear in the output
    assert "__hack__" not in dumped

def test_empty_items():
    # Empty list should still create a dict with the hack key
    jd = JsonDictPreservingDuplicateKeys([])
    # items() should return the empty list
    assert jd.items() == []
    # json.dumps should produce an empty object
    assert json.dumps(jd, separators=(",", ":")) == "{}"

def test_invalid_initialization():
    # Passing a non-list (e.g., None) should raise a TypeError
    with pytest.raises(TypeError):
        JsonDictPreservingDuplicateKeys(None)
