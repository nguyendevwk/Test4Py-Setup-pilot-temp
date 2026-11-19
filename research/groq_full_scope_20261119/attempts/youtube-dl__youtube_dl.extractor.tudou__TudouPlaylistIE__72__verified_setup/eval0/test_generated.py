import re
import pytest
from youtube_dl.extractor.tudou import TudouPlaylistIE
from youtube_dl.utils import DownloadError

# Test 1: URL validation and ID extraction
def test_valid_url_and_id_extraction():
    url = "http://www.tudou.com/listplay/zzdE77v6Mmo.html"
    # Ensure the regex matches the URL
    assert re.match(TudouPlaylistIE._VALID_URL, url)
    # Instantiate the extractor and extract the ID
    ie = TudouPlaylistIE()
    extracted_id = ie._match_id(url)
    assert extracted_id == "zzdE77v6Mmo"

# Test 2: Invalid URL should raise a regex error
def test_invalid_url_raises():
    url = "http://www.tudou.com/invalid/zzdE77v6Mmo.html"
    ie = TudouPlaylistIE()
    with pytest.raises(DownloadError):
        ie._match_id(url)

# Test 3: Real extraction attempts to download JSON and should fail without network
def test_real_extract_raises_download_error(tmp_path):
    url = "http://www.tudou.com/listplay/zzdE77v6Mmo.html"
    ie = TudouPlaylistIE()
    # The extractor will try to download JSON; without network this should raise DownloadError
    with pytest.raises(DownloadError):
        ie._real_extract(url)
