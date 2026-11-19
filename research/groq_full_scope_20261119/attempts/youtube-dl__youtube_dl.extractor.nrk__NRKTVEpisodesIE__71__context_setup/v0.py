import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodesIE

# Helper to create a minimal extractor instance
def make_extractor():
    return NRKTVEpisodesIE()

def test_normal_extraction(monkeypatch):
    """Test that a normal NRK TV episodes page is parsed correctly."""
    sample_html = """
    <html>
    <h1>Nytt på nytt, sesong: 201210</h1>
    <div data-episode="12345"></div>
    <div data-episode="67890"></div>
    <div data-episode="54321"></div>
    <div data-episode="98765"></div>
    </html>
    """
    # Patch the download method to return our sample HTML
    monkeypatch.setattr(NRKTVEpisodesIE, "_download_webpage", lambda self, url, playlist_id: sample_html)

    extractor = make_extractor()
    result = extractor._real_extract("https://tv.nrk.no/program/episodes/nytt-paa-nytt/69031")

    # Verify playlist metadata
    assert result["id"] == "69031"
    assert result["title"] == "Nytt på nytt, sesong: 201210"
    assert result["description"] is None  # _extract_description is a stub returning None

    # Verify entries
    entries = result["entries"]
    assert len(entries) == 4
    expected_ids = ["12345", "67890", "54321", "98765"]
    for entry, expected_id in zip(entries, expected_ids):
        assert entry["url"] == f"nrk:{expected_id}"
        assert entry["ie_key"] == "NRKIE"

def test_missing_title(monkeypatch):
    """Test that _extract_title returns None when no <h1> tag is present."""
    sample_html = """
    <html>
    <div data-episode="11111"></div>
    </html>
    """
    monkeypatch.setattr(NRKTVEpisodesIE, "_download_webpage", lambda self, url, playlist_id: sample_html)

    extractor = make_extractor()
    title = extractor._extract_title(sample_html)
    assert title is None

def test_no_entries(monkeypatch):
    """Test that an empty list of entries is returned when no data-episode tags are found."""
    sample_html = """
    <html>
    <h1>Empty playlist</h1>
    </html>
    """
    monkeypatch.setattr(NRKTVEpisodesIE, "_download_webpage", lambda self, url, playlist_id: sample_html)

    extractor = make_extractor()
    result = extractor._real_extract("https://tv.nrk.no/program/episodes/empty/12345")

    assert result["id"] == "12345"
    assert result["title"] == "Empty playlist"
    assert result["entries"] == []
