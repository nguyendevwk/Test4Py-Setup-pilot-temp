import json
import sys
import pytest
from httpie.utils import JsonDictPreservingDuplicateKeys

def test_preserves_duplicate_keys_and_json_output(tmp_path):
    # Create a dict with duplicate keys
    items = [("a", 1), ("b", 2), ("a", 3)]
    jd = JsonDictPreservingDuplicateKeys(items)
    # The internal items should match the input
    assert list(jd.items()) == items
    # json.dumps should preserve the order and duplicates
    dumped = json.dumps(jd, separators=(",", ":"))
    # The output should contain both "a" keys in order
    assert dumped == '{"a":1,"b":2,"a":3}'
    # Ensure that the hack key is not present in the output
    assert "__hack__" not in dumped

def test_empty_items_adds_hack_key_and_json_output():
    # Empty items list
    items = []
    jd = JsonDictPreservingDuplicateKeys(items)
    # The internal items should contain only the hack key
    assert list(jd.items()) == [("__hack__", "__hack__")]
    # json.dumps should produce an empty object
    dumped = json.dumps(jd, separators=(",", ":"))
    assert dumped == "{}"

def test_constructor_with_invalid_items_type_raises_type_error():
    # Passing a non-list (e.g., a dict) should raise a TypeError
    with pytest.raises(TypeError):
        JsonDictPreservingDuplicateKeys({"a": 1})
