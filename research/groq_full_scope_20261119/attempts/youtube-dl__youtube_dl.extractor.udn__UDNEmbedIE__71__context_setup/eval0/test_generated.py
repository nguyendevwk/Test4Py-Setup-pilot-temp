import re
import pytest
from youtube_dl.extractor.udn import UDNEmbedIE

def test_valid_url_pattern_matches():
    """The _VALID_URL regex should match known UDN embed URLs."""
    valid_urls = [
        "http://video.udn.com/embed/news/300040",
        "https://video.udn.com/embed/news/123456",
        "http://video.udn.com/play/news/987654",
        "https://video.udn.com/play/news/111111",
    ]
    for url in valid_urls:
        assert re.match(UDNEmbedIE._VALID_URL, url), f"URL did not match: {url}"

def test_match_id_extraction():
    """The extractor should correctly extract the video id from the URL."""
    ie = UDNEmbedIE()
    test_cases = {
        "http://video.udn.com/embed/news/300040": "300040",
        "https://video.udn.com/play/news/987654": "987654",
        "http://video.udn.com/embed/news/123456": "123456",
    }
    for url, expected_id in test_cases.items():
        extracted_id = ie._match_id(url)
        assert extracted_id == expected_id, f"Expected {expected_id}, got {extracted_id}"

def test_invalid_url_raises():
    """An URL that does not match the pattern should raise a ValueError when matched."""
    ie = UDNEmbedIE()
    invalid_urls = [
        "http://example.com/video/123",
        "https://video.udn.com/invalid/123",
        "ftp://video.udn.com/embed/news/123",
        "http://video.udn.com/embed/123",
    ]
    for url in invalid_urls:
        with pytest.raises(ValueError):
            ie._match_id(url)
