import re
import pytest
from youtube_dl.postprocessor.metadatafromtitle import MetadataFromTitlePP


class DummyDownloader:
    def __init__(self):
        self.messages = []

    def to_screen(self, msg):
        self.messages.append(msg)


def test_normal_parsing_and_messages():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "%(title)s - %(artist)s")
    info = {"title": "Hello - Adele"}
    out, updated = pp.run(info)

    # The postprocessor should not modify the list of postprocessors
    assert out == []

    # The info dict should now contain the parsed fields
    assert updated["title"] == "Hello"
    assert updated["artist"] == "Adele"

    # Messages should report the parsed values
    assert any("[fromtitle] parsed title: Hello" in m for m in downloader.messages)
    assert any("[fromtitle] parsed artist: Adele" in m for m in downloader.messages)


def test_no_match_uses_original_title_and_logs_error():
    downloader = DummyDownloader()
    pp = MetadataFromTitlePP(downloader, "%(title)s - %(artist)s")
    info = {"title": "Just a random title"}
    out, updated = pp.run(info)

    # No changes to info
    assert updated == {"title": "Just a random title"}

    # An error message should be logged
    assert any(
        "[fromtitle] Could not interpret title of video as \"%s\"" % pp._titleformat
        in m for m in downloader.messages
    )


def test_format_to_regex_escapes_special_characters():
    downloader = DummyDownloader()
    # Title format contains regex special characters that must be escaped
    fmt = "%(artist)s & %(title)s (Live)"
    pp = MetadataFromTitlePP(downloader, fmt)

    # The regex should escape '&' and parentheses
    expected_regex = r'(?P<artist>.+)\ \&\ (?P<title>.+)\ \(\Live\)'
    assert pp._titleregex == expected_regex

    # Test that parsing works with the escaped regex
    info = {"title": "Adele & Hello (Live)"}
    out, updated = pp.run(info)
    assert updated["artist"] == "Adele"
    assert updated["title"] == "Hello"
