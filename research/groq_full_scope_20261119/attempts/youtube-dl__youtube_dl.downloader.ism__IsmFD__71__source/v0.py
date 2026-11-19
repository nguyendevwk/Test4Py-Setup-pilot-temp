import io
import types
import pytest
from youtube_dl.downloader import ism
from urllib.error import HTTPError

# Helper to create a minimal fragment content with a fake tfhd box
def make_fragment_content(track_id=1):
    # tfhd box: 'tfhd' + 4 bytes track_id
    return b'moof' + b'traf' + b'tfhd' + (track_id.to_bytes(4, 'big') + b'xxxx')

class DummyIsmFD(ism.IsmFD):
    def __init__(self, params=None):
        super().__init__(params=params or {})
        self.calls = []

    def _prepare_and_start_frag_download(self, ctx):
        self.calls.append(('prepare', ctx))

    def _download_fragment(self, ctx, url, info_dict):
        self.calls.append(('download', url))
        # Simulate success with dummy content
        return True, make_fragment_content()

    def _append_fragment(self, ctx, frag_content):
        self.calls.append(('append', frag_content))

    def _finish_frag_download(self, ctx):
        self.calls.append(('finish', ctx))

    def report_retry_fragment(self, err, frag_index, count, max_retries):
        self.calls.append(('retry', frag_index, count))

    def report_skip_fragment(self, frag_index):
        self.calls.append(('skip', frag_index))

    def report_error(self, msg):
        self.calls.append(('error', msg))

# Patch external helpers
@pytest.fixture(autouse=True)
def patch_helpers(monkeypatch):
    monkeypatch.setattr(ism, 'write_piff_header', lambda stream, params: stream.write(b'header'))
    monkeypatch.setattr(ism, 'extract_box_data', lambda content, boxes: content)
    monkeypatch.setattr(ism, 'u32', types.SimpleNamespace(unpack=lambda b: [int.from_bytes(b, 'big')]))

def test_normal_download(tmp_path):
    fd = DummyIsmFD()
    dest = tmp_path / "output.mp4"
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {}
    }
    result = fd.real_download(str(dest), info)
    assert result is True
    # Ensure header written once and fragment appended
    assert any(call[0] == 'append' for call in fd.calls)
    assert any(call[0] == 'finish' for call in fd.calls)
    # Check that track_id was set
    assert info['_download_params']['track_id'] == 1

def test_retry_on_http_error(tmp_path, monkeypatch):
    class RetryIsmFD(DummyIsmFD):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attempt = 0

        def _download_fragment(self, ctx, url, info_dict):
            self.attempt += 1
            if self.attempt == 1:
                raise HTTPError(url, 500, "Server error", hdrs=None, fp=None)
            return True, make_fragment_content()

    fd = RetryIsmFD(params={'fragment_retries': 1})
    dest = tmp_path / "output.mp4"
    info = {'fragments': [{'url': 'http://example.com/frag1'}], '_download_params': {}}
    result = fd.real_download(str(dest), info)
    assert result is True
    # Ensure retry was reported
    assert any(call[0] == 'retry' for call in fd.calls)
    # Ensure fragment appended after retry
    assert any(call[0] == 'append' for call in fd.calls)

def test_skip_unavailable_fragment(tmp_path):
    class SkipIsmFD(DummyIsmFD):
        def _download_fragment(self, ctx, url, info_dict):
            raise HTTPError(url, 404, "Not found", hdrs=None, fp=None)

    fd = SkipIsmFD(params={'fragment_retries': 0, 'skip_unavailable_fragments': True})
    dest = tmp_path / "output.mp4"
    info = {'fragments': [{'url': 'http://example.com/frag1'}], '_download_params': {}}
    result = fd.real_download(str(dest), info)
    assert result is True
    # Ensure skip was reported
    assert any(call[0] == 'skip' for call in fd.calls)
    # No append should occur
    assert not any(call[0] == 'append' for call in fd.calls)
