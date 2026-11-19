import json
import pytest
from httpie.utils import JsonDictPreservingDuplicateKeys


def test_preserves_duplicate_keys_and_serializes_correctly():
    # Duplicate keys are preserved in the internal list
    items = [("a", 1), ("b", 2), ("a", 3)]
    jd = JsonDictPreservingDuplicateKeys(items)
    # The internal items list should match the original
    assert list(jd.items()) == items
    # json.dumps should output the keys in the order they were added,
    # including duplicates, and the hack key should be present
    dumped = json.dumps(jd, sort_keys=False)
    # The hack key is added to satisfy the C implementation
    assert "__hack__" in dumped
    # The order of keys in the JSON string should reflect the original order
    # (excluding the hack key which appears last)
    assert dumped.startswith('{"a":1,"b":2,"a":3')
    # Ensure that the hack key appears after the original keys
    assert dumped.rfind('"__hack__"') > dumped.rfind('"a":3')


def test_empty_items_do_not_add_hack_key_and_dump_empty_object():
    # When no items are provided, the hack key should not be added
    jd = JsonDictPreservingDuplicateKeys([])
    assert list(jd.items()) == []
    dumped = json.dumps(jd, sort_keys=False)
    # The output should be an empty JSON object
    assert dumped == "{}"


def test_constructor_raises_type_error_on_invalid_items():
    # Passing a non-iterable (e.g., None) should raise a TypeError
    with pytest.raises(TypeError):
        JsonDictPreservingDuplicateKeys(None)
