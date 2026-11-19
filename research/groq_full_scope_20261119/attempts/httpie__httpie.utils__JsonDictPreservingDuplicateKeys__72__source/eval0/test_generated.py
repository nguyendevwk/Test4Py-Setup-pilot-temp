import json
import pytest
from httpie.utils import JsonDictPreservingDuplicateKeys


def test_preserve_duplicate_keys_and_order(tmp_path):
    # Duplicate keys with different values
    items = [
        ("a", 1),
        ("b", 2),
        ("a", 3),  # duplicate key
        ("c", 4),
    ]
    jd = JsonDictPreservingDuplicateKeys(items)

    # The internal items should be exactly as provided
    assert list(jd.items()) == items

    # json.dumps should output the keys in the original order, including duplicates
    dumped = json.dumps(jd, separators=(",", ":"))
    # Expected string: {"a":1,"b":2,"a":3,"c":4}
    assert dumped == '{"a":1,"b":2,"a":3,"c":4}'

    # When sorting is supported, json.dumps with sort_keys=True should still preserve duplicates
    if JsonDictPreservingDuplicateKeys.SUPPORTS_SORTING:
        sorted_dump = json.dumps(jd, sort_keys=True, separators=(",", ":"))
        # Sorted keys: a, a, b, c
        assert sorted_dump == '{"a":1,"a":3,"b":2,"c":4}'


def test_empty_items_behavior():
    # Empty list of items should still create a dict with the hack key
    jd = JsonDictPreservingDuplicateKeys([])
    # The hack key is added to satisfy both JSON encoders
    assert "__hack__" in jd
    assert jd["__hack__"] == "__hack__"

    # json.dumps should produce an empty object (hack key is removed by items method)
    dumped = json.dumps(jd, separators=(",", ":"))
    assert dumped == "{}"


def test_invalid_items_raises():
    # Passing None should cause json.dumps to raise a TypeError because items() returns None
    jd = JsonDictPreservingDuplicateKeys(None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        json.dumps(jd, separators=(",", ":"))
