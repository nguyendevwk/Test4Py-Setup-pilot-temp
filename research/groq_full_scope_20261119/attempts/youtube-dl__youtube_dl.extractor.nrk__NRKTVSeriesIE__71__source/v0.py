import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeriesIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE


def test_valid_url_parsing():
    """_VALID_URL should correctly capture domain, serie_kind and id."""
    url = "https://tv.nrk.no/serie/groenn-glede"
    match = re.match(NRKTVSeriesIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    domain, serie_kind, series_id = match.groups()
    assert domain in ("tv.nrk.no", "radio.nrk.no", "tv.nrksuper.no", "nrksuper.no")
    assert serie_kind in ("serie", "podcast", "podkast")
    assert series_id == "groenn-glede"


def test_suitable_true_for_series_url():
    """suitable should return True for a series URL that is not matched by other IE."""
    url = "https://tv.nrk.no/serie/groenn-glede"
    # Ensure that none of the other IE classes consider this URL suitable
    assert not NRKTVIE.suitable(url), "NRKTVIE should not match series URL"
    assert not NRKTVEpisodeIE.suitable(url), "NRKTVEpisodeIE should not match series URL"
    assert not NRKRadioPodkastIE.suitable(url), "NRKRadioPodkastIE should not match series URL"
    assert not NRKTVSeasonIE.suitable(url), "NRKTVSeasonIE should not match series URL"
    # Now check that NRKTVSeriesIE considers it suitable
    assert NRKTVSeriesIE.suitable(url), "NRKTVSeriesIE should match series URL"


def test_suitable_false_for_non_series_url():
    """suitable should return False for URLs that do not match the series pattern."""
    url = "https://tv.nrk.no/episode/12345"
    assert not NRKTVSeriesIE.suitable(url), "Non-series URL should not be suitable for NRKTVSeriesIE"
