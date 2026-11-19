import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeriesIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE


def test_valid_url_parsing():
    """The _VALID_URL regex should correctly capture domain, serie_kind and id."""
    url = "https://tv.nrk.no/serie/groenn-glede"
    match = re.match(NRKTVSeriesIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    domain, serie_kind, serie_id = match.groups()
    assert domain == "tv.nrk"
    assert serie_kind == "serie"
    assert serie_id == "groenn-glede"


def test_suitable_precedence():
    """NRKTVSeriesIE.suitable should return False when any of the other IE classes are suitable."""
    # A URL that is suitable for NRKTVIE (e.g. a single episode)
    episode_url = "https://tv.nrk.no/episode/12345"
    # Ensure that NRKTVIE considers it suitable
    assert NRKTVIE.suitable(episode_url) is True
    # NRKTVSeriesIE should then return False for the same URL
    assert NRKTVSeriesIE.suitable(episode_url) is False

    # A URL that is suitable for NRKRadioPodkastIE
    podkast_url = "https://radio.nrk.no/podkast/ulrikkes_univers"
    assert NRKRadioPodkastIE.suitable(podkast_url) is True
    assert NRKTVSeriesIE.suitable(podkast_url) is False

    # A URL that is suitable for NRKTVSeasonIE
    season_url = "https://tv.nrk.no/serie/groenn-glede/sesong/1"
    assert NRKTVSeasonIE.suitable(season_url) is True
    assert NRKTVSeriesIE.suitable(season_url) is False


def test_suitable_series_url():
    """NRKTVSeriesIE.suitable should return True for a series URL that is not matched by other IE classes."""
    series_url = "https://tv.nrk.no/serie/groenn-glede"
    # Ensure no other IE class claims this URL
    assert NRKTVIE.suitable(series_url) is False
    assert NRKTVEpisodeIE.suitable(series_url) is False
    assert NRKRadioPodkastIE.suitable(series_url) is False
    assert NRKTVSeasonIE.suitable(series_url) is False
    # NRKTVSeriesIE should claim it
    assert NRKTVSeriesIE.suitable(series_url) is True
