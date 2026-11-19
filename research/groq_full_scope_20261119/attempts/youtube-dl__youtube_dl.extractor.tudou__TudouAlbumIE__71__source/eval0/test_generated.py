import pytest
from youtube_dl.extractor.tudou import TudouAlbumIE

# Helper to create a fake extractor instance with overridden _download_json
class FakeTudouAlbumIE(TudouAlbumIE):
    def __init__(self, fake_json):
        super().__init__()
        self._fake_json = fake_json

    def _download_json(self, url, video_id, note=None, errnote=None, data=None, headers=None, query=None, timeout=None, add_headers=None, add_query=None, add_data=None, add_note=None, add_errnote=None, add_timeout=None, add_add_headers=None, add_add_query=None, add_add_data=None, add_add_note=None, add_add_errnote=None, add_add_timeout=None, add_add_add_headers=None, add_add_add_query=None, add_add_add_data=None, add_add_add_note=None, add_add_add_errnote=None, add_add_add_timeout=None, add_add_add_add_headers=None, add_add_add_add_query=None, add_add_add_add_data=None, add_add_add_add_note=None, add_add_add_add_errnote=None, add_add_add_add_timeout=None, add_add_add_add_add_headers=None, add_add_add_add_add_query=None, add_add_add_add_add_data=None, add_add_add_add_add_note=None, add_add_add_add_add_errnote=None, add_add_add_add_add_timeout=None, add_add_add_add_add_add_headers=None, add_add_add_add_add_add_query=None, add_add_add_add_add_add_data=None, add_add_add_add_add_add_note=None, add_add_add_add_add_add_errnote=None, add_add_add_add_add_add_timeout=None, add_add_add_add_add_add_add_headers=None, add_add_add_add_add_add_add_query=None, add_add_add_add_add_add_add_data=None, add_add_add_add_add_add_add_note=None, add_add_add_add_add_add_add_errnote=None, add_add_add_add_add_add_add_timeout=None, add_add_add_add_add_add_add_add_headers=None, add_add_add_add_add_add_add_add_query=None, add_add_add_add_add_add_add_add_data=None, add_add_add_add_add_add_add_add_note=None, add_add_add_add_add_add_add_add_errnote=None, add_add_add_add_add_add_add_add_timeout=None, add_add_add_add_add_add_add_add_add_headers=None, add_add_add_add_add_add_add_add_add_query=None, add_add_add_add_add_add_add_add_add_data=None, add_add_add_add_add_add_add_add_add_note=None, add_add_add_add_add_add_add_add_add_errnote=None, add_add_add_add_add_add_add_add_add_timeout=None, add_add_add_add_add_add_add_add_add_add_headers=None, add_add_add_add_add_add_add_add_add_add_query=None, add_add_add_add_add_add_add_add_add_add_data=None, add_add_add_add_add_add_add_add_add_add_note=None, add_add_add_add_add_add_add_add_add_add_errnote=None, add_add_add_add_add_add_add_add_add_add_timeout=None, add_add_add_add_add_add_add_add_add_add_add_headers=None, add_add_add_add_add_add_add_add_add_add_add_query=None, add_add_add_add_add_add_add_add_add_add_add_data=None, add_add_add_add_add_add_add_add_add_add_add_note=None, add_add_add_add_add_add_add_add_add_add_add_errnote=None, add_add_add_add_add_add_add_add_add_add_add_timeout=None):
        return self._fake_json

def test_normal_extraction(tmp_path):
    # Fake JSON with two items
    fake_json = {
        'items': [
            {'icode': 'abc123', 'kw': 'video1'},
            {'icode': 'def456', 'kw': 'video2'}
        ]
    }
    ie = FakeTudouAlbumIE(fake_json)
    result = ie.extract('http://www.tudou.com/albumplay/xyzABC12345.html')
    assert result['id'] == 'xyzABC12345'
    assert result['entries'] == [
        {'url': 'http://www.tudou.com/programs/view/abc123', 'ie_key': 'Tudou', 'id': 'abc123', 'title': 'video1'},
        {'url': 'http://www.tudou.com/programs/view/def456', 'ie_key': 'Tudou', 'id': 'def456', 'title': 'video2'}
    ]

def test_empty_items_boundary(tmp_path):
    # Fake JSON with empty items list
    fake_json = {'items': []}
    ie = FakeTudouAlbumIE(fake_json)
    result = ie.extract('http://www.tudou.com/albumplay/empty12345.html')
    assert result['id'] == 'empty12345'
    assert result['entries'] == []

def test_missing_items_key_error(tmp_path):
    # Fake JSON missing 'items' key
    fake_json = {}
    ie = FakeTudouAlbumIE(fake_json)
    with pytest.raises(KeyError):
        ie.extract('http://www.tudou.com/albumplay/missing12345.html')
