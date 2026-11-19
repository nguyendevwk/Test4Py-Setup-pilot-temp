import pytest
from youtube_dl.extractor.hitrecord import HitRecordIE
from youtube_dl.utils import clean_html

# Helper to create a fake extractor instance with patched download method
def make_extractor(json_response):
    ie = HitRecordIE()
    ie._download_json = lambda url, video_id: json_response
    return ie

def test_normal_extraction():
    # Simulate a typical API response
    json_resp = {
        'title': 'Test Video',
        'source_url': {'mp4_url': 'https://example.com/video.mp4'},
        'body': '<p>Some <b>description</b></p>',
        'duration': 123456,          # milliseconds
        'created_at_i': 1609459200,  # 2021-01-01
        'user': {'username': 'tester', 'id': 42},
        'total_views_count': 1000,
        'hearts_count': 200,
        'comments_count': 10,
        'tags': [{'text': 'tag1'}, {'text': 'tag2'}]
    }
    ie = make_extractor(json_resp)
    result = ie._real_extract('https://hitrecord.org/records/12345')
    assert result['id'] == '12345'
    assert result['url'] == 'https://example.com/video.mp4'
    assert result['title'] == 'Test Video'
    assert result['description'] == 'Some description'
    assert result['duration'] == 123.456
    assert result['timestamp'] == 1609459200
    assert result['uploader'] == 'tester'
    assert result['uploader_id'] == '42'
    assert result['view_count'] == 1000
    assert result['like_count'] == 200
    assert result['comment_count'] == 10
    assert result['tags'] == ['tag1', 'tag2']

def test_missing_tags_and_optional_fields():
    # Response without tags and optional numeric fields
    json_resp = {
        'title': 'No Tags',
        'source_url': {'mp4_url': 'https://example.com/no_tags.mp4'},
        'body': None,
        'duration': None,
        'created_at_i': None,
        'user': {'username': 'anon', 'id': '99'},
        'total_views_count': None,
        'hearts_count': None,
        'comments_count': None,
        # 'tags' key absent
    }
    ie = make_extractor(json_resp)
    result = ie._real_extract('https://hitrecord.org/records/98765')
    assert result['tags'] is None
    assert result['description'] == ''
    assert result['duration'] is None
    assert result['timestamp'] is None
    assert result['view_count'] is None
    assert result['like_count'] is None
    assert result['comment_count'] is None

def test_invalid_url_raises():
    ie = HitRecordIE()
    with pytest.raises(ValueError):
        ie._real_extract('https://invalid.url/records/abc')
