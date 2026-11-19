import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeriesIE

# Test that the regular expression correctly captures the components of a valid URL
def test_valid_url_match():
    url = "https://tv.nrk.no/serie/groenn-glede"
    match = re.match(NRKTVSeriesIE._VALID_URL, url)
    assert match is not None, "URL should match the _VALID_URL pattern"
    domain, serie_kind, series_id = match.groups()
    assert domain in ("tv.nrk", "radio.nrk", "tv.nrksuper", "nrksuper")
    assert serie_kind in ("serie", "podcast", "podkast")
    assert series_id == "groenn-glede"

# Test that the `suitable` classmethod correctly excludes URLs that match other extractors
def test_suitable_exclusion(monkeypatch):
    # Mock the other extractors' suitable methods to return True for this URL
    class DummyIE:
        @classmethod
        def suitable(cls, url):
            return True
    monkeypatch.setattr("youtube_dl.extractor.nrk.NRKTVIE", DummyIE)
    monkeypatch.setattr("youtube_dl.extractor.nrk.NRKTVEpisodeIE", DummyIE)
    monkeypatch.setattr("youtube_dl.extractor.nrk.NRKRadioPodkastIE", DummyIE)
    monkeypatch.setattr("youtube_dl.extractor.nrk.NRKTVSeasonIE", DummyIE)

    url = "https://tv.nrk.no/serie/groenn-glede"
    assert NRKTVSeriesIE.suitable(url) is False, "URL should not be suitable when other extractors match"

# Test that an obviously invalid URL is not considered suitable
def test_invalid_url_not_suitable():
    url = "https://example.com/not-a-nrk-url"
    assert NRKTVSeriesIE.suitable(url) is False, "Non-NRK URL should not be suitable"
