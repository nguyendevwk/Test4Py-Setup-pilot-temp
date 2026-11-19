import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeasonIE

# Test that the _VALID_URL regex correctly captures the expected groups
def test_valid_url_groups():
    url = "https://tv.nrk.no/serie/backstage/sesong/1"
    m = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert m is not None
    assert m.group("domain") == "tv"
    assert m.group("serie_kind") == "serie"
    assert m.group("serie") == "backstage"
    assert m.group("id") == "1"
    assert m.group("id_2") is None

    url2 = "https://radio.nrk.no/serie/dickie-dick-dickens/sesong/1"
    m2 = re.match(NRKTVSeasonIE._VALID_URL, url2)
    assert m2 is not None
    assert m2.group("domain") == "radio"
    assert m2.group("serie_kind") == "serie"
    assert m2.group("serie") == "dickie-dick-dickens"
    assert m2.group("id") == "1"
    assert m2.group("id_2") is None

    url3 = "https://radio.nrk.no/podkast/hele_historien/sesong/diagnose-kverulant"
    m3 = re.match(NRKTVSeasonIE._VALID_URL, url3)
    assert m3 is not None
    assert m3.group("domain") == "radio"
    assert m3.group("serie_kind") == "podkast"
    assert m3.group("serie") == "hele_historien"
    assert m3.group("id") is None
    assert m3.group("id_2") == "diagnose-kverulant"

# Test that URLs not matching the pattern return None
def test_invalid_url():
    url = "https://example.com/not-nrk/serie/abc"
    m = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert m is None

# Test that the display_id is constructed correctly from the matched groups
def test_display_id_construction():
    url = "https://tv.nrk.no/serie/lindmo/2016"
    m = re.match(NRKTVSeasonIE._VALID_URL, url)
    assert m is not None
    domain = m.group("domain")
    serie_kind = m.group("serie_kind")
    serie = m.group("serie")
    season_id = m.group("id") or m.group("id_2")
    display_id = f"{serie}/{season_id}"
    assert display_id == "lindmo/2016"
