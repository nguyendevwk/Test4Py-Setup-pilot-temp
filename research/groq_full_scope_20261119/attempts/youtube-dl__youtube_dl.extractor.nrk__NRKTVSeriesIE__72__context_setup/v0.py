import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeriesIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE


def test_valid_url_match():
    """NRKTVSeriesIE._VALID_URL should match expected NRK series URLs."""
    pattern = re.compile(NRKTVSeriesIE._VALID_URL)
    # Known valid URLs from the extractor tests
    valid_urls = [
        "https://tv.nrk.no/serie/groenn-glede",
        "https://radio.nrk.no/serie/dickie-dick-dickens",
        "https://nrksuper.no/serie/labyrint",
        "https://tv.nrk.no/serie/backstage",
    ]
    for url in valid_urls:
        assert pattern.match(url), f"URL {url!r} should match the pattern"

    # URLs that should not match (different domain or path)
    invalid_urls = [
        "https://tv.nrk.no/episode/123",
        "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8",
        "https://example.com/serie/groenn-glede",
    ]
    for url in invalid_urls:
        assert not pattern.match(url), f"URL {url!r} should not match the pattern"


def test_suitable_excludes_other_extractors():
    """NRKTVSeriesIE.suitable must return False when a more specific extractor matches."""
    # URL that matches NRKTVIE
    url_tv = "https://tv.nrk.no/serie/hellums-kro"
    assert NRKTVIE.suitable(url_tv)
    assert not NRKTVSeriesIE.suitable(url_tv)

    # URL that matches NRKTVEpisodeIE
    url_episode = "https://tv.nrk.no/serie/hellums-kro/sesong/1/episode/2"
    assert NRKTVEpisodeIE.suitable(url_episode)
    assert not NRKTVSeriesIE.suitable(url_episode)

    # URL that matches NRKRadioPodkastIE
    url_podkast = "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"
    assert NRKRadioPodkastIE.suitable(url_podkast)
    assert not NRKTVSeriesIE.suitable(url_podkast)

    # URL that matches NRKTVSeasonIE
    url_season = "https://tv.nrk.no/serie/backstage/sesong/1"
    assert NRKTVSeasonIE.suitable(url_season)
    assert not NRKTVSeriesIE.suitable(url_season)

    # URL that should be suitable for NRKTVSeriesIE
    url_series = "https://tv.nrk.no/serie/groenn-glede"
    assert NRKTVSeriesIE.suitable(url_series)
    # Ensure no other extractor claims it
    assert not any(
        ie.suitable(url_series)
        for ie in (NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE)
    )


def test_invalid_url_returns_none():
    """NRKTVSeriesIE.suitable should return False for URLs that do not match the pattern."""
    bad_urls = [
        "https://tv.nrk.no/episode/123",
        "https://radio.nrk.no/podkast/ulrikkes_univers/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8",
        "https://example.com/serie/groenn-glede",
        "https://tv.nrk.no/serie/",
        "http://tv.nrk.no/serie",
    ]
    for url in bad_urls:
        assert not NRKTVSeriesIE.suitable(url), f"URL {url!r} should not be suitable for NRKTVSeriesIE"
