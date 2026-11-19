import os
import tempfile
import pytest
from youtube_dl.postprocessor.xattrpp import XAttrMetadataPP
from youtube_dl.utils import XAttrMetadataError, XAttrUnavailableError

# Helper to create a dummy downloader with minimal interface
class DummyDownloader:
    def __init__(self):
        self.messages = []

    def to_screen(self, msg):
        self.messages.append(('screen', msg))

    def report_error(self, msg):
        self.messages.append(('error', msg))

    def report_warning(self, msg):
        self.messages.append(('warning', msg))

# Test normal operation: all attributes written successfully
def test_xattr_metadatapp_success(tmp_path):
    # Create a temporary file to attach xattrs
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy content")

    # Patch write_xattr to record calls instead of actually writing
    calls = []
    def fake_write_xattr(fname, name, value):
        assert fname == str(file_path)
        calls.append((name, value.decode('utf-8')))

    # Monkeypatch the function in the module
    original_write = XAttrMetadataPP.__module__.write_xattr
    XAttrMetadataPP.__module__.write_xattr = fake_write_xattr

    try:
        downloader = DummyDownloader()
        pp = XAttrMetadataPP(downloader)
        info = {
            'filepath': str(file_path),
            'webpage_url': 'https://example.com',
            'title': 'Test Video',
            'upload_date': '20240101',
            'description': 'A test video',
            'uploader': 'Tester',
            'format': 'mp4',
        }
        pp.run(info)

        # Verify that all expected xattrs were attempted
        expected = {
            'user.xdg.referrer.url': 'https://example.com',
            'user.dublincore.title': 'Test Video',
            'user.dublincore.date': '2024-01-01',
            'user.dublincore.description': 'A test video',
            'user.dublincore.contributor': 'Tester',
            'user.dublincore.format': 'mp4',
        }
        assert set(name for name, _ in calls) == set(expected.keys())
        for name, value in calls:
            assert expected[name] == value
        # No error or warning messages should be recorded
        assert all(msg[0] == 'screen' for msg in downloader.messages)
    finally:
        XAttrMetadataPP.__module__.write_xattr = original_write

# Test boundary: missing optional fields should not raise errors
def test_xattr_metadatapp_missing_fields(tmp_path):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy content")

    calls = []
    def fake_write_xattr(fname, name, value):
        calls.append((name, value.decode('utf-8')))

    original_write = XAttrMetadataPP.__module__.write_xattr
    XAttrMetadataPP.__module__.write_xattr = fake_write_xattr

    try:
        downloader = DummyDownloader()
        pp = XAttrMetadataPP(downloader)
        info = {
            'filepath': str(file_path),
            'title': 'Only Title',
            # No other fields provided
        }
        pp.run(info)

        # Only the title xattr should be written
        assert calls == [('user.dublincore.title', 'Only Title')]
        # No error or warning messages
        assert all(msg[0] == 'screen' for msg in downloader.messages)
    finally:
        XAttrMetadataPP.__module__.write_xattr = original_write

# Test error handling: simulate XAttrMetadataError with NO_SPACE reason
def test_xattr_metadatapp_no_space_error(tmp_path):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy content")

    def fake_write_xattr(fname, name, value):
        # Simulate disk full after first write
        if name == 'user.dublincore.title':
            raise XAttrMetadataError('NO_SPACE')

    original_write = XAttrMetadataPP.__module__.write_xattr
    XAttrMetadataPP.__module__.write_xattr = fake_write_xattr

    try:
        downloader = DummyDownloader()
        pp = XAttrMetadataPP(downloader)
        info = {
            'filepath': str(file_path),
            'title': 'Title',
            'description': 'Desc',
        }
        pp.run(info)

        # Expect a warning about no space
        warnings = [msg for typ, msg in downloader.messages if typ == 'warning']
        assert any("no disk space" in w.lower() for w in warnings)
        # No error messages should be recorded
        errors = [msg for typ, msg in downloader.messages if typ == 'error']
        assert not errors
    finally:
        XAttrMetadataPP.__module__.write_xattr = original_write
