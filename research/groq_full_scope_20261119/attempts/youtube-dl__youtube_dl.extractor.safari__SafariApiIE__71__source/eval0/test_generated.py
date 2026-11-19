import json
import re
import pytest
from youtube_dl.extractor.safari import SafariApiIE

# Helper to create a dummy extractor instance with a patched _download_json
def make_extractor(json_response):
    extractor = SafariApiIE()
    def fake_download_json(url, name, note):
        # The real method would fetch from the network; we return the provided JSON.
        return json_response
    extractor._download_json = fake_download_json
    return extractor

def test_safari_api_ie_normal_extraction():
    # Given a valid URL and a JSON containing a web_url field
    url = "https://www.safaribooksonline.com/api/v1/book/123456789/chapter/part01.html"
    json_response = {"web_url": "https://example.com/content/part01"}
    extractor = make_extractor(json_response)

    result = extractor._real_extract(url)

    # The result should be a URL result pointing to the web_url
    assert result._url == json_response["web_url"]
    assert result._ie_key == "safari"

def test_safari_api_ie_missing_web_url_raises():
    # When the JSON lacks the required 'web_url' key, an ExtractorError should be raised
    url = "https://www.safaribooksonline.com/api/v1/book/987654321/chapter/part02.html"
    json_response = {"not_web_url": "https://example.com/invalid"}
    extractor = make_extractor(json_response)

    with pytest.raises(Exception) as excinfo:
        extractor._real_extract(url)
    assert "web_url" in str(excinfo.value)

def test_safari_api_ie_invalid_url_pattern():
    # URLs that do not match the pattern should result in a regex match failure
    url = "https://www.safaribooksonline.com/api/v1/book/123/chapter/part01/extra.html"
    extractor = SafariApiIE()
    # _real_extract will call re.match; we expect it to return None and raise
    with pytest.raises(Exception) as excinfo:
        extractor._real_extract(url)
    assert "Downloading part JSON" not in str(excinfo.value)
