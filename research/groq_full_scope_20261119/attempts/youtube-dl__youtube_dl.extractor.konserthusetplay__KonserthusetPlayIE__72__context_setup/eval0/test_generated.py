import pytest
from youtube_dl.extractor.konserthusetplay import KonserthusetPlayIE
from youtube_dl.utils import determine_ext, int_or_none, float_or_none, url_or_none


class DummyKonserthusetPlayIE(KoncerthusetPlayIE):
    """A subclass that overrides network calls to return deterministic data."""

    def __init__(self, webpage, json_response):
        super().__init__(downloader=None)
        self._webpage = webpage
        self._json_response = json_response

    def _download_webpage(self, url, video_id, note=None, errnote=None, *, data=None, headers=None, query=None, timeout=None, fatal=True):
        return self._webpage

    def _download_json(self, url, video_id, note=None, headers=None, data=None, query=None, timeout=None, transform_source=None, errnote=None, fatal=True):
        if transform_source:
            return transform_source(self._json_response)
        return self._json_response


def test_normal_extraction(tmp_path):
    # Prepare a minimal webpage containing the required 'e' parameter
    webpage = (
        '<html>'
        '<script src="https://csp.picsearch.com/rest?e=EXAMPLE_E&containerId=mediaplayer&i=object"></script>'
        '</html>'
    )
    # JSON response mimicking the structure used in _real_extract
    json_response = (
        '{"media": {"title": "Test Title", "image": "http://example.com/thumb.jpg", '
        '"duration": 123456, "playerconfig": {"title": "Config Title", "playlist": '
        '[{"url": "http://example.com/video.m3u8", "bitrates": [], "provider": "hls"}], '
        '"rtmp": {"netConnectionUrl": "rtmp://example.com/stream"}, '
        '"plugins": {"bwcheck": {"netConnectionUrl": "rtmp://example.com/bwcheck"}}}, '
        '"captionsAvailableLanguages": {"en": "http://example.com/subs_en.vtt"}}}'
    )
    # Instantiate the dummy extractor
    extractor = DummyKonserthusetPlayIE(webpage, json_response)
    result = extractor._real_extract('http://www.konserthusetplay.se/?m=TESTID')
    # Assertions on extracted fields
    assert result['id'] == 'TESTID'
    assert result['title'] == 'Config Title'
    assert result['description'] is None
    assert result['thumbnail'] == 'http://example.com/thumb.jpg'
    assert result['duration'] == 123.456
    # Check that formats include the m3u8 format
    m3u8_formats = [f for f in result['formats'] if f.get('url') == 'http://example.com/video.m3u8']
    assert m3u8_formats, "Expected m3u8 format to be present"
    # Check subtitles
    assert 'en' in result['subtitles']
    assert result['subtitles']['en'][0]['url'] == 'http://example.com/subs_en.vtt'


def test_only_matching_url():
    # The second test URL should only match the regex and not be extracted
    extractor = KonserthusetPlayIE()
    # _real_extract should raise a ValueError because the URL does not contain the 'e' parameter
    with pytest.raises(ValueError):
        extractor._real_extract('http://rspoplay.se/?m=elWuEH34SMKvaO4wO_cHBw')


def test_missing_e_parameter(tmp_path):
    # Webpage without the 'e' parameter should cause a regex failure
    webpage = '<html><body>No e param here</body></html>'
    json_response = '{}'
    extractor = DummyKonserthusetPlayIE(webpage, json_response)
    with pytest.raises(ValueError):
        extractor._real_extract('http://www.konserthusetplay.se/?m=NOE')
