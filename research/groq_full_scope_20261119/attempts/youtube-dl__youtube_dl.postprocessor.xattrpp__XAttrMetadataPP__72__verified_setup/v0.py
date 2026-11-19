import os
import pytest
from youtube_dl.postprocessor.xattrpp import XAttrMetadataPP, XAttrUnavailableError, XAttrMetadataError

class DummyDownloader:
    def __init__(self):
        self.messages = []

    def to_screen(self, msg):
        self.messages.append(("screen", msg))

    def report_error(self, msg):
        self.messages.append(("error", msg))

    def report_warning(self, msg):
        self.messages.append(("warning", msg))

@pytest.fixture
def downloader():
    return DummyDownloader()

def test_run_writes_expected_xattrs(tmp_path, downloader, monkeypatch):
    # Create a dummy file
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    # Prepare info dict with all fields
    info = {
        "filepath": str(file_path),
        "webpage_url": "https://example.com",
        "title": "Test Video",
        "upload_date": "20240101",
        "description": "A test video",
        "uploader": "Tester",
        "format": "mp4",
    }
    # Patch write_xattr to record calls
    calls = []
    def fake_write_xattr(fname, name, value):
        calls.append((fname, name, value))
    monkeypatch.setattr("youtube_dl.postprocessor.xattrpp.write_xattr", fake_write_xattr)
    pp = XAttrMetadataPP(downloader)
    pp.run(info)
    # Verify that each expected xattr was written with correct value
    expected = {
        "user.xdg.referrer.url": b"https://example.com",
        "user.dublincore.title": b"Test Video",
        "user.dublincore.date": b"2024-01-01",
        "user.dublincore.description": b"A test video",
        "user.dublincore.contributor": b"Tester",
        "user.dublincore.format": b"mp4",
    }
    assert set(name for _, name, _ in calls) == set(expected.keys())
    for _, name, value in calls:
        assert expected[name] == value

def test_run_unavailable_error(tmp_path, downloader, monkeypatch):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    info = {"filepath": str(file_path), "title": "Test"}
    # Simulate XAttrUnavailableError
    def fake_write_xattr(fname, name, value):
        raise XAttrUnavailableError("xattr not supported")
    monkeypatch.setattr("youtube_dl.postprocessor.xattrpp.write_xattr", fake_write_xattr)
    pp = XAttrMetadataPP(downloader)
    pp.run(info)
    # Expect an error message reported
    assert any(msg[0] == "error" and "xattr not supported" in msg[1] for msg in downloader.messages)

def test_run_metadata_error_no_space(tmp_path, downloader, monkeypatch):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    info = {"filepath": str(file_path), "title": "Test"}
    # Simulate XAttrMetadataError with NO_SPACE after one write
    def fake_write_xattr(fname, name, value):
        raise XAttrMetadataError("NO_SPACE")
    monkeypatch.setattr("youtube_dl.postprocessor.xattrpp.write_xattr", fake_write_xattr)
    pp = XAttrMetadataPP(downloader)
    pp.run(info)
    # Expect a warning about no disk space
    assert any(msg[0] == "warning" and "no disk space" in msg[1] for msg in downloader.messages)
