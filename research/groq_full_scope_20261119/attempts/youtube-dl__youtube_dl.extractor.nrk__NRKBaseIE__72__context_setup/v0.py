import re
import random
import pytest
from youtube_dl.extractor.nrk import NRKBaseIE
from youtube_dl.utils import ExtractorError

class DummyNRKIE(NRKBaseIE):
    """A test subclass that overrides network‑dependent methods."""
    def __init__(self):
        super().__init__()
        self.geo_restricted_called = False
        self.geo_restricted_msg = None
        self.geo_restricted_countries = None

    # Override to avoid real network calls
    def _download_json(self, url, video_id, note=None, fatal=True, query=None, headers=None):
        return {}

    # Capture geo‑restricted calls
    def raise_geo_restricted(self, msg=None, countries=None):
        self.geo_restricted_called = True
        self.geo_restricted_msg = msg
        self.geo_restricted_countries = countries

    # Stub format extraction methods
    def _extract_akamai_formats(self, asset_url, video_id):
        return [{'format_id': 'akamai', 'url': asset_url}]

    def _extract_m3u8_formats(self, asset_url, video_id, ext, protocol, fatal=True):
        return [{'format_id': 'm3u8', 'url': asset_url}]


def test_raise_error_program_rights():
    """_raise_error should raise ExtractorError with the correct message."""
    ie = DummyNRKIE()
    data = {'messageType': 'ProgramRightsAreNotReady'}
    with pytest.raises(ExtractorError) as excinfo:
        ie._raise_error(data)
    assert "Du kan dessverre ikke se eller høre programmet" in str(excinfo.value)


def test_raise_error_geo_blocked():
    """_raise_error should trigger raise_geo_restricted for geo‑blocked messages."""
    ie = DummyNRKIE()
    data = {'messageType': 'ProgramIsGeoBlocked'}
    with pytest.raises(ExtractorError):
        ie._raise_error(data)
    assert ie.geo_restricted_called is True
    assert ie.geo_restricted_msg == "NRK har ikke rettigheter til å vise dette programmet utenfor Norge"
    assert ie.geo_restricted_countries == ie._GEO_COUNTRIES


def test_extract_nrk_formats_cdn_and_akamai(tmp_path):
    """_extract_nrk_formats should handle Akamai URLs and CDN replacements."""
    ie = DummyNRKIE()
    video_id = 'testvideo'

    # Akamai URL path
    akamai_url = 'https://example.akamaihd.net/i/test.m3u8'
    formats = ie._extract_nrk_formats(akamai_url, video_id)
    assert formats == [{'format_id': 'akamai', 'url': akamai_url}]

    # Non‑Akamai URL that matches CDN regex
    cdn_url = 'https://nrkod1-akamized.net/47115-cacheod0/stream.m3u8'
    # Ensure the regex matches
    assert re.search(ie._CDN_REPL_REGEX, cdn_url)
    formats = ie._extract_nrk_formats(cdn_url, video_id)
    # Should return the m3u8 format from the original URL
    assert formats == [{'format_id': 'm3u8', 'url': cdn_url}]
