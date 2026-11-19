import re
import pytest
from youtube_dl.postprocessor.metadatafromtitle import MetadataFromTitlePP

class DummyDownloader:
    def __init__(self):
        self.messages = []

    def to_screen(self, msg):
        self.messages.append(msg)

def test_normal_parsing_and_attribute_assignment():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "%(title)s - %(artist)s")
    info = {"title": "Hello - Adele"}
    _, updated_info = pp.run(info)
    assert updated_info["title"] == "Hello"
    assert updated_info["artist"] == "Adele"
    assert "[fromtitle] parsed title: Hello" in downloader.messages
    assert "[fromtitle] parsed artist: Adele" in downloader.messages

def test_no_placeholders_titleformat():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "Static Title")
    info = {"title": "Static Title"}
    _, updated_info = pp.run(info)
    assert updated_info["title"] == "Static Title"
    assert downloader.messages == []

def test_title_mismatch_shows_error_and_no_changes():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "%(title)s - %(artist)s")
    info = {"title": "Unmatched Title"}
    _, updated_info = pp.run(info)
    assert updated_info is info
    assert "[fromtitle] Could not interpret title of video as" in downloader.messages[0]
    assert "title" not in updated_info or updated_info["title"] == "Unmatched Title"
    assert "artist" not in updated_info
