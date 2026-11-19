import pytest
from youtube_dl.extractor.tudou import TudouAlbumIE

# Helper to create a fake downloader that records calls
class FakeDownloader:
    def __init__(self, json_data):
        self.json_data = json_data
        self.called_with = []

    def _download_json(self, url, video_id):
        self.called_with.append((url, video_id))
        return self.json_data

def test_tudou_album_normal_extraction(tmp_path):
    # Arrange: fake JSON with two items
    fake_json = {
        'items': [
            {'icode': 'abc123', 'kw': 'video1'},
            {'icode': 'def456', 'kw': 'video2'},
        ]
    }
    downloader = FakeDownloader(fake_json)
    ie = TudouAlbumIE(downloader=downloader)

    # Act
    result = ie.extract('http://www.tudou.com/albumplay/abc123def45.html')

    # Assert
    assert result['id'] == 'abc123def45'
    assert result['entries'] == [
        {'url': 'http://www.tudou.com/programs/view/abc123', 'ie_key': 'Tudou', 'id': 'abc123', 'title': 'video1'},
        {'url': 'http://www.tudou.com/programs/view/def456', 'ie_key': 'Tudou', 'id': 'def456', 'title': 'video2'},
    ]
    # Ensure the downloader was called with the correct URL
    assert downloader.called_with == [('http://www.tudou.com/tvp/alist.action?acode=abc123def45', 'abc123def45')]

def test_tudou_album_empty_items(tmp_path):
    # Arrange: fake JSON with empty items list
    fake_json = {'items': []}
    downloader = FakeDownloader(fake_json)
    ie = TudouAlbumIE(downloader=downloader)

    # Act
    result = ie.extract('http://www.tudou.com/albumcover/xyz98765432.html')

    # Assert
    assert result['id'] == 'xyz98765432'
    assert result['entries'] == []
    assert downloader.called_with == [('http://www.tudou.com/tvp/alist.action?acode=xyz98765432', 'xyz98765432')]

def test_tudou_album_missing_items_key(tmp_path):
    # Arrange: fake JSON missing 'items' key
    fake_json = {'no_items': []}
    downloader = FakeDownloader(fake_json)
    ie = TudouAlbumIE(downloader=downloader)

    # Act & Assert: should raise a KeyError when accessing 'items'
    with pytest.raises(KeyError):
        ie.extract('http://www.tudou.com/albumplay/12345678901.html')
