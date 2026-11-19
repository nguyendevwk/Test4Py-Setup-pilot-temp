import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodeIE, NRKTVIE, NRKIE

# Helper to create a minimal extractor instance with a dummy downloader
def make_extractor():
    return NRKTVEpisodeIE()

# Test normal extraction with all required data present
def test_nrk_episode_extraction_normal(monkeypatch):
    extractor = make_extractor()
    url = "https://tv.nrk.no/serie/hellums-kro/sesong/1/episode/2"

    # Mock the webpage download to return a simple HTML containing the required meta tags
    monkeypatch.setattr(extractor, "_download_webpage", lambda u, d: "<html></html>")

    # Mock JSON-LD search to return a dict with @id
    mock_info = {"@id": "MUHH36005220"}
    monkeypatch.setattr(extractor, "_search_json_ld", lambda w, d, default: mock_info)

    # Ensure other search helpers are not called
    monkeypatch.setattr(extractor, "_html_search_meta", lambda *args, **kwargs: None)
    monkeypatch.setattr(extractor, "_search_regex", lambda *args, **kwargs: None)

    # Perform extraction
    result = extractor._real_extract(url)

    # Assertions on the returned info dict
    assert result["_type"] == "url"
    assert result["id"] == "MUHH36005220"
    assert result["url"] == "nrk:MUHH36005220"
    assert result["ie_key"] == NRKIE.ie_key()
    assert result["season_number"] == 1
    assert result["episode_number"] == 2
    assert result["display_id"] == "hellums-kro/sesong/1/episode/2"

# Test extraction when JSON-LD is missing but meta tag provides nrk id
def test_nrk_episode_extraction_meta_fallback(monkeypatch):
    extractor = make_extractor()
    url = "https://tv.nrk.no/serie/backstage/sesong/1/episode/8"

    monkeypatch.setattr(extractor, "_download_webpage", lambda u, d: "<html></html>")

    # JSON-LD returns empty dict
    monkeypatch.setattr(extractor, "_search_json_ld", lambda w, d, default: {})

    # Meta tag returns the nrk id
    monkeypatch.setattr(extractor, "_html_search_meta",
                       lambda name, w, default: "MSUI14000816" if name == "nrk:program-id" else default)

    # Ensure regex fallback is not used
    monkeypatch.setattr(extractor, "_search_regex", lambda *args, **kwargs: None)

    result = extractor._real_extract(url)

    assert result["id"] == "MSUI14000816"
    assert result["url"] == "nrk:MSUI14000816"
    assert result["season_number"] == 1
    assert result["episode_number"] == 8

# Test that an invalid nrk id raises an AssertionError
def test_nrk_episode_extraction_invalid_id(monkeypatch):
    extractor = make_extractor()
    url = "https://tv.nrk.no/serie/invalid/sesong/1/episode/1"

    monkeypatch.setattr(extractor, "_download_webpage", lambda u, d: "<html></html>")

    # Provide an invalid nrk id that does not match the expected pattern
    monkeypatch.setattr(extractor, "_search_json_ld", lambda w, d, default: {"@id": "INVALID_ID"})

    monkeypatch.setattr(extractor, "_html_search_meta", lambda *args, **kwargs: None)
    monkeypatch.setattr(extractor, "_search_regex", lambda *args, **kwargs: None)

    with pytest.raises(AssertionError):
        extractor._real_extract(url)
