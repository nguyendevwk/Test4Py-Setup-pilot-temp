import pytest
from youtube_dl.extractor.hitrecord import HitRecordIE
from youtube_dl.utils import clean_html

def test_normal_extraction(monkeypatch):
    # Simulate a typical API response
    api_response = {
        'title': 'Test Video',
        'source_url': {'mp4_url': 'https://example.com/video.mp4'},
        'body': '<p>Some <b>description</b></p>',
        'duration': 123456,          # milliseconds
        'created_at_i': 1609459200,  # 2021-01-01
        'user': {'username': 'tester', 'id': 42},
        'total_views_count': 1000,
        'hearts_count': 200,
        'comments_count': 30,
        'tags': [{'text': 'tag1'}, {'text': 'tag2'}],
    }

    def fake_download_json(url, video_id):
        assert video_id == '12345'
        return api_response

    monkeypatch.setattr(HitRecordIE, '_download_json', fake_download_json)

    ie = HitRecordIE()
    result = ie._real_extract('https://hitrecord.org/records/12345')

    assert result['id'] == '12345'
    assert result['url'] == 'https://example.com/video.mp4'
    assert result['title'] == 'Test Video'
    assert result['description'] == clean_html(api_response['body'])
    assert result['duration'] == 123.456  # 123456 ms -> 123.456 s
    assert result['timestamp'] == 1609459200
    assert result['uploader'] == 'tester'
    assert result['uploader_id'] == '42'
    assert result['view_count'] == 1000
    assert result['like_count'] == 200
    assert result['comment_count'] == 30
    assert result['tags'] == ['tag1', 'tag2']

def test_missing_optional_fields(monkeypatch):
    # API response missing optional fields like tags and body
    api_response = {
        'title': 'No Tags',
        'source_url': {'mp4_url': 'https://example.com/no_tags.mp4'},
        'duration': 5000,          # 5 seconds
        'created_at_i': 1610000000,
        'user': {'username': 'no_tags_user', 'id': 99},
        'total_views_count': None,
        'hearts_count': None,
        'comments_count': None,
    }

    def fake_download_json(url, video_id):
        return api_response

    monkeypatch.setattr(HitRecordIE, '_download_json', fake_download_json)

    ie = HitRecordIE()
    result = ie._real_extract('https://hitrecord.org/records/99999')

    assert result['tags'] is None
    assert result['description'] is None
    assert result['duration'] == 5.0
    assert result['view_count'] is None
    assert result['like_count'] is None
    assert result['comment_count'] is None

def test_invalid_url_raises(monkeypatch):
    # Ensure that an invalid URL triggers a ValueError from _match_id
    ie = HitRecordIE()
    with pytest.raises(ValueError):
        ie._real_extract('https://hitrecord.org/invalid/abc')
