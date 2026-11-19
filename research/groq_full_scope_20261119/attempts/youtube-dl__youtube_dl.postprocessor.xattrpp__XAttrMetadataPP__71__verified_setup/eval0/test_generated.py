import os
import pytest
from youtube_dl.postprocessor.xattrpp import XAttrMetadataPP, XAttrUnavailableError, XAttrMetadataError
from youtube_dl.utils import hyphenate_date

class DummyDownloader:
    def __init__(self):
        self.messages = []

    def to_screen(self, msg):
        self.messages.append(('screen', msg))

    def report_error(self, msg):
        self.messages.append(('error', msg))

    def report_warning(self, msg):
        self.messages.append(('warning', msg))

def test_run_writes_expected_xattrs(tmp_path):
    # Create a dummy file
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    # Prepare info dict with all fields
    info = {
        'filepath': str(file_path),
        'webpage_url': 'https://example.com',
        'title': 'Test Title',
        'upload_date': '20240101',
        'description': 'A description',
        'uploader': 'Uploader',
        'format': 'mp4',
    }
    # Monkeypatch write_xattr to record calls
    calls = []
    def fake_write_xattr(path, name, value):
        calls.append((path, name, value))
    original_write_xattr = XAttrMetadataPP.__dict__['write_xattr'] if 'write_xattr' in XAttrMetadataPP.__dict__ else None
    try:
        # Replace the function in the module
        import youtube_dl.postprocessor.xattrpp as mod
        mod.write_xattr = fake_write_xattr
        pp = XAttrMetadataPP(DummyDownloader())
        pp.run(info)
    finally:
        if original_write_xattr is not None:
            mod.write_xattr = original_write_xattr
    # Verify that each expected xattr was written with correct value
    expected = {
        'user.xdg.referrer.url': b'https://example.com',
        'user.dublincore.title': b'Test Title',
        'user.dublincore.date': hyphenate_date('20240101').encode('utf-8'),
        'user.dublincore.description': b'A description',
        'user.dublincore.contributor': b'Uploader',
        'user.dublincore.format': b'mp4',
    }
    assert len(calls) == len(expected)
    for path, name, value in calls:
        assert path == str(file_path)
        assert expected[name] == value

def test_run_unavailable_error(tmp_path):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    info = {'filepath': str(file_path), 'title': 'Test'}
    def fake_write_xattr(path, name, value):
        raise XAttrUnavailableError("xattr not supported")
    original_write_xattr = XAttrMetadataPP.__dict__['write_xattr'] if 'write_xattr' in XAttrMetadataPP.__dict__ else None
    try:
        import youtube_dl.postprocessor.xattrpp as mod
        mod.write_xattr = fake_write_xattr
        downloader = DummyDownloader()
        pp = XAttrMetadataPP(downloader)
        pp.run(info)
    finally:
        if original_write_xattr is not None:
            mod.write_xattr = original_write_xattr
    # Expect an error message reported
    assert ('error', 'xattr not supported') in downloader.messages

def test_run_metadata_error_no_space(tmp_path):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy")
    info = {'filepath': str(file_path), 'title': 'Test'}
    def fake_write_xattr(path, name, value):
        raise XAttrMetadataError("no space", reason='NO_SPACE')
    original_write_xattr = XAttrMetadataPP.__dict__['write_xattr'] if 'write_xattr' in XAttrMetadataPP.__dict__ else None
    try:
        import youtube_dl.postprocessor.xattrpp as mod
        mod.write_xattr = fake_write_xattr
        downloader = DummyDownloader()
        pp = XAttrMetadataPP(downloader)
        pp.run(info)
    finally:
        if original_write_xattr is not None:
            mod.write_xattr = original_write_xattr
    # Expect a warning about no space
    assert any(msg[0] == 'warning' and "no disk space" in msg[1] for msg in downloader.messages)
