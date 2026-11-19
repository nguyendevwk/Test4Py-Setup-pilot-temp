import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeasonIE, NRKTVSerieBaseIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE


def test_nrk_tv_season_eligible_urls():
    """NRKTVSeasonIE should be suitable for season URLs but not for episode or podkast URLs."""
    season_url = "https://tv.nrk.no/serie/backstage/sesong/1"
    episode_url = "https://tv.nrk.no/serie/backstage/sesong/1/episode/2"
    podkast_url = "https://radio.nrk.no/podkast/hele_historien/sesong/diagnose-kverulant"

    assert NRKTVSeasonIE.suitable(season_url) is True
    assert NRKTVEpisodeIE.suitable(episode_url) is True
    assert NRKRadioPodkastIE.suitable(podkast_url) is True
    # NRKTVSeasonIE should not claim suitability for episode or podkast URLs
    assert NRKTVSeasonIE.suitable(episode_url) is False
    assert NRKTVSeasonIE.suitable(podkast_url) is False


def test_nrk_tv_season_valid_url_parsing():
    """The _VALID_URL regex should correctly capture components of a season URL."""
    url = "https://radio.nrk.no/serie/dickie-dick-dickens/sesong/1"
    match = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert match is not None
    assert match.group('domain') == "radio"
    assert match.group('serie_kind') == "serie"
    assert match.group('serie') == "dickie-dick-dickens"
    # id group should capture the numeric season id
    assert match.group('id') == "1"
    # id_2 should be None for numeric id
    assert match.group('id_2') is None
    # Construct display_id as expected
    display_id = f"{match.group('serie')}/{match.group('id') or match.group('id_2')}"
    assert display_id == "dickie-dick-dickens/1"


def test_nrk_tv_season_catalog_name():
    """_catalog_name should return 'series' for serie kinds and 'podcast' for podkast kinds."""
    assert NRKTVSerieBaseIE._catalog_name("serie") == "series"
    assert NRKTVSerieBaseIE._catalog_name("podcast") == "podcast"
    assert NRKTVSerieBaseIE._catalog_name("podkast") == "podcast"
    # Unknown kind should default to 'series'
    assert NRKTVSerieBaseIE._catalog_name("unknown") == "series"
