import re
import pytest
from youtube_dl.extractor.tudou import TudouPlaylistIE
from youtube_dl.utils import ExtractorError

# Test that the regular expression matches a valid Tudou playlist URL
def test_valid_url_regex():
    url = "http://www.tudou.com/listplay/zzdE77v6Mmo.html"
    assert re.match(TudouPlaylistIE._VALID_URL, url), "URL should match the regex"

# Test that the extractor correctly extracts the playlist id from a valid URL
def test_match_id_extraction():
    url = "https://www.tudou.com/listplay/zzdE77v6Mmo.html"
    extractor = TudouPlaylistIE()
    playlist_id = extractor._match_id(url)
    assert playlist_id == "zzdE77v6Mmo", "Extracted id should match the expected value"

# Test that providing an invalid URL raises an ExtractorError
def test_invalid_url_raises():
    url = "https://www.tudou.com/not_a_playlist.html"
    extractor = TudouPlaylistIE()
    with pytest.raises(ExtractorError):
        extractor._match_id(url)
