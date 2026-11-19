import json
import sys
import pytest
from httpie.utils import JsonDictPreservingDuplicateKeys


def test_duplicate_keys_order_and_json_dump(tmp_path):
    # Create a dict with duplicate keys
    items = [("a", 1), ("b", 2), ("a", 3), ("c", 4)]
    jd = JsonDictPreservingDuplicateKeys(items)

    # The items method should return the original list including duplicates
    assert list(jd.items()) == items

    # json.dumps should preserve the order of duplicate keys
    dumped = json.dumps(jd, separators=(",", ":"))
    # The hack key is added, so we expect it at the end
    expected = '{"a":1,"b":2,"a":3,"c":4,"__hack__":"__hack__"}'
    assert dumped == expected

    # Ensure that the hack key is present in the dict
    assert "__hack__" in jd
    assert jd["__hack__"] == "__hack__"


def test_empty_items_adds_hack_key():
    # When no items are provided, the hack key should still be added
    jd = JsonDictPreservingDuplicateKeys([])
    assert list(jd.items()) == [("__hack__", "__hack__")]
    assert "__hack__" in jd
    assert jd["__hack__"] == "__hack__"

    # json.dumps should produce an empty object with the hack key
    dumped = json.dumps(jd, separators=(",", ":"))
    assert dumped == '{"__hack__":"__hack__"}'


def test_supports_sorting_flag_behavior():
    # The SUPPORTS_SORTING flag depends on the Python version
    if sys.version_info >= (3, 8):
        assert JsonDictPreservingDuplicateKeys.SUPPORTS_SORTING is True
    else:
        assert JsonDictPreservingDuplicateKeys.SUPPORTS_SORTING is False

    # When sorting is supported, json.dumps with sort_keys=True should sort unique keys
    items = [("b", 2), ("a", 1), ("b", 3)]
    jd = JsonDictPreservingDuplicateKeys(items)
    dumped = json.dumps(jd, sort_keys=True, separators=(",", ":"))
    # The hack key is added and sorted last because of its name
    expected = '{"__hack__":"__hack__","a":1,"b":2,"b":3}'
    assert dumped == expected
