import pytest
from youtube_dl.extractor.safari import SafariIE
from youtube_dl.utils import ExtractorError

@pytest.fixture
def extractor():
    return SafariIE()

def test_safari_valid_extraction(extractor, monkeypatch):
    # Patch network calls to avoid real HTTP requests
    monkeypatch.setattr(extractor, "_download_webpage_handle", lambda url, video_id: ("<html></html>", type('Mock', (), {'geturl': lambda self: url})()))
    monkeypatch.setattr(extractor, "_search_regex", lambda *args, **kwargs: "dummy")
    monkeypatch.setattr(extractor, "_download_json", lambda *args, **kwargs: None)
    result = extractor.extract_info(
        "https://www.safaribooksonline.com/library/view/hadoop-fundamentals-livelessons/9780133392838/part00.html",
        download=False)
    assert result['id'] == '0_qbqx90ic'
    assert result['ext'] == 'mp4'
    assert result['title'] == 'Introduction to Hadoop Fundamentals LiveLessons'
    assert result['timestamp'] == 1437758058
    assert result['upload_date'] == '20150724'
    assert result['uploader_id'] == 'stork'
    assert result['_type'] == 'url_transparent'
    assert result['ie_key'] == 'Kaltura'
    assert result['url'].startswith('https://cdnapisec.kaltura.com/html5/html5lib/v2.37.1/mwEmbedFrame.php')

def test_safari_non_digit_course_id_only_matching(extractor):
    url = "https://www.safaribooksonline.com/library/view/create-a-nodejs/100000006A0210/part00.html"
    assert extractor.suitable(url) is True
    with pytest.raises(ExtractorError):
        extractor.extract_info(url, download=False)

def test_safari_invalid_url_raises(extractor):
    url = "https://example.com/not-a-safari-url"
    assert extractor.suitable(url) is False
    with pytest.raises(ExtractorError):
        extractor.extract_info(url, download=False)
