import re
import json
import pytest
from youtube_dl.extractor.nrk import NRKTVEpisodeIE, NRKIE, NRKTVIE


class DummyNRKTVEpisodeIE(NRKTVEpisodeIE):
    """Subclass that overrides network calls for deterministic testing."""

    def __init__(self, webpage, json_ld=None, meta_id=None):
        super().__init__()
        self._dummy_webpage = webpage
        self._dummy_json_ld = json_ld
        self._dummy_meta_id = meta_id

    def _download_webpage(self, url, display_id, note=None, errnote=None, *, data=None, headers=None, timeout=None, err=None):
        return self._dummy_webpage

    def _search_json_ld(self, webpage, display_id, default=None):
        if self._dummy_json_ld is not None:
            return self._dummy_json_ld
        return default

    def _html_search_meta(self, name, webpage, default=None):
        if self._dummy_meta_id is not None:
            return self._dummy_meta_id
        return default

    def _search_regex(self, pattern, string, name, default=None):
        # Fallback to regex search if needed
        m = re.search(pattern, string)
        return m.group(1) if m else default


def test_extract_with_json_ld():
    """Test extraction when JSON‑LD contains the NRK id."""
    # Prepare a minimal webpage containing JSON‑LD with @id
    json_ld = {
        "@id": "MUHH36005220",
        "name": "Hellums kro - 2. Kro, krig og kjærlighet",
        "description": "Some description",
        "duration": 1563.92,
        "ageLimit": 6,
        "episode": "2. Kro, krig og kjærlighet",
        "series": "Hellums kro"
    }
    webpage = f'<script type="application/ld+json">{json.dumps(json_ld)}</script>'
    extractor = DummyNRKTVEpisodeIE(webpage, json_ld=json_ld)
    info = extractor._real_extract(
        'https://tv.nrk.no/serie/hellums-kro/sesong/1/episode/2')
    assert info['id'] == 'MUHH36005220'
    assert info['season_number'] == 1
    assert info['episode_number'] == 2
    assert info['title'] == 'Hellums kro - 2. Kro, krig og kjærlighet'
    assert info['age_limit'] == 6
    assert info['ie_key'] == NRKIE.ie_key()
    assert info['url'] == 'nrk:MUHH36005220'


def test_extract_with_meta_tag():
    """Test extraction when JSON‑LD is missing but meta tag provides NRK id."""
    # Webpage without JSON‑LD but with meta tag
    webpage = '<meta name="nrk:program-id" content="MSUI14000816">'
    extractor = DummyNRKTVEpisodeIE(webpage, meta_id="MSUI14000816")
    info = extractor._real_extract(
        'https://tv.nrk.no/serie/backstage/sesong/1/episode/8')
    assert info['id'] == 'MSUI14000816'
    assert info['season_number'] == 1
    assert info['episode_number'] == 8
    assert info['title'] == 'Backstage - 8. episode'
    assert info['age_limit'] == 0
    assert info['url'] == 'nrk:MSUI14000816'


def test_extract_fallback_regex():
    """Test extraction when both JSON‑LD and meta tag are missing, fallback to regex."""
    # Webpage with data-program-id attribute
    webpage = '<div data-program-id="MUHH36005220"></div>'
    extractor = DummyNRKTVEpisodeIE(webpage, json_ld=None, meta_id=None)
    # Override _search_regex pattern to match NRKTVIE._EPISODE_RE
    info = extractor._real_extract(
        'https://tv.nrk.no/serie/hellums-kro/sesong/1/episode/2')
    assert info['id'] == 'MUHH36005220'
    assert info['season_number'] == 1
    assert info['episode_number'] == 2
    assert info['url'] == 'nrk:MUHH36005220'
