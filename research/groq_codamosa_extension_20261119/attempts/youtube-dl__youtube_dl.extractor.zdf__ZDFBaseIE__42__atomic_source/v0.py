import json
import re
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass that overrides network calls for testing."""
    def __init__(self, json_data):
        super().__init__()
        self._json_data = json_data

    def _download_json(self, url, video_id, note, headers=None):
        # Return the pre‑provided JSON data regardless of URL
        return self._json_data

    def _parse_json(self, json_str, video_id):
        return json.loads(json_str)

    def _extract_m3u8_formats(self, *args, **kwargs):
        return [{'url': 'http://example.com/stream.m3u8', 'format_id': 'hls'}]

    def _extract_f4m_formats(self, *args, **kwargs):
        return [{'url': 'http://example.com/stream.f4m', 'format_id': 'hds'}]

    def _sort_formats(self, formats):
        # Simple sort by quality value
        formats.sort(key=lambda f: f.get('quality', 0))

    def _search_regex(self, pattern, string, name, default=None, fatal=True, group=None):
        m = re.search(pattern, string)
        if m:
            return m.group(group or 0)
        if fatal:
            raise ValueError(f"Regex {name} not found")
        return default

def test_extract_subtitles_basic():
    """Test that subtitles are extracted correctly from a simple JSON structure."""
    src = {
        'captions': [
            {'uri': 'http://example.com/sub_de.vtt', 'language': 'deu'},
            {'uri': 'http://example.com/sub_en.vtt', 'language': 'eng'},
            {'uri': None, 'language': 'deu'},  # should be ignored
        ]
    }
    ie = DummyZDFIE({})
    subs = ie._extract_subtitles(src)
    assert 'deu' in subs
    assert 'eng' in subs
    assert len(subs['deu']) == 1
    assert subs['deu'][0]['url'] == 'http://example.com/sub_de.vtt'
    assert subs['eng'][0]['url'] == 'http://example.com/sub_en.vtt'

def test_extract_format_m3u8_and_f4m():
    """Test that _extract_format correctly handles m3u8 and f4m URLs."""
    ie = DummyZDFIE({})
    formats = []
    seen = set()
    # m3u8 case
    meta_m3u8 = {
        'url': 'http://example.com/video.m3u8',
        'mimeType': 'application/x-mpegURL',
        'type': 'video',
        'quality': 'high',
        'mimeCodec': 'video/mp4; codecs="avc1.64001F"',
        'language': 'deu'
    }
    ie._extract_format('vid123', formats, seen, meta_m3u8)
    assert any(f['format_id'] == 'hls' for f in formats)
    # f4m case
    meta_f4m = {
        'url': 'http://example.com/video.f4m',
        'mimeType': 'application/f4m+xml',
        'type': 'video',
        'quality': 'low',
        'mimeCodec': 'video/mp4; codecs="avc1.64001F"',
        'language': 'deu'
    }
    ie._extract_format('vid123', formats, seen, meta_f4m)
    assert any(f['format_id'] == 'hds' for f in formats)
    # Regular case
    meta_http = {
        'url': 'http://example.com/video.mp4',
        'mimeType': 'video/mp4',
        'type': 'video',
        'quality': 'med',
        'mimeCodec': 'video/mp4; codecs="avc1.64001F"',
        'language': 'deu'
    }
    ie._extract_format('vid123', formats, seen, meta_http)
    assert any(f['format_id'] == 'http-video-med' for f in formats)
    # Duplicate URL should not be added again
    prev_len = len(formats)
    ie._extract_format('vid123', formats, seen, meta_http)
    assert len(formats) == prev_len

def test_extract_ptmd_parsing_and_duration(tmp_path):
    """Test that _extract_ptmd parses priority list and calculates duration."""
    # Prepare a fake API response
    ptmd_response = {
        'basename': 'test_video',
        'attributes': {'duration': {'value': 123456}},
        'priorityList': [
            {
                'formitaeten': [
                    {
                        'qualities': [
                            {
                                'audio': {'tracks': [{'uri': 'http://a1', 'language': 'deu'}]},
                                'quality': 'low'
                            },
                            {
                                'audio': {'tracks': [{'uri': 'http://a2', 'language': 'eng'}]},
                                'quality': 'high'
                            }
                        ],
                        'type': 'audio',
                        'mimeType': 'audio/mp4',
                        'mimeCodec': 'audio/mp4; codecs="mp4a.40.2"'
                    }
                ],
                'type': 'audio'
            }
        ],
        'captions': [
            {'uri': 'http://sub.vtt', 'language': 'deu'}
        ]
    }
    # Write the JSON to a temporary file and use its path as the URL
    json_path = tmp_path / 'ptmd.json'
    json_path.write_text(json.dumps(ptmd_response))
    ie = DummyZDFIE(ptmd_response)
    result = ie._extract_ptmd(str(json_path), 'vid123', api_token=None, referrer=None)
    assert result['id'] == 'test_video'
    assert result['duration'] == 123.456  # 123456 ms -> 123.456 s
    # Two formats should be extracted
    assert len(result['formats']) == 2
    # Subtitles extracted
    assert 'deu' in result['subtitles']
    assert result['subtitles']['deu'][0]['url'] == 'http://sub.vtt'
