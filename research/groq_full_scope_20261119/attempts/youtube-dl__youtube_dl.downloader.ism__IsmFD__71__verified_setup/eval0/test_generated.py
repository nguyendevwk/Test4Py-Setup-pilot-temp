import io
import types
import pytest
from youtube_dl.downloader import ism

# Patch helper functions used by IsmFD
ism.extract_box_data = lambda data, boxes: data  # return data unchanged
ism.u32 = types.SimpleNamespace(unpack=lambda b: [int.from_bytes(b, 'big')])
ism.write_piff_header = lambda stream, params: stream.write(b'header')

class DummyIsmFD(ism.IsmFD):
    def __init__(self, params=None):
        super().__init__(params=params or {})
        self.prepare_called = False
        self.download_calls = []
        self.append_calls = []
        self.finish_called = False
        self.retry_calls = []
        self.skip_calls = []
        self.error_calls = []

    def _prepare_and_start_frag_download(self, ctx):
        self.prepare_called = True
        ctx['dest_stream'] = io.BytesIO()

    def _download_fragment(self, ctx, url, info_dict):
        self.download_calls.append(url)
        # Simulate failure for specific URL
        if url == 'fail':
            return False, b''
        # Simulate HTTPError for specific URL
        if url == 'http_error':
            raise ism.compat_urllib_error.HTTPError(url, 404, 'Not Found', {}, None)
        return True, b'fragment_data'

    def _append_fragment(self, ctx, frag_content):
        self.append_calls.append(frag_content)
        ctx['dest_stream'].write(frag_content)

    def _finish_frag_download(self, ctx):
        self.finish_called = True

    def report_retry_fragment(self, err, frag_index, count, fragment_retries):
        self.retry_calls.append((frag_index, count))

    def report_skip_fragment(self, frag_index):
        self.skip_calls.append(frag_index)

    def report_error(self, msg):
        self.error_calls.append(msg)

def test_successful_download(tmp_path):
    fd = DummyIsmFD()
    info = {
        'fragments': [{'url': 'http://example.com/seg1'}],
        '_download_params': {}
    }
    result = fd.real_download(tmp_path / 'out.mp4', info)
    assert result is True
    assert fd.prepare_called
    assert fd.download_calls == ['http://example.com/seg1']
    assert fd.append_calls == [b'fragment_data']
    assert fd.finish_called
    # dest_stream should contain header + fragment_data
    data = fd._prepare_and_start_frag_download.__self__.dest_stream.getvalue()
    assert data.startswith(b'header')
    assert b'fragment_data' in data

def test_retry_and_skip(tmp_path):
    fd = DummyIsmFD(params={'fragment_retries': 1, 'skip_unavailable_fragments': True})
    info = {
        'fragments': [{'url': 'http_error'}],
        '_download_params': {}
    }
    result = fd.real_download(tmp_path / 'out.mp4', info)
    assert result is True
    assert fd.retry_calls == [(1, 1)]
    assert fd.skip_calls == [1]
    assert fd.error_calls == []

def test_retry_and_fail(tmp_path):
    fd = DummyIsmFD(params={'fragment_retries': 1, 'skip_unavailable_fragments': False})
    info = {
        'fragments': [{'url': 'http_error'}],
        '_download_params': {}
    }
    result = fd.real_download(tmp_path / 'out.mp4', info)
    assert result is False
    assert fd.retry_calls == [(1, 1)]
    assert fd.skip_calls == []
    assert fd.error_calls == ['giving up after 1 fragment retries']
