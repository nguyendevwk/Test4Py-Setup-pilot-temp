import re
import pytest
from youtube_dl.extractor.zdf import ZDFChannelIE, ZDFIE


def test_suitable_channel_url():
    """ZDFChannelIE should be suitable for a channel URL but not for a ZDFIE URL."""
    channel_url = "https://www.zdf.de/sport/das-aktuelle-sportstudio"
    zdfie_url = "https://www.zdf.de/video/12345"

    assert ZDFChannelIE.suitable(channel_url) is True
    assert ZDFIE.suitable(zdfie_url) is True
    # ZDFChannelIE should not claim suitability for a URL that ZDFIE claims
    assert ZDFChannelIE.suitable(zdfie_url) is False


def test_match_id_extraction():
    """_match_id should correctly extract the ID part from a ZDF channel URL."""
    url = "https://www.zdf.de/sport/das-aktuelle-sportstudio"
    expected_id = "das-aktuelle-sportstudio"

    extractor = ZDFChannelIE()
    extracted_id = extractor._match_id(url)

    assert extracted_id == expected_id
    # The extracted ID should match the regex group in _VALID_URL
    pattern = re.compile(ZDFChannelIE._VALID_URL)
    match = pattern.search(url)
    assert match is not None
    assert match.group("id") == expected_id


def test_invalid_url_rejection():
    """ZDFChannelIE should not be suitable for URLs that do not match its pattern."""
    invalid_url = "https://www.zdf.de/filme/taunuskrimi/"
    # The URL ends with a slash and has no ID segment; suitable should be False
    assert ZDFChannelIE.suitable(invalid_url) is False
