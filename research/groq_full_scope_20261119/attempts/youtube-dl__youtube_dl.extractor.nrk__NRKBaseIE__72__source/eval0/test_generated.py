import re
import random
import pytest
from youtube_dl.extractor.nrk import NRKBaseIE


class DummyNRKIE(NRKBaseIE):
    """A minimal subclass that records calls to raise_geo_restricted and
    replaces format extraction methods with deterministic stubs."""
    def __init__(self):
        super().__init__()
        self.geo_restricted_called = False
        self.geo_restricted_msg = None
        self.geo_restricted_countries = None

    def raise_geo_restricted(self, msg=None, countries=None):
        self.geo_restricted_called = True
        self.geo_restricted_msg = msg
        self.geo_restricted_countries = countries

    def _extract_akamai_formats(self, asset_url, video_id):
        return [{'format_id': 'akamai', 'url': asset_url}]

    def _extract_m3u8_formats(self, asset_url, video_id, ext, parser, fatal):
        return [{'format_id': 'm3u8', 'url': asset_url}]


def test_raise_error_geo_blocked(monkeypatch):
    """_raise_error should call raise_geo_restricted for geo‑blocked messages."""
    ie = DummyNRKIE()
    data = {'messageType': 'ProgramIsGeoBlocked'}
    with pytest.raises(Exception) as excinfo:
        ie._raise_error(data)
    assert ie.geo_restricted_called
    assert ie.geo_restricted_msg == 'NRK har ikke rettigheter til å vise dette programmet utenfor Norge'
    assert ie.geo_restricted_countries == ['NO']
    assert 'NRK har ikke rettigheter' in str(excinfo.value)


def test_extract_formats_akamai(monkeypatch):
    """_extract_nrk_formats should delegate to _extract_akamai_formats for Akamai URLs."""
    ie = DummyNRKIE()
    asset_url = 'https://example.akamaihd.net/i/test.m3u8'
    formats = ie._extract_nrk_formats(asset_url, 'vid123')
    assert formats == [{'format_id': 'akamai', 'url': asset_url}]


def test_extract_formats_cdn_replacement(monkeypatch):
    """When no formats are found and the URL matches the CDN regex,
    a replacement URL is generated and formats are extracted."""
    ie = DummyNRKIE()
    # URL that matches the CDN regex but is not an Akamai URL
    asset_url = 'https://nrkod1-httpcache0-47115-cacheod0.dna.ip-only.net/47115-cacheod0/some/path.m3u8'
    # Patch random.randint to return a fixed value for deterministic test
    monkeypatch.setattr(random, 'randint', lambda a, b: 42)
    # Patch _extract_m3u8_formats to return a predictable format list
    def fake_extract_m3u8(asset_url, video_id, ext, parser, fatal):
        return [{'format_id': 'cdn', 'url': asset_url}]
    monkeypatch.setattr(ie, '_extract_m3u8_formats', fake_extract_m3u8)
    formats = ie._extract_nrk_formats(asset_url, 'vid123')
    # The replacement URL should contain the generated host
    assert any('nrk-od-42.akamaized.net' in f['url'] for f in formats)
    assert formats[0]['format_id'] == 'cdn'
