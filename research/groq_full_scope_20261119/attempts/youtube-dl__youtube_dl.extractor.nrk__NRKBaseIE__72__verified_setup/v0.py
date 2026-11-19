import re
import random
import pytest
from youtube_dl.extractor.nrk import NRKBaseIE
from youtube_dl.utils import ExtractorError


class DummyNRKIE(NRKBaseIE):
    """A minimal subclass that overrides network‑dependent methods."""

    def _download_json(self, url, video_id, note, fatal=True, query=None, headers=None):
        # Return a fixed JSON structure for testing _raise_error
        return {"messageType": "ProgramRightsAreNotReady", "endUserMessage": "Test message"}

    def _extract_akamai_formats(self, asset_url, video_id):
        # Return a deterministic format list for akamai URLs
        return [{"format_id": "akamai", "url": asset_url}]

    def _extract_m3u8_formats(self, asset_url, video_id, ext, parser, fatal=False):
        # Return a deterministic format list for non‑akamai URLs
        return [{"format_id": "m3u8", "url": asset_url}]

    def raise_geo_restricted(self, msg=None, countries=None):
        # Record that geo restriction was raised
        self.geo_restricted = (msg, countries)


def test_raise_error_message():
    """_raise_error should raise ExtractorError with the correct message."""
    ie = DummyNRKIE()
    data = {"messageType": "ProgramRightsHasExpired"}
    with pytest.raises(ExtractorError) as excinfo:
        ie._raise_error(data)
    assert "ProgramRightsHasExpired" in str(excinfo.value)
    assert "Programmet har gått ut" in str(excinfo.value)


def test_raise_error_geo_blocked():
    """_raise_error should raise geo restriction when appropriate."""
    ie = DummyNRKIE()
    data = {"messageType": "ProgramIsGeoBlocked"}
    with pytest.raises(ExtractorError) as excinfo:
        ie._raise_error(data)
    assert "NRK har ikke rettigheter" in str(excinfo.value)
    # The overridden raise_geo_restricted should have been called
    assert ie.geo_restricted == ("NRK har ikke rettigheter til å vise dette programmet utenfor Norge", ["NO"])


def test_extract_nrk_formats_akamai():
    """_extract_nrk_formats should delegate to _extract_akamai_formats for akamai URLs."""
    ie = DummyNRKIE()
    asset_url = "https://example.akamaihd.net/i/test.m3u8"
    video_id = "12345"
    formats = ie._extract_nrk_formats(asset_url, video_id)
    assert isinstance(formats, list)
    assert formats[0]["format_id"] == "akamai"
    assert formats[0]["url"] == asset_url
