import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeriesIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE


def test_valid_url_parsing():
    """NRKTVSeriesIE should correctly parse valid URLs into components."""
    url = "https://tv.nrk.no/serie/groenn-glede"
    match = re.match(NRKTVSeriesIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    domain, serie_kind, series_id = match.groups()
    assert domain in ("tv.nrk", "radio.nrk", "tv.nrksuper", "nrksuper")
    assert serie_kind in ("serie", "podcast", "podkast")
    assert series_id == "groenn-glede"


def test_suitable_precedence(monkeypatch):
    """NRKTVSeriesIE.suitable should return False if any higher‑priority IE is suitable."""
    url = "https://tv.nrk.no/serie/groenn-glede"

    # Ensure other IE classes report suitable
    monkeypatch.setattr(NRKTVIE, "suitable", lambda cls, u: u == url)
    monkeypatch.setattr(NRKTVEpisodeIE, "suitable", lambda cls, u: False)
    monkeypatch.setattr(NRKRadioPodkastIE, "suitable", lambda cls, u: False)
    monkeypatch.setattr(NRKTVSeasonIE, "suitable", lambda cls, u: False)

    assert NRKTVSeriesIE.suitable(url) is False, "Should defer to higher‑priority IE"

    # When no other IE is suitable, NRKTVSeriesIE should be suitable
    monkeypatch.setattr(NRKTVIE, "suitable", lambda cls, u: False)
    assert NRKTVSeriesIE.suitable(url) is True, "Should be suitable when no other IE matches"


def test_invalid_url_rejection():
    """NRKTVSeriesIE.suitable should reject URLs that do not match the pattern."""
    invalid_urls = [
        "https://example.com/serie/groenn-glede",
        "https://tv.nrk.no/episode/123",
        "http://tv.nrk.no/serie/",
        "https://tv.nrk.no/serie/groenn-glede/extra",
    ]
    for url in invalid_urls:
        assert NRKTVSeriesIE.suitable(url) is False, f"URL {url} should not be suitable"
