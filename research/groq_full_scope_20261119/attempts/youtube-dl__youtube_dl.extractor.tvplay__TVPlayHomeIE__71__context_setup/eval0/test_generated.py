import pytest
from youtube_dl.extractor.tvplay import TVPlayHomeIE
from youtube_dl.utils import parse_duration, int_or_none


class DummyTVPlayIE(TVPlayHomeIE):
    """A subclass that overrides network calls with deterministic data."""

    def __init__(self, asset_json, m3u8_formats):
        super().__init__()
        self._asset_json = asset_json
        self._m3u8_formats = m3u8_formats

    def _download_json(self, url, video_id, *args, **kwargs):
        # Return the pre‑defined asset JSON regardless of URL
        return self._asset_json

    def _extract_m3u8_formats(self, url, video_id, ext, protocol, **kwargs):
        # Return the pre‑defined formats list
        return self._m3u8_formats

    def _sort_formats(self, formats):
        # No-op sorting for deterministic order
        pass


def test_full_extraction_with_all_fields():
    asset = {
        'movie': {'contentUrl': 'http://example.com/stream.m3u8'},
        'assetId': '12345',
        'title': {'title': 'Test Title', 'summaryLong': 'Long summary',
                  'runTime': 'PT7M30S', 'titleBrief': 'Brief'},
        'imageUrl': '/images/cover.jpg',
        'metadata': {'seasonNumber': '2', 'episodeNumber': '5'},
        'tvSeriesTitle': 'Series Name',
        'tvSeasonTitle': 'Season 2',
    }
    formats = [{'format_id': '720p', 'url': 'http://example.com/720p.mp4'}]
    ie = DummyTVPlayIE(asset, formats)

    result = ie._real_extract('https://tvplay.tv3.lt/test/test-12345')

    assert result['id'] == '12345'
    assert result['title'] == 'Test Title'
    assert result['description'] == 'Long summary'
    assert result['thumbnails'] == [{'url': 'http://example.com/images/cover.jpg', 'ext': 'jpg'}]
    assert result['duration'] == parse_duration('PT7M30S')
    assert result['series'] == 'Series Name'
    assert result['season'] == 'Season 2'
    assert result['season_number'] == 2
    assert result['episode'] == 'Brief'
    assert result['episode_number'] == 5
    assert result['formats'] == formats


def test_missing_optional_fields():
    asset = {
        'movie': {'contentUrl': 'http://example.com/stream.m3u8'},
        'assetId': '67890',
        'title': {'title': 'No Image', 'summaryShort': 'Short summary',
                  'runTime': 'PT5M', 'titleBrief': 'Brief'},
        # No imageUrl, no metadata
        'tvSeriesTitle': 'Series Only',
        'tvSeasonTitle': 'Season 1',
    }
    formats = [{'format_id': '480p', 'url': 'http://example.com/480p.mp4'}]
    ie = DummyTVPlayIE(asset, formats)

    result = ie._real_extract('https://play.tv3.lt/no-image-67890')

    assert result['thumbnails'] is None
    assert result['season_number'] is None
    assert result['episode_number'] is None
    assert result['formats'] == formats


def test_missing_title_and_runtime():
    asset = {
        'movie': {'contentUrl': 'http://example.com/stream.m3u8'},
        'assetId': '54321',
        'title': {'title': 'Missing Fields'},
        # No summary, no runTime, no titleBrief
        'metadata': {'seasonNumber': '1'},
        'tvSeriesTitle': 'Series',
        'tvSeasonTitle': 'Season',
    }
    formats = [{'format_id': '360p', 'url': 'http://example.com/360p.mp4'}]
    ie = DummyTVPlayIE(asset, formats)

    result = ie._real_extract('https://tvplay.skaties.lv/missing/missing-54321')

    assert result['description'] is None
    assert result['duration'] is None
    assert result['episode'] is None
    assert result['episode_number'] is None
    assert result['season_number'] == 1
    assert result['formats'] == formats
