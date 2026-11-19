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

@pytest.fixture
def dummy_downloader():
    return DummyDownloader()

def test_run_writes_expected_xattrs(tmp_path, dummy_downloader, monkeypatch):
    # Create a dummy file
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy content")

    # Capture calls to write_xattr
    called = []

    def fake_write_xattr(fname, key, value):
        called.append((fname, key, value))

    monkeypatch.setattr("youtube_dl.postprocessor.xattrpp.write_xattr", fake_write_xattr)

    pp = XAttrMetadataPP(dummy_downloader)
    info = {
        'filepath': str(file_path),
        'webpage_url': 'https://example.com',
        'title': 'Test Video',
        'upload_date': '20240101',
        'description': 'A test',
        'uploader': 'Tester',
        'format': 'mp4',
    }

    pp.run(info)

    # Verify that each expected xattr was written with correct value
    expected = {
        'user.xdg.referrer.url': b'https://example.com',
        'user.dublincore.title': b'Test Video',
        'user.dublincore.date': hyphenate_date('20240101').encode('utf-8'),
        'user.dublincore.description': b'A test',
        'user.dublincore.contributor': b'Tester',
        'user.dublincore.format': b'mp4',
    }
    assert set(k for _, k, _ in called) == set(expected.keys())
    for _, key, value in called:
        assert value == expected[key]
    # Ensure no error or warning was reported
    assert all(m[0] != 'error' for m in dummy_downloader.messages)
    assert all(m[0] != 'warning' for m in dummy_downloader.messages)

def test_run_unavailable_error(tmp_path, dummy_downloader, monkeypatch):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy content")

    def fake_write_xattr(fname, key, value):
        raise XAttrUnavailableError("xattr not supported")

    monkeypatch.setattr("youtube_dl.postprocessor.xattrpp.write_xattr", fake_write_xattr)

    pp = XAttrMetadataPP(dummy_downloader)
    info = {'filepath': str(file_path), 'title': 'Test'}

    pp.run(info)

    # Expect an error message reported
    errors = [msg for typ, msg in dummy_downloader.messages if typ == 'error']
    assert any("xattr not supported" in e for e in errors)

def test_run_no_space_warning(tmp_path, dummy_downloader, monkeypatch):
    file_path = tmp_path / "video.mp4"
    file_path.write_text("dummy content")

    # Simulate writing first attribute succeeds, second fails with NO_SPACE
    call_count = 0
    def fake_write_xattr(fname, key, value):
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise XAttrMetadataError("NO_SPACE", "No space left")
        return

    monkeypatch.setattr("youtube_dl.postprocessor.xattrpp.write_xattr", fake_write_xattr)

    pp = XAttrMetadataPP(dummy_downloader)
    info = {
        'filepath': str(file_path),
        'title': 'Test',
        'upload_date': '20240101',
    }

    pp.run(info)

    # Expect a warning about no space
    warnings = [msg for typ, msg in dummy_downloader.messages if typ == 'warning']
    assert any("no disk space" in w.lower() for w in warnings)
    # Ensure no error was reported
    assert all(m[0] != 'error' for m in dummy_downloader.messages)
