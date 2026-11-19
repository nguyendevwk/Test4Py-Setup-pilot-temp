import re
import pytest
from youtube_dl.extractor.konserthusetplay import KonserthusetPlayIE
from youtube_dl.utils import determine_ext, int_or_none, float_or_none, url_or_none

def test_match_id_extraction():
    """Verify that the extractor correctly extracts the video id from a URL."""
    extractor = KonserthusetPlayIE()
    url = "https://www.konserthusetplay.se/?m=CKDDnlCY-dhWAAqiMERd-A"
    video_id = extractor._match_id(url)
    assert video_id == "CKDDnlCY-dhWAAqiMERd-A"

def test_search_regex_and_fallback():
    """Test that _search_regex correctly finds patterns and returns defaults."""
    extractor = KonserthusetPlayIE()
    sample_text = (
        '... https://csp.picsearch.com/rest?e=abc123&containerId=mediaplayer&i=object ...'
        '... fallbackUrl="https://example.com/video_h264m.mp4" ...'
    )
    # Extract the 'e' parameter
    e_value = extractor._search_regex(r'e=([^&]+)', sample_text, 'e')
    assert e_value == "abc123"

    # Extract format id from fallback URL
    format_id = extractor._search_regex(
        r'_([^_]+)_h264m\.mp4', sample_text, 'format id', default=None)
    assert format_id == "video"

    # When pattern not found, default should be returned
    missing = extractor._search_regex(r'nonexistent', sample_text, 'missing', default="none")
    assert missing == "none"

def test_util_functions_and_edge_cases():
    """Ensure utility functions handle edge cases correctly."""
    # determine_ext should return 'm3u8' for a typical HLS URL
    assert determine_ext("https://example.com/playlist.m3u8") == "m3u8"

    # int_or_none should convert numeric strings and return None for invalid
    assert int_or_none("123") == 123
    assert int_or_none("abc") is None
    assert int_or_none(None) is None

    # float_or_none should convert numeric strings with optional multiplier
    assert float_or_none("398.76", 1000) == 398.76
    assert float_or_none("398.76", 1) == 398.76
    assert float_or_none("abc", 1000) is None
    assert float_or_none(None, 1000) is None

    # url_or_none should return None for invalid URLs
    assert url_or_none("http://valid.url") == "http://valid.url"
    assert url_or_none("not a url") is None
    assert url_or_none(None) is None
