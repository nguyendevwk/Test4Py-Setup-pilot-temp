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
    info = {"title": "Song Title - Artist Name"}
    _, updated_info = pp.run(info)
    assert updated_info["title"] == "Song Title"
    assert updated_info["artist"] == "Artist Name"
    assert any("[fromtitle] parsed title: Song Title" in m for m in downloader.messages)
    assert any("[fromtitle] parsed artist: Artist Name" in m for m in downloader.messages)

def test_no_placeholder_title_format():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "Static Title")
    info = {"title": "Static Title"}
    _, updated_info = pp.run(info)
    assert updated_info["title"] == "Static Title"
    assert "parsed" not in "".join(downloader.messages)

def test_title_mismatch_and_error_message():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "%(artist)s - %(title)s")
    info = {"title": "Song Title - Artist Name"}
    _, updated_info = pp.run(info)
    assert updated_info == info
    assert any("[fromtitle] Could not interpret title" in m for m in downloader.messages)
