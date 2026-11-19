import io
import pytest
from youtube_dl.downloader import ism

# Helper to create a minimal IsmFD subclass that records actions
class DummyIsmFD(ism.IsmFD):
    def __init__(self, params=None):
        super().__init__(params=params or {})
        self.actions = []

    def _prepare_and_start_frag_download(self, ctx):
        self.actions.append(("prepare", ctx))

    def _download_fragment(self, ctx, url, info_dict):
        # Simulate a successful download returning dummy content
        return True, b'\x00\x00\x00\x00\x00\x00\x00\x01'  # dummy frag_content

    def _append_fragment(self, ctx, frag_content):
        self.actions.append(("append", frag_content))

    def _finish_frag_download(self, ctx):
        self.actions.append(("finish", ctx))

    def report_retry_fragment(self, err, frag_index, count, max_retries):
        self.actions.append(("retry", frag_index, count, max_retries))

    def report_skip_fragment(self, frag_index):
        self.actions.append(("skip", frag_index))

    def report_error(self, msg):
        self.actions.append(("error", msg))

# Patch external dependencies used by real_download
@pytest.fixture(autouse=True)
def patch_external(monkeypatch):
    # extract_box_data returns bytes where track id is at offset 4-8
    monkeypatch.setattr(ism, "extract_box_data", lambda content, boxes: b'\x00\x00\x00\x00\x00\x00\x00\x01')
    # write_piff_header just writes a header marker
    monkeypatch.setattr(ism, "write_piff_header", lambda stream, params: stream.write(b'HEADER'))
    # u32.unpack returns list with track id
    class DummyU32:
        @staticmethod
        def unpack(data):
            return [1]
    monkeypatch.setattr(ism, "u32", DummyU32)

def test_normal_download(tmp_path):
    fd = DummyIsmFD()
    dest = io.BytesIO()
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {}
    }
    result = fd.real_download(dest, info)
    assert result is True
    # Verify actions: prepare, append, finish
    assert fd.actions[0][0] == "prepare"
    assert fd.actions[1][0] == "append"
    assert fd.actions[2][0] == "finish"
    # Header should be written before first fragment
    dest.seek(0)
    assert dest.read(6) == b'HEADER'

def test_test_mode_limits_fragments(tmp_path):
    fd = DummyIsmFD(params={'test': True})
    dest = io.BytesIO()
    info = {
        'fragments': [
            {'url': 'http://example.com/frag1'},
            {'url': 'http://example.com/frag2'}
        ],
        '_download_params': {}
    }
    result = fd.real_download(dest, info)
    assert result is True
    # Only one fragment should be processed
    assert len([a for a in fd.actions if a[0] == "append"]) == 1
    # The second fragment should be skipped due to test mode
    assert fd.actions[0][0] == "prepare"

def test_retry_exhaustion_and_skip(tmp_path):
    class RetryFailIsmFD(DummyIsmFD):
        def __init__(self, params=None):
            super().__init__(params=params or {})
            self.attempts = 0

        def _download_fragment(self, ctx, url, info_dict):
            self.attempts += 1
            # Fail all attempts
            raise ism.compat_urllib_error.HTTPError(url, 404, "Not Found", {}, None)

    fd = RetryFailIsmFD(params={'fragment_retries': 2, 'skip_unavailable_fragments': True})
    dest = io.BytesIO()
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {}
    }
    result = fd.real_download(dest, info)
    assert result is True  # skip leads to success
    # Should have retried 3 times (initial + 2 retries)
    retry_actions = [a for a in fd.actions if a[0] == "retry"]
    assert len(retry_actions) == 3
    # Skip action should be recorded
    skip_actions = [a for a in fd.actions if a[0] == "skip"]
    assert len(skip_actions) == 1
