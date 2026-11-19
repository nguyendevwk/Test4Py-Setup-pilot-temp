import pytest
from youtube_dl.extractor.tudou import TudouPlaylistIE

class DummyTudouPlaylistIE(TudouPlaylistIE):
    """Subclass that overrides _download_json to return controlled data."""
    def __init__(self, fake_json):
        super().__init__()
        self._fake_json = fake_json

    def _download_json(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None, add_dto=None, **kw):
        # Return the fake JSON data regardless of URL
        return self._fake_json


def test_normal_extraction(tmp_path):
    # Fake playlist data with two items
    fake_json = {
        "items": [
            {"icode": "abc123", "kw": "video1"},
            {"icode": "def456", "kw": "video2"},
        ]
    }
    ie = DummyTudouPlaylistIE(fake_json)
    result = ie.extract('http://www.tudou.com/listplay/zzdE77v6Mmo.html')
    assert result['id'] == 'zzdE77v6Mmo'
    assert result['entries'] == [
        {
            'url': 'http://www.tudou.com/programs/view/abc123',
            'ie_key': 'Tudou',
            'id': 'abc123',
            'title': 'video1',
        },
        {
            'url': 'http://www.tudou.com/programs/view/def456',
            'ie_key': 'Tudou',
            'id': 'def456',
            'title': 'video2',
        },
    ]


def test_empty_playlist(tmp_path):
    # Fake playlist data with no items
    fake_json = {"items": []}
    ie = DummyTudouPlaylistIE(fake_json)
    result = ie.extract('http://www.tudou.com/listplay/zzdE77v6Mmo.html')
    assert result['id'] == 'zzdE77v6Mmo'
    assert result['entries'] == []


def test_missing_items_key(tmp_path):
    # Fake playlist data missing 'items' key
    fake_json = {"no_items": []}
    ie = DummyTudouPlaylistIE(fake_json)
    with pytest.raises(KeyError):
        ie.extract('http://www.tudou.com/listplay/zzdE77v6Mmo.html')
