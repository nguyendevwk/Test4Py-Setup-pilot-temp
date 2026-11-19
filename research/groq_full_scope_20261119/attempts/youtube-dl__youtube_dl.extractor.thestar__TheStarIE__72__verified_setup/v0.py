import re
import pytest
from youtube_dl.extractor.thestar import TheStarIE
from youtube_dl.utils import ExtractorError

# Test 1: Validate the URL regex matches expected patterns and captures the id correctly
def test_valid_url_regex():
    url = "http://www.thestar.com/life/2016/02/01/mankind-why-this-woman-started-a-men-s-skincare-line.html"
    match = re.match(TheStarIE._VALID_URL, url)
    assert match is not None, "URL should match the regex"
    assert match.group('id') == "mankind-why-this-woman-started-a-men-s-skincare-line", "Captured id should match the path segment before .html"

# Test 2: Ensure the test metadata dictionary contains all required keys and values
def test_test_dict_structure():
    test_dict = TheStarIE._TEST
    required_keys = {'url', 'md5', 'info_dict', 'params'}
    assert required_keys.issubset(test_dict.keys()), "Test dict missing required keys"
    assert test_dict['url'].startswith('http://'), "Test URL should start with http://"
    assert isinstance(test_dict['md5'], str) and len(test_dict['md5']) == 32, "MD5 should be a 32-character hex string"
    info = test_dict['info_dict']
    for key in ['id', 'ext', 'title', 'description', 'uploader_id', 'timestamp', 'upload_date']:
        assert key in info, f"info_dict missing key: {key}"
    assert test_dict['params'].get('skip_download') is True, "params should request skip_download"

# Test 3: Subclass TheStarIE to override network calls and test extraction logic
class DummyTheStarIE(TheStarIE):
    def __init__(self, webpage):
        super().__init__()
        self._dummy_webpage = webpage

    def _download_webpage(self, url, display_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, speed_limit=None, max_retries=None, fatal=True):
        # Return the pre-set dummy webpage instead of performing a real download
        return self._dummy_webpage

def test_real_extract_success_and_failure():
    # Successful extraction: brightcove id present
    webpage_success = '''
        <script>
            var mainartBrightcoveVideoId = "1234567890";
        </script>
    '''
    extractor_success = DummyTheStarIE(webpage_success)
    result = extractor_success._real_extract("http://www.thestar.com/some/path.html")
    expected_url = extractor_success.BRIGHTCOVE_URL_TEMPLATE % "1234567890"
    assert result.url == expected_url, "Result URL should contain the brightcove id"
    assert result.info_dict['ext'] == 'mp4', "Default extension should be mp4"
    assert result.info_dict['id'] == "1234567890", "Info dict id should match brightcove id"

    # Failure extraction: brightcove id missing
    webpage_fail = '''
        <script>
            var someOtherVariable = "no id here";
        </script>
    '''
    extractor_fail = DummyTheStarIE(webpage_fail)
    with pytest.raises(ExtractorError):
        extractor_fail._real_extract("http://www.thestar.com/some/other/path.html")
