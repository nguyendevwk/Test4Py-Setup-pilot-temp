import pytest
import requests
from httpie.cli.dicts import HTTPHeadersDict
from httpie.client import apply_missing_repeated_headers


def test_apply_missing_repeated_headers_restores_all_original_values():
    # Original headers contain the same header twice with different values
    original = HTTPHeadersDict([("X-Test", "value1"), ("X-Test", "value2")])
    # Prepared request has only the first value
    prepared = requests.PreparedRequest()
    prepared.headers = {"X-Test": "value1"}
    apply_missing_repeated_headers(original, prepared)
    # After merging, both values should be present
    assert set(prepared.headers.get_all("X-Test")) == {"value1", "value2"}
    # No other headers should be added
    assert len(prepared.headers) == 1


def test_apply_missing_repeated_headers_preserves_non_matching_headers():
    original = HTTPHeadersDict([("X-Only", "foo")])
    prepared = requests.PreparedRequest()
    prepared.headers = {"X-Only": "foo", "X-Other": "bar"}
    apply_missing_repeated_headers(original, prepared)
    # X-Only should remain unchanged
    assert prepared.headers["X-Only"] == "foo"
    # X-Other should also remain unchanged
    assert prepared.headers["X-Other"] == "bar"
    # No new headers should appear
    assert set(prepared.headers.keys()) == {"X-Only", "X-Other"}


def test_apply_missing_repeated_headers_is_case_insensitive_and_preserves_overridden_value():
    original = HTTPHeadersDict([("X-Case", "A"), ("X-Case", "B")])
    prepared = requests.PreparedRequest()
    # Simulate an overridden header value that is not in original
    prepared.headers = {"X-CASE": "C"}
    apply_missing_repeated_headers(original, prepared)
    # Since "C" is not among original values, it should be preserved
    assert prepared.headers["X-CASE"] == "C"
    # Original values should not be added because the current value was overridden
    assert set(prepared.headers.get_all("X-CASE")) == {"C"}
