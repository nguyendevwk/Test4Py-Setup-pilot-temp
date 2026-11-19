import pytest
from youtube_dl.extractor.tudou import TudouAlbumIE


def test_match_id_parses_valid_url():
    """Verify that the extractor correctly extracts the album id from a valid URL."""
    extractor = TudouAlbumIE()
    url = "http://www.tudou.com/albumplay/v5qckFJvNJg.html"
    album_id = extractor._match_id(url)
    assert album_id == "v5qckFJvNJg"


def test_real_extract_uses_download_json_and_builds_entries(monkeypatch):
    """Ensure that _real_extract calls _download_json and constructs playlist entries."""
    extractor = TudouAlbumIE()

    # Fake album data that _download_json would return
    fake_album_data = {
        "items": [
            {"icode": "abc123", "kw": "video1"},
            {"icode": "def456", "kw": "video2"},
        ]
    }

    # Patch _download_json to return the fake data
    def fake_download_json(url, video_id, note=None, data=None, headers=None, query=None, timeout=None):
        assert video_id == "v5qckFJvNJg"
        return fake_album_data

    monkeypatch.setattr(extractor, "_download_json", fake_download_json)

    # Call the extractor
    result = extractor._real_extract("http://www.tudou.com/albumplay/v5qckFJvNJg.html")

    # Verify the playlist result
    assert result["id"] == "v5qckFJvNJg"
    assert len(result["entries"]) == 2

    # Check each entry's structure
    for entry, item in zip(result["entries"], fake_album_data["items"]):
        assert entry["url"] == f"http://www.tudou.com/programs/view/{item['icode']}"
        assert entry["ie_key"] == "Tudou"
        assert entry["id"] == item["icode"]
        assert entry["title"] == item["kw"]


def test_real_extract_raises_on_invalid_url():
    """Confirm that an invalid URL raises a ValueError due to regex mismatch."""
    extractor = TudouAlbumIE()
    invalid_url = "http://www.tudou.com/invalid/12345.html"
    with pytest.raises(ValueError):
        extractor._match_id(invalid_url)
