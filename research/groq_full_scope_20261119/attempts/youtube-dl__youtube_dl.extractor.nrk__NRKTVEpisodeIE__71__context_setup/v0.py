import re
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodeIE, NRKIE, NRKTVIE

# Helper to create a minimal extractor instance with a dummy downloader
def make_extractor():
    return NRKTVEpisodeIE()

# Test normal extraction with all required data present
def test_nrk_episode_extraction_normal(monkeypatch):
    extractor = make_extractor()
    url = "https://tv.nrk.no/serie/hellums-kro/sesong/1/episode/2"

    # Mock the webpage download to return a simple HTML
    monkeypatch.setattr(
        extractor, "_download_webpage",
        lambda u, d: f'<html><meta name="nrk:program-id" content="MUHH36005220"></html>'
    )

    # Mock JSON-LD search to return a dict with @id
    monkeypatch.setattr(
        extractor, "_search_json_ld",
        lambda w, d, default: {"@id": "MUHH36005220"}
    )

    # Ensure the regex search is not called
    monkeypatch.setattr(
        extractor, "_search_regex",
        lambda *args, **kwargs: None
    )

    # Perform extraction
    info = extractor._real_extract(url)

    # Assertions on the returned info dict
    assert info["id"] == "MUHH36005220"
    assert info["url"] == "nrk:MUHH36005220"
    assert info["ie_key"] == NRKIE.ie_key()
    assert info["season_number"] == 1
    assert info["episode_number"] == 2
    assert info["_type"] == "url"

# Test extraction when JSON-LD is missing but meta tag provides nrk id
def test_nrk_episode_extraction_meta(monkeypatch):
    extractor = make_extractor()
    url = "https://tv.nrk.no/serie/backstage/sesong/1/episode/8"

    # Mock webpage download
    monkeypatch.setattr(
        extractor, "_download_webpage",
        lambda u, d: f'<html><meta name="nrk:program-id" content="MSUI14000816"></html>'
    )

    # Mock JSON-LD to return empty dict
    monkeypatch.setattr(
        extractor, "_search_json_ld",
        lambda w, d, default: {}
    )

    # Mock meta search to return the id
    monkeypatch.setattr(
        extractor, "_html_search_meta",
        lambda name, w, default: "MSUI14000816"
    )

    # Ensure regex search is not called
    monkeypatch.setattr(
        extractor, "_search_regex",
        lambda *args, **kwargs: None
    )

    info = extractor._real_extract(url)

    assert info["id"] == "MSUI14000816"
    assert info["url"] == "nrk:MSUI14000816"
    assert info["season_number"] == 1
    assert info["episode_number"] == 8

# Test extraction failure when nrk id does not match expected pattern
def test_nrk_episode_extraction_invalid_id(monkeypatch):
    extractor = make_extractor()
    url = "https://tv.nrk.no/serie/invalid/sesong/1/episode/1"

    # Mock webpage download
    monkeypatch.setattr(
        extractor, "_download_webpage",
        lambda u, d: f'<html><meta name="nrk:program-id" content="INVALID123"></html>'
    )

    # Mock JSON-LD to return empty dict
    monkeypatch.setattr(
        extractor, "_search_json_ld",
        lambda w, d, default: {}
    )

    # Mock meta search to return the invalid id
    monkeypatch.setattr(
        extractor, "_html_search_meta",
        lambda name, w, default: "INVALID123"
    )

    # Ensure regex search is not called
    monkeypatch.setattr(
        extractor, "_search_regex",
        lambda *args, **kwargs: None
    )

    # Extraction should raise an AssertionError due to pattern mismatch
    with pytest.raises(AssertionError):
        extractor._real_extract(url)
