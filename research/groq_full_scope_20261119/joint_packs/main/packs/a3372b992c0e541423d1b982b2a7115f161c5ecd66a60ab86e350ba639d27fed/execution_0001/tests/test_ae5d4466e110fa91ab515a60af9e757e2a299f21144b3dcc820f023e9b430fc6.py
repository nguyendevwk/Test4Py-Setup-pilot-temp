import pytest
from youtube_dl.extractor.hitrecord import HitRecordIE
from youtube_dl.utils import clean_html

# Helper to create a fake downloader that returns a predefined JSON
class FakeDownloader:
    def __init__(self, json_data):
        self.json_data = json_data
        self.called = False

    def _download_json(self, url, video_id):
        self.called = True
        return self.json_data

@pytest.fixture
def extractor():
    return HitRecordIE()

def test_normal_extraction(extractor):
    # Arrange: fake JSON with all fields
    fake_json = {
        'title': 'Test Video',
        'source_url': {'mp4_url': 'https://example.com/video.mp4'},
        'body': '<p>Some <b>description</b></p>',
        'duration': 120000,  # milliseconds
        'created_at_i': 1609459200,
        'user': {'username': 'tester', 'id': 42},
        'total_views_count': 1000,
        'hearts_count': 150,
        'comments_count': 20,
        'tags': [{'text': 'tag1'}, {'text': 'tag2'}],
    }
    extractor._download_json = FakeDownloader(fake_json)._download_json

    # Act
    result = extractor._real_extract('https://hitrecord.org/records/12345')

    # Assert
    assert result['id'] == '12345'
    assert result['url'] == 'https://example.com/video.mp4'
    assert result['title'] == 'Test Video'
    assert result['description'] == 'Some description'
    assert result['duration'] == 120.0
    assert result['timestamp'] == 1609459200
    assert result['uploader'] == 'tester'
    assert result['uploader_id'] == '42'
    assert result['view_count'] == 1000
    assert result['like_count'] == 150
    assert result['comment_count'] == 20
    assert result['tags'] == ['tag1', 'tag2']

def test_missing_tags_and_optional_fields(extractor):
    # Arrange: fake JSON missing tags and optional numeric fields
    fake_json = {
        'title': 'No Tags',
        'source_url': {'mp4_url': 'https://example.com/no_tags.mp4'},
        'body': None,
        'duration': None,
        'created_at_i': None,
        'user': {'username': 'anon', 'id': '999'},
        'total_views_count': None,
        'hearts_count': None,
        'comments_count': None,
        # 'tags' key absent
    }
    extractor._download_json = FakeDownloader(fake_json)._download_json

    # Act
    result = extractor._real_extract('https://hitrecord.org/records/67890')

    # Assert
    assert result['id'] == '67890'
    assert result['url'] == 'https://example.com/no_tags.mp4'
    assert result['title'] == 'No Tags'
    assert result['description'] is None
    assert result['duration'] is None
    assert result['timestamp'] is None
    assert result['uploader'] == 'anon'
    assert result['uploader_id'] == '999'
    assert result['view_count'] is None
    assert result['like_count'] is None
    assert result['comment_count'] is None
    assert result['tags'] is None

def test_invalid_tag_entries(extractor):
    # Arrange: fake JSON with malformed tags
    fake_json = {
        'title': 'Bad Tags',
        'source_url': {'mp4_url': 'https://example.com/bad_tags.mp4'},
        'body': '<p>desc</p>',
        'duration': 30000,
        'created_at_i': 1610000000,
        'user': {'username': 'baduser', 'id': 123},
        'total_views_count': 10,
        'hearts_count': 2,
        'comments_count': 1,
        'tags': [
            {'text': 'good'},          # valid
            {'text': 123},             # invalid type
            {'no_text': 'missing'},    # missing key
            'just a string',           # not a dict
        ],
    }
    extractor._download_json = FakeDownloader(fake_json)._download_json

    # Act
    result = extractor._real_extract('https://hitrecord.org/records/11111')

    # Assert
    assert result['tags'] == ['good']
