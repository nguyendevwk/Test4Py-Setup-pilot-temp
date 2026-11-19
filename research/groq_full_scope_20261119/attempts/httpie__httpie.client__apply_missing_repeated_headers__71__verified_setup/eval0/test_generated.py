import pytest
import requests
from httpie.cli.dicts import HTTPHeadersDict
from httpie.client import apply_missing_repeated_headers


def test_apply_missing_repeated_headers_preserves_overridden_value(tmp_path):
    # Original headers contain two occurrences of "X-Test" with different values
    original = HTTPHeadersDict([("X-Test", "value1"), ("X-Test", "value2")])
    # Prepare a request that overrides the second value
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"X-Test": "value2", "Other": "foo"},
    )
    prepared = req.prepare()
    # Apply the function
    apply_missing_repeated_headers(original, prepared)
    # The overridden value should remain, but the original first value should be restored
    assert prepared.headers["X-Test"] == "value1"
    assert prepared.headers["Other"] == "foo"


def test_apply_missing_repeated_headers_no_change_when_not_present(tmp_path):
    original = HTTPHeadersDict([("X-Only", "foo")])
    req = requests.Request(method="GET", url="http://example.com")
    prepared = req.prepare()
    apply_missing_repeated_headers(original, prepared)
    # No header was present, so nothing should change
    assert "X-Only" not in prepared.headers
    assert prepared.headers == {}


def test_apply_missing_repeated_headers_case_insensitivity(tmp_path):
    original = HTTPHeadersDict([("X-Case", "upper"), ("x-case", "lower")])
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"X-CASE": "upper"},
    )
    prepared = req.prepare()
    apply_missing_repeated_headers(original, prepared)
    # The function should treat header names case‑insensitively and restore all original values
    assert prepared.headers["X-Case"] == "upper"
    assert prepared.headers["x-case"] == "lower"
