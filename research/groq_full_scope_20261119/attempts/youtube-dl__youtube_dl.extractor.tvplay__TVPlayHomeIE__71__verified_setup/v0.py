import pytest
from youtube_dl.extractor.tvplay import TVPlayHomeIE
from youtube_dl.utils import ExtractorError

class DummyTVPlayIE(TVPlayHomeIE):
    """A subclass that overrides network calls for deterministic testing."""
    def __init__(self, asset_json, m3u8_formats):
        super().__init__()
        self._asset_json = asset_json
        self._m3u8_formats = m3u8_formats

    def _download_json(self, url, video_id, *args, **kwargs):
        # Return the pre‑defined asset JSON regardless of URL
        return self._asset_json

    def _extract_m3u8_formats(self, url, video_id, ext, *args, **kwargs):
        # Return the pre‑defined formats list
        return self._m3u8_formats

    def _sort_formats(self, formats):
        # No-op sorting for test determinism
        pass


def test_full_extraction_with_all_fields():
    asset = {
        'movie': {'contentUrl': '/m3u8/stream.m3u8'},
        'assetId': '12345',
        'title': {'title': 'Test Title', 'summaryLong': 'Long summary', 'runTime': 'PT7M44S', 'titleBrief': 'Brief'},
        'imageUrl': '/images/cover.jpg',
        'metadata': {'seasonNumber': '2', 'episodeNumber': '5'},
        'tvSeriesTitle': 'Series Name',
        'tvSeasonTitle': 'Season 2',
    }
    formats = [{'format_id': '720p', 'url': 'http://example.com/720p.mp4'}]
    ie = DummyTVPlayIE(asset, formats)

    result = ie._real_extract('https://tvplay.tv3.lt/some/path-12345')

    assert result['id'] == '12345'
    assert result['title'] == 'Test Title'
    assert result['description'] == 'Long summary'
    assert result['thumbnails'] == [{'url': 'https://tvplay.tv3.lt/images/cover.jpg', 'ext': 'jpg'}]
    assert result['duration'] == 464  # 7*60 + 44
    assert result['series'] == 'Series Name'
    assert result['season'] == 'Season 2'
    assert result['season_number'] == 2
    assert result['episode'] == 'Brief'
    assert result['episode_number'] == 5
    assert result['formats'] == formats


def test_extraction_missing_optional_fields():
    asset = {
        'movie': {'contentUrl': '/m3u8/stream.m3u8'},
        'assetId': '67890',
        'title': {'title': 'No Image', 'summaryShort': 'Short', 'runTime': 'PT5M'},
        # No imageUrl, no metadata
        'tvSeriesTitle': 'Series X',
        'tvSeasonTitle': 'Season 1',
    }
    formats = [{'format_id': '480p', 'url': 'http://example.com/480p.mp4'}]
    ie = DummyTVPlayIE(asset, formats)

    result = ie._real_extract('https://play.tv3.lt/no-image-67890')

    assert result['id'] == '67890'
    assert result['title'] == 'No Image'
    assert result['description'] == 'Short'
    assert result['thumbnails'] is None
    assert result['duration'] == 300  # 5*60
    assert result['series'] == 'Series X'
    assert result['season'] == 'Season 1'
    assert result['season_number'] is None
    assert result['episode'] is None
    assert result['episode_number'] is None
    assert result['formats'] == formats


def test_invalid_url_raises_extractor_error():
    ie = TVPlayHomeIE()
    with pytest.raises(ExtractorError):
        ie._real_extract('https://invalid.url/notmatchingpattern')
