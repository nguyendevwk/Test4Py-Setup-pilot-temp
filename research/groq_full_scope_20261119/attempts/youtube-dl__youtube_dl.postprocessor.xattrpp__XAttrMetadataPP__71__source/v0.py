import os
import pytest
from youtube_dl.postprocessor.xattrpp import XAttrMetadataPP
from youtube_dl.utils import XAttrUnavailableError, XAttrMetadataError

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
def dummy_pp(tmp_path):
    pp = XAttrMetadataPP()
    pp._downloader = DummyDownloader()
    return pp, tmp_path

def test_run_writes_expected_xattrs(dummy_pp, monkeypatch):
    pp, tmp_path = dummy_pp
    file = tmp_path / "video.mp4"
    file.write_text("dummy")
    info = {
        'filepath': str(file),
        'webpage_url': 'https://example.com',
        'title': 'Test Video',
        'upload_date': '20240101',
        'description': 'A test',
        'uploader': 'Tester',
        'format': 'mp4',
    }
    written = []

    def fake_write_xattr(path, name, value):
        written.append((name, value.decode()))
    monkeypatch.setattr(pp, 'write_xattr', fake_write_xattr)

    # monkeypatch the imported write_xattr
    monkeypatch.setattr('youtube_dl.postprocessor.xattrpp.write_xattr', fake_write_xattr)

    pp.run(info)

    expected = {
        'user.xdg.referrer.url': 'https://example.com',
        'user.dublincore.title': 'Test Video',
        'user.dublincore.date': '2024-01-01',
        'user.dublincore.description': 'A test',
        'user.dublincore.contributor': 'Tester',
        'user.dublincore.format': 'mp4',
    }
    assert set(written) == set((k, v) for k, v in expected.items())
    assert ('error', _) not in pp._downloader.messages
    assert ('warning', _) not in pp._downloader.messages

def test_run_unavailable_error(dummy_pp, monkeypatch):
    pp, tmp_path = dummy_pp
    file = tmp_path / "video.mp4"
    file.write_text("dummy")
    info = {'filepath': str(file)}

    def fake_write_xattr(path, name, value):
        raise XAttrUnavailableError("xattr not available")
    monkeypatch.setattr('youtube_dl.postprocessor.xattrpp.write_xattr', fake_write_xattr)

    pp.run(info)

    assert any(msg[0] == 'error' and 'xattr not available' in msg[1] for msg in pp._downloader.messages)

def test_run_no_space_warning(dummy_pp, monkeypatch):
    pp, tmp_path = dummy_pp
    file = tmp_path / "video.mp4"
    file.write_text("dummy")
    info = {
        'filepath': str(file),
        'title': 'Test',
    }

    def fake_write_xattr(path, name, value):
        raise XAttrMetadataError('NO_SPACE')
    monkeypatch.setattr('youtube_dl.postprocessor.xattrpp.write_xattr', fake_write_xattr)

    pp.run(info)

    assert any(msg[0] == 'warning' and "no disk space" in msg[1] for msg in pp._downloader.messages)
