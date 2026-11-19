import re
import pytest
from youtube_dl.extractor.nrk import NRKTVDirekteIE

def test_valid_url_regex_matches_expected_patterns():
    """The _VALID_URL regex should match the two example URLs and capture the id part."""
    pattern = re.compile(NRKTVDirekteIE._VALID_URL)
    tv_url = "https://tv.nrk.no/direkte/nrk1"
    radio_url = "https://radio.nrk.no/direkte/p1_oslo_akershus"

    tv_match = pattern.match(tv_url)
    radio_match = pattern.match(radio_url)

    assert tv_match is not None, f"Pattern did not match TV URL: {tv_url}"
    assert radio_match is not None, f"Pattern did not match Radio URL: {radio_url}"
    assert tv_match.group("id") == "nrk1", f"Captured id wrong for TV URL: {tv_match.group('id')}"
    assert radio_match.group("id") == "p1_oslo_akershus", f"Captured id wrong for Radio URL: {radio_match.group('id')}"

def test_test_entries_only_matching_flag():
    """Each test entry in _TESTS should have only_matching set to True."""
    for test in NRKTVDirekteIE._TESTS:
        assert test.get("only_matching") is True, (
            f"Test entry {test} does not have only_matching=True"
        )

def test_inheritance_and_description():
    """NRKTVDirekteIE should inherit from InfoExtractor and have a non-empty description."""
    assert issubclass(NRKTVDirekteIE, NRKTVDirekteIE.__mro__[1]), (
        "NRKTVDirekteIE does not inherit from its parent class"
    )
    assert hasattr(NRKTVDirekteIE, "IE_DESC"), "IE_DESC attribute missing"
    assert isinstance(NRKTVDirekteIE.IE_DESC, str) and NRKTVDirekteIE.IE_DESC, (
        "IE_DESC should be a non-empty string"
    )
