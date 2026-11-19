import pytest
from youtube_dl.extractor.hitrecord import HitRecordIE
from youtube_dl.utils import clean_html

class DummyHitRecordIE(HitRecordIE):
    """A test subclass that overrides _download_json to return a controlled payload."""
    def __init__(self, payload):
        super().__init__()
        self._payload = payload

    def _download_json(self, url, video_id, note=None, errnote=None, data=None, headers=None, query=None, timeout=None, err=None, **kw):
        # Ignore all parameters and return the predefined payload
        return self._payload


def test_normal_extraction():
    """Test normal extraction with all fields present."""
    payload = {
        'title': 'Test Video',
        'source_url': {'mp4_url': 'https://example.com/video.mp4'},
        'body': '<p>Some <b>HTML</b> description.</p>',
        'duration': 123456,  # milliseconds
        'created_at_i': 1609459200,
        'user': {'username': 'tester', 'id': 42},
        'total_views_count': 1000,
        'hearts_count': 200,
        'comments_count': 30,
        'tags': [{'text': 'tag1'}, {'text': 'tag2'}],
    }
    ie = DummyHitRecordIE(payload)
    result = ie._real_extract('https://hitrecord.org/records/12345')
    assert result['id'] == '12345'
    assert result['url'] == 'https://example.com/video.mp4'
    assert result['title'] == 'Test Video'
    assert result['description'] == 'Some HTML description.'
    assert result['duration'] == 123.456
    assert result['timestamp'] == 1609459200
    assert result['uploader'] == 'tester'
    assert result['uploader_id'] == '42'
    assert result['view_count'] == 1000
    assert result['like_count'] == 200
    assert result['comment_count'] == 30
    assert result['tags'] == ['tag1', 'tag2']


def test_missing_tags_and_html_cleaning():
    """Test extraction when tags are missing and body contains HTML."""
    payload = {
        'title': 'No Tags',
        'source_url': {'mp4_url': 'https://example.com/no_tags.mp4'},
        'body': '<div>Line1<br>Line2</div>',
        'duration': 5000,
        'created_at_i': 1610000000,
        'user': {'username': 'no_tags_user', 'id': 99},
        'total_views_count': None,
        'hearts_count': None,
        'comments_count': None,
        # tags key absent
    }
    ie = DummyHitRecordIE(payload)
    result = ie._real_extract('https://hitrecord.org/records/67890')
    assert result['tags'] is None
    assert result['description'] == 'Line1Line2'
    assert result['duration'] == 5.0
    assert result['view_count'] is None
    assert result['like_count'] is None
    assert result['comment_count'] is None


def test_invalid_duration_and_missing_user():
    """Test extraction when duration is not a number and user information is missing."""
    payload = {
        'title': 'Invalid Duration',
        'source_url': {'mp4_url': 'https://example.com/invalid.mp4'},
        'body': 'Plain text',
        'duration': 'not_a_number',
        'created_at_i': 'not_an_int',
        # user key missing
        'total_views_count': 'NaN',
        'hearts_count': 'NaN',
        'comments_count': 'NaN',
        'tags': [{'text': 'single'}],
    }
    ie = DummyHitRecordIE(payload)
    result = ie._real_extract('https://hitrecord.org/records/11111')
    assert result['duration'] is None
    assert result['timestamp'] is None
    assert result['uploader'] is None
    assert result['uploader_id'] is None
    assert result['view_count'] is None
    assert result['like_count'] is None
    assert result['comment_count'] is None
    assert result['tags'] == ['single']
