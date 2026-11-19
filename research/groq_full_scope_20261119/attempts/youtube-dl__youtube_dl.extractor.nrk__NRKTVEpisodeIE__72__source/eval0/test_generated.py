import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodeIE

# Test 1: Validate that the _VALID_URL regex correctly captures the display_id,
# season_number and episode_number from a known URL.
def test_valid_url_regex_groups():
    url = 'https://tv.nrk.no/serie/hellums-kro/sesong/1/episode/2'
    match = re.match(NRKTVEpisodeIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    display_id, season_number, episode_number = match.groups()
    assert display_id == 'hellums-kro/sesong/1/episode/2'
    assert season_number == '1'
    assert episode_number == '2'

# Test 2: Ensure that passing an invalid URL to the regex raises an AttributeError
# because .groups() is called on None.
def test_invalid_url_raises():
    invalid_url = 'https://example.com/not-nrk'
    with pytest.raises(AttributeError):
        re.match(NRKTVEpisodeIE._VALID_URL, invalid_url).groups()

# Test 3: Verify that each test case in NRKTVEpisodeIE._TESTS contains the required
# keys and that the 'info_dict' includes the expected mandatory fields.
def test_test_cases_structure():
    required_keys = {'url', 'info_dict', 'params'}
    mandatory_info_fields = {
        'id', 'ext', 'title', 'description', 'duration',
        'series', 'season_number', 'episode_number', 'episode', 'age_limit'
    }
    for test in NRKTVEpisodeIE._TESTS:
        assert required_keys.issubset(test.keys()), f"Missing keys in test: {test}"
        info = test['info_dict']
        assert mandatory_info_fields.issubset(info.keys()), f"Missing info fields in test: {info}"
