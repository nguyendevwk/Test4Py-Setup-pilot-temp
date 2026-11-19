import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeasonIE, NRKTVSerieBaseIE


def test_valid_url_parsing():
    """Verify that NRKTVSeasonIE correctly extracts components from a valid URL."""
    url = "https://tv.nrk.no/serie/backstage/sesong/1"
    match = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert match is not None, "URL should match the VALID_URL pattern"
    assert match.group('domain') == 'tv'
    assert match.group('serie_kind') == 'serie'
    assert match.group('serie') == 'backstage'
    # id should be captured from the first alternative
    assert match.group('id') == '1'
    assert match.group('id_2') is None
    # display_id should combine serie and season id
    display_id = f"{match.group('serie')}/{match.group('id') or match.group('id_2')}"
    assert display_id == "backstage/1"


def test_suitable_exclusion_of_other_extractors():
    """Ensure NRKTVSeasonIE is not suitable for URLs that match other NRK extractors."""
    # URL that matches NRKTVIE (not shown here but assumed to exist)
    tv_url = "https://tv.nrk.no/serie/backstage"
    # URL that matches NRKTVEpisodeIE
    episode_url = "https://tv.nrk.no/serie/backstage/sesong/1/episode/2"
    # URL that matches NRKRadioPodkastIE
    podkast_url = "https://radio.nrk.no/podkast/hele_historien/l_96f4f1b0-de54-4e6a-b4f1-b0de54fe6af8"

    # NRKTVSeasonIE should not consider these URLs suitable
    assert not NRKTVSeasonIE.suitable(tv_url)
    assert not NRKTVSeasonIE.suitable(episode_url)
    assert not NRKTVSeasonIE.suitable(podkast_url)

    # A URL that matches the season pattern should be suitable
    season_url = "https://radio.nrk.no/serie/dagsnytt/sesong/201509"
    assert NRKTVSeasonIE.suitable(season_url)


def test_catalog_name_mapping():
    """Test that the catalog name is correctly derived from the serie_kind."""
    assert NRKTVSerieBaseIE._catalog_name('serie') == 'series'
    assert NRKTVSerieBaseIE._catalog_name('podcast') == 'podcast'
    assert NRKTVSerieBaseIE._catalog_name('podkast') == 'podcast'
    # Unknown kind should default to 'series'
    assert NRKTVSerieBaseIE._catalog_name('unknown') == 'series'
