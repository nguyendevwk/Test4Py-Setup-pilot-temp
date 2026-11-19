import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeriesIE, NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE

# Test 1: Validate that the regex captures the expected groups
def test_valid_url_regex_groups():
    url = "https://tv.nrk.no/serie/groenn-glede"
    match = re.match(NRKTVSeriesIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    domain, serie_kind, series_id = match.groups()
    assert domain == "tv.nrk"
    assert serie_kind == "serie"
    assert series_id == "groenn-glede"

# Test 2: Ensure NRKTVSeriesIE.suitable returns False when any of the other IE classes are suitable
def test_suitable_returns_false_when_other_ie_suitable():
    url = "https://tv.nrk.no/serie/groenn-glede"
    # At least one of the other IE classes should be suitable for this URL
    other_ies = [NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE]
    any_other_suitable = any(ie.suitable(url) for ie in other_ies)
    assert any_other_suitable, "At least one other IE should be suitable for the test URL"
    # NRKTVSeriesIE should then return False
    assert not NRKTVSeriesIE.suitable(url), "NRKTVSeriesIE.suitable should be False when another IE is suitable"

# Test 3: Verify that NRKTVSeriesIE.suitable returns True when no other IE is suitable
def test_suitable_returns_true_when_no_other_ie_suitable():
    # Construct a URL that matches the regex but is unlikely to be suitable for the other IE classes
    # Using a random series id that probably doesn't exist
    url = "https://tv.nrk.no/serie/this_series_does_not_exist_12345"
    other_ies = [NRKTVIE, NRKTVEpisodeIE, NRKRadioPodkastIE, NRKTVSeasonIE]
    any_other_suitable = any(ie.suitable(url) for ie in other_ies)
    # It's possible that some IE might still claim suitability; if so, skip the test
    if any_other_suitable:
        pytest.skip("Another IE claims suitability for the constructed URL; cannot test NRKTVSeriesIE.suitable=True")
    assert NRKTVSeriesIE.suitable(url), "NRKTVSeriesIE.suitable should be True when no other IE is suitable"
