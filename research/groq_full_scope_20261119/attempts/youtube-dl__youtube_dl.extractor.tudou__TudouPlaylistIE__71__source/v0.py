import pytest
from youtube_dl.extractor.tudou import TudouPlaylistIE


class DummyTudouPlaylistIE(TudouPlaylistIE):
    """Subclass that overrides _download_json to return controlled data."""

    def __init__(self, fake_json):
        super().__init__()
        self._fake_json = fake_json

    def _download_json(self, url, video_id, *args, **kwargs):
        # ignore url and video_id, return the fake data
        return self._fake_json


def test_tudou_playlist_normal(tmp_path):
    # Prepare fake playlist data with two items
    fake_data = {
        "items": [
            {"icode": "abc123", "kw": "video1"},
            {"icode": "def456", "kw": "video2"},
        ]
    }
    ie = DummyTudouPlaylistIE(fake_data)
    result = ie.extract("http://www.tudou.com/listplay/zzdE77v6Mmo.html")

    # Assert that the result is a playlist with the correct id
    assert result["id"] == "zzdE77v6Mmo"
    assert result["entries"] == [
        {
            "_type": "url",
            "url": "http://www.tudou.com/programs/view/abc123",
            "ie_key": "Tudou",
            "id": "abc123",
            "title": "video1",
        },
        {
            "_type": "url",
            "url": "http://www.tudou.com/programs/view/def456",
            "ie_key": "Tudou",
            "id": "def456",
            "title": "video2",
        },
    ]


def test_tudou_playlist_empty_items(tmp_path):
    # Fake playlist data with no items
    fake_data = {"items": []}
    ie = DummyTudouPlaylistIE(fake_data)
    result = ie.extract("http://www.tudou.com/listplay/zzdE77v6Mmo.html")

    # The playlist should contain zero entries
    assert result["entries"] == []
    assert result["id"] == "zzdE77v6Mmo"


def test_tudou_playlist_missing_items_key(tmp_path):
    # Fake playlist data missing 'items' key
    fake_data = {"not_items": []}
    ie = DummyTudouPlaylistIE(fake_data)

    with pytest.raises(KeyError):
        ie.extract("http://www.tudou.com/listplay/zzdE77v6Mmo.html")
