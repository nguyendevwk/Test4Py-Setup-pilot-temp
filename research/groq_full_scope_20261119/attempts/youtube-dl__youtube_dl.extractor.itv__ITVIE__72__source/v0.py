import json
import re
import pytest
from youtube_dl.extractor.itv import ITVIE
from youtube_dl.utils import determine_ext, parse_duration, clean_html, get_element_by_class

# Helper to create a minimal webpage with required attributes
def build_webpage(video_id, data_video_id, hmac, base_url, media_files, subtitles):
    attrs = {
        'data-video-id': data_video_id,
        'data-video-hmac': hmac,
        'data-video-playlist': f'https://example.com/playlist/{video_id}.json',
    }
    attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
    media_html = ''.join(f'<div href="{mf}"></div>' for mf in media_files)
    sub_html = ''.join(f'<div href="{s}"></div>' for s in subtitles)
    return f'''
    <html>
      <head>
        <meta property="og:title" content="Test Title"/>
        <script type="application/ld+json">
          {{ "@type": "TVEpisode", "name": "Episode", "description": "Desc" }}
        </script>
      </head>
      <body>
        <div id="video" {attr_str}></div>
        <div class="episode-info__synopsis"> <p>Synopsis</p> </div>
        {media_html}
        {sub_html}
      </body>
    </html>
    '''

# Mock JSON playlist response
def build_playlist(base_url, media_files, subtitles):
    return {
        "Playlist": {
            "Video": {
                "Base": base_url,
                "MediaFiles": [{"Href": mf} for mf in media_files],
                "Subtitles": [{"Href": s} for s in subtitles],
                "Duration": "PT1H2M3S"
            }
        }
    }

@pytest.fixture
def extractor():
    return ITVIE()

def test_itvie_normal_extraction(monkeypatch, extractor):
    video_id = "abc123"
    webpage = build_webpage(
        video_id,
        data_video_id="vid123",
        hmac="abcd",
        base_url="https://cdn.example.com/",
        media_files=["/video1.mp4", "/video2.m3u8"],
        subtitles=["https://sub.example.com/sub.vtt"]
    )
    playlist = build_playlist(
        base_url="https://cdn.example.com/",
        media_files=["/video1.mp4", "/video2.m3u8"],
        subtitles=["https://sub.example.com/sub.vtt"]
    )

    monkeypatch.setattr(ITVIE, "_download_webpage", lambda self, url, video_id: webpage)
    monkeypatch.setattr(ITVIE, "_download_json", lambda self, url, video_id, data, headers: playlist)

    info = extractor.extract(video_id)
    assert info["id"] == video_id
    assert info["title"] == "Test Title"
    assert info["description"] == "Synopsis"
    # formats should contain both mp4 and m3u8
    formats = info["formats"]
    assert any(f["url"] == "https://cdn.example.com/video1.mp4" for f in formats)
    assert any(f["url"].startswith("https://cdn.example.com/video2.m3u8") for f in formats)
    # subtitles
    subs = info["subtitles"]
    assert "en" in subs
    assert subs["en"][0]["url"] == "https://sub.example.com/sub.vtt"
    # duration parsed
    assert info["duration"] == 3723  # 1h2m3s in seconds

def test_itvie_missing_media(monkeypatch, extractor):
    video_id = "no_media"
    webpage = build_webpage(
        video_id,
        data_video_id="vid_no",
        hmac="abcd",
        base_url="https://cdn.example.com/",
        media_files=[],
        subtitles=[]
    )
    playlist = build_playlist(
        base_url="https://cdn.example.com/",
        media_files=[],
        subtitles=[]
    )
    monkeypatch.setattr(ITVIE, "_download_webpage", lambda self, url, video_id: webpage)
    monkeypatch.setattr(ITVIE, "_download_json", lambda self, url, video_id, data, headers: playlist)

    info = extractor.extract(video_id)
    assert info["id"] == video_id
    assert info["formats"] == []
    assert info["subtitles"] == {}

def test_itvie_invalid_json(monkeypatch, extractor):
    video_id = "bad_json"
    webpage = build_webpage(
        video_id,
        data_video_id="vid_bad",
        hmac="abcd",
        base_url="https://cdn.example.com/",
        media_files=["/video.mp4"],
        subtitles=[]
    )
    # Simulate JSON decode error by raising ValueError
    def bad_download_json(self, url, video_id, data, headers):
        raise ValueError("Invalid JSON")
    monkeypatch.setattr(ITVIE, "_download_webpage", lambda self, url, video_id: webpage)
    monkeypatch.setattr(ITVIE, "_download_json", bad_download_json)

    with pytest.raises(ValueError):
        extractor.extract(video_id)
