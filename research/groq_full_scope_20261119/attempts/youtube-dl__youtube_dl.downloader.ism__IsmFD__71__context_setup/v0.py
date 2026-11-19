import io
import pytest
import types
from urllib import error as urllib_error

# Import the target class
from youtube_dl.downloader.ism import IsmFD, extract_box_data, u32

# Helper to create a minimal writable stream
class DummyStream(io.BytesIO):
    def __init__(self):
        super().__init__()
        self.written = []

    def write(self, b):
        self.written.append(b)
        return super().write(b)

# Helper to create a dummy IsmFD instance with overridden methods
def make_ismfd(params=None):
    ydl = types.SimpleNamespace()
    fd = IsmFD(ydl, params or {})
    # Replace methods with dummies that record calls
    fd._prepare_and_start_frag_download = lambda ctx: setattr(fd, 'prepare_called', True)
    fd._download_fragment = lambda ctx, url, info: (True, b'\x00'*8 + b'moof' + b'\x00'*4 + b'traf' + b'\x00'*4 + b'tfhd' + b'\x00'*4)
    fd._append_fragment = lambda ctx, frag: setattr(fd, 'appended', True)
    fd._finish_frag_download = lambda ctx: setattr(fd, 'finish_called', True)
    fd.report_retry_fragment = lambda err, frag_index, count, max_retries: setattr(fd, 'retry_called', True)
    fd.report_skip_fragment = lambda frag_index: setattr(fd, 'skip_called', True)
    fd.report_error = lambda msg: setattr(fd, 'error_called', msg)
    fd._download_fragment = lambda ctx, url, info: (True, b'\x00'*8 + b'moof' + b'\x00'*4 + b'traf' + b'\x00'*4 + b'tfhd' + b'\x00'*4)
    return fd

def test_normal_download(tmp_path):
    fd = make_ismfd()
    dest = DummyStream()
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None}
    }
    result = fd.real_download(str(tmp_path / 'output'), info)
    assert result is True
    assert getattr(fd, 'prepare_called', False)
    assert getattr(fd, 'appended', False)
    assert getattr(fd, 'finish_called', False)
    # track_id should be set from extracted data (first 4 bytes after tfhd)
    assert info['_download_params']['track_id'] == 0
    # ensure write_piff_header was called by checking stream has data
    assert dest.written, "Piff header not written"

def test_skip_unavailable_fragment(tmp_path):
    fd = make_ismfd({'fragment_retries': 1, 'skip_unavailable_fragments': True})
    dest = DummyStream()
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None}
    }
    # Simulate HTTPError on first attempt
    def download_fail(ctx, url, info):
        raise urllib_error.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
    fd._download_fragment = download_fail
    result = fd.real_download(str(tmp_path / 'output'), info)
    assert result is True  # skip but overall success
    assert getattr(fd, 'skip_called', False)
    assert not getattr(fd, 'appended', False)

def test_giving_up_after_retries(tmp_path):
    fd = make_ismfd({'fragment_retries': 1, 'skip_unavailable_fragments': False})
    dest = DummyStream()
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None}
    }
    # Simulate HTTPError on both attempts
    def download_fail(ctx, url, info):
        raise urllib_error.HTTPError(url, 500, "Server Error", hdrs=None, fp=None)
    fd._download_fragment = download_fail
    result = fd.real_download(str(tmp_path / 'output'), info)
    assert result is False
    assert getattr(fd, 'error_called', None) == 'giving up after 1 fragment retries'
