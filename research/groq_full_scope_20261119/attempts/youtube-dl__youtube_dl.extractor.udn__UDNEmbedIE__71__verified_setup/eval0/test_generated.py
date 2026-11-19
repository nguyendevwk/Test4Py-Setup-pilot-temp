import re
import pytest
from youtube_dl.extractor.udn import UDNEmbedIE
from youtube_dl.utils import determine_ext

# Helper to create a fake extractor with patched download methods
def make_extractor(page_content, video_url_map):
    ie = UDNEmbedIE()
    # Patch _download_webpage to return page_content for the main URL
    # and return the corresponding video URL for the API URLs
    def fake_download(url, video_id, note=None):
        if url == f"http://video.udn.com/embed/news/{video_id}":
            return page_content
        return video_url_map.get(url, "")
    ie._download_webpage = fake_download
    return ie

def test_extract_with_options_present(monkeypatch):
    # Page contains a valid options object
    page = (
        "var options = {"
        "video:{mp4:'/video_720p_500.mp4'},"
        "title:'Sample Video',"
        "poster:'/thumb.jpg'};"
    )
    # Video URL returned by the API endpoint
    video_url_map = {
        "http://video.udn.com/video_720p_500.mp4": "http://cdn.example.com/video_720p_500.mp4"
    }
    ie = make_extractor(page, video_url_map)
    result = ie._real_extract("http://video.udn.com/embed/news/12345")
    assert result["id"] == "12345"
    assert result["title"] == "Sample Video"
    assert result["thumbnail"] == "/thumb.jpg"
    # Only one format should be present
    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["url"] == "http://cdn.example.com/video_720p_500.mp4"
    assert fmt["format_id"] == "http-mp4"
    # Height and tbr should be parsed from the URL
    assert fmt["height"] == 720
    assert fmt["tbr"] == 500

def test_extract_with_options_missing(monkeypatch):
    # Page contains options string but no 'video' key, so fallback parsing is used
    page = (
        "var options = {"
        "title:'Fallback Title',"
        "poster:'/fallback.jpg'};"
        "var video = {mp4:'/fallback_480p_300.mp4'};"
    )
    video_url_map = {
        "http://video.udn.com/fallback_480p_300.mp4": "http://cdn.example.com/fallback_480p_300.mp4"
    }
    ie = make_extractor(page, video_url_map)
    result = ie._real_extract("http://video.udn.com/embed/news/67890")
    assert result["id"] == "67890"
    assert result["title"] == "Fallback Title"
    assert result["thumbnail"] == "/fallback.jpg"
    assert len(result["formats"]) == 1
    fmt = result["formats"][0]
    assert fmt["url"] == "http://cdn.example.com/fallback_480p_300.mp4"
    assert fmt["format_id"] == "http-mp4"
    assert fmt["height"] == 480
    assert fmt["tbr"] == 300

def test_extract_youtube_redirect(monkeypatch):
    # Page contains a youtube redirect in the video dict
    page = (
        "var options = {"
        "video:{youtube:'https://www.youtube.com/watch?v=dQw4w9WgXcQ'},"
        "title:'YouTube Video'};"
    )
    ie = make_extractor(page, {})
    result = ie._real_extract("http://video.udn.com/embed/news/11111")
    # The extractor should return a url_result pointing to YouTube
    assert result["id"] == "11111"
    assert result["title"] == "YouTube Video"
    assert result["thumbnail"] is None
    # The result should be a dict with a 'url' key pointing to the YouTube URL
    assert result["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert result["ie_key"] == "Youtube"
