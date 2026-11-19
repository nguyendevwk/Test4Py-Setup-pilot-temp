import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeasonIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE

# Test that the regular expression correctly captures the expected groups
def test_valid_url_groups():
    url = 'https://tv.nrk.no/serie/backstage/sesong/1'
    m = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert m is not None
    assert m.group('domain') == 'tv'
    assert m.group('serie_kind') == 'serie'
    assert m.group('serie') == 'backstage'
    assert m.group('id') == '1'
    assert m.group('id_2') is None

    url2 = 'https://radio.nrk.no/serie/dickie-dick-dickens/sesong/1'
    m2 = re.match(NRKTVSeasonIE._VALID_URL, url2)
    assert m2 is not None
    assert m2.group('domain') == 'radio'
    assert m2.group('serie_kind') == 'serie'
    assert m2.group('serie') == 'dickie-dick-dickens'
    assert m2.group('id') == '1'
    assert m2.group('id_2') is None

    url3 = 'https://radio.nrk.no/podkast/hele_historien/sesong/diagnose-kverulant'
    m3 = re.match(NRKTVSeasonIE._VALID_URL, url3)
    assert m3 is not None
    assert m3.group('domain') == 'radio'
    assert m3.group('serie_kind') == 'podkast'
    assert m3.group('serie') == 'hele_historien'
    assert m3.group('id') is None
    assert m3.group('id_2') == 'diagnose-kverulant'

# Test that suitable returns True for season URLs and False for other NRK URLs
def test_suitable_true():
    season_urls = [
        'https://tv.nrk.no/serie/backstage/sesong/1',
        'https://radio.nrk.no/serie/dickie-dick-dickens/sesong/1',
        'https://radio.nrk.no/podkast/hele_historien/sesong/diagnose-kverulant',
    ]
    for url in season_urls:
        assert NRKTVSeasonIE.suitable(url) is True

# Test that suitable returns False for URLs that match other extractors
def test_suitable_false():
    # URLs that match NRKTVIE (series page)
    assert NRKTVSeasonIE.suitable('https://tv.nrk.no/serie/backstage') is False
    # URLs that match NRKTVEpisodeIE (episode page)
    assert NRKTVSeasonIE.suitable('https://tv.nrk.no/serie/backstage/episode/1') is False
    # URLs that match NRKRadioPodkastIE (podcast page)
    assert NRKTVSeasonIE.suitable('https://radio.nrk.no/podkast/hele_historien') is False
