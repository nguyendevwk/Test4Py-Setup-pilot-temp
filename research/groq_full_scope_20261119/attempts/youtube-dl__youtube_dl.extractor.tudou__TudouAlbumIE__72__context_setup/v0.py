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
    result = ie.extract('http://www.tudou.com/albumplay/xyz789.html')

    # Assert
    assert result['id'] == 'xyz789'
    assert result['entries'] == [
        {
            '_type': 'url',
            'url': 'http://www.tudou.com/programs/view/abc123',
            'ie_key': 'Tudou',
            'id': 'abc123',
            'title': 'video1',
        },
        {
            '_type': 'url',
            'url': 'http://www.tudou.com/programs/view/def456',
            'ie_key': 'Tudou',
            'id': 'def456',
            'title': 'video2',
        },
    ]
    # Verify that the downloader was called with the correct URL
    assert downloader.called_with == [
        ('http://www.tudou.com/tvp/alist.action?acode=xyz789', 'xyz789')
    ]

def test_tudou_album_empty_items(tmp_path):
    # Arrange: fake JSON with empty items list
    fake_json = {'items': []}
    downloader = FakeDownloader(fake_json)
    ie = TudouAlbumIE(downloader=downloader)

    # Act
    result = ie.extract('http://www.tudou.com/albumcover/abc123.html')

    # Assert
    assert result['id'] == 'abc123'
    assert result['entries'] == []

def test_tudou_album_missing_items_key(tmp_path):
    # Arrange: fake JSON missing 'items' key
    fake_json = {'not_items': []}
    downloader = FakeDownloader(fake_json)
    ie = TudouAlbumIE(downloader=downloader)

    # Act & Assert: should raise a KeyError when accessing album_data['items']
    with pytest.raises(KeyError):
        ie.extract('http://www.tudou.com/albumplay/def456.html')
