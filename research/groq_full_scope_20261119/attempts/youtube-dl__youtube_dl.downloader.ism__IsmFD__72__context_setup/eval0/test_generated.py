import io
import pytest
import types
from youtube_dl.downloader.ism import IsmFD, extract_box_data, u32
from youtube_dl.compat import compat_urllib_error

class DummyIsmFD(IsmFD):
    def __init__(self, ydl, params):
        super().__init__(ydl, params)
        self.calls = []
        self.dest_stream = io.BytesIO()
        self.track_written = False

    def _prepare_and_start_frag_download(self, ctx):
        self.calls.append(('prepare', ctx))

    def _download_fragment(self, ctx, url, info_dict):
        self.calls.append(('download', url))
        # Simulate a successful download returning dummy data
        dummy_data = b'\x00\x00\x00\x08moof' + b'\x00'*4 + b'\x00\x00\x00\x08traf' + b'\x00'*4 + b'\x00\x00\x00\x08tfhd' + b'\x00'*4
        return True, dummy_data

    def _append_fragment(self, ctx, frag_content):
        self.calls.append(('append', frag_content))
        self.dest_stream.write(frag_content)

    def _finish_frag_download(self, ctx):
        self.calls.append(('finish', ctx))

    def report_retry_fragment(self, err, frag_index, count, fragment_retries):
        self.calls.append(('retry', frag_index, count))

    def report_skip_fragment(self, frag_index):
        self.calls.append(('skip', frag_index))

    def report_error(self, msg):
        self.calls.append(('error', msg))

    def write_piff_header(self, stream, params):
        self.calls.append(('write_header', params))
        stream.write(b'header')

def test_normal_download(tmp_path):
    fd = DummyIsmFD(ydl=None, params={})
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None}
    }
    result = fd.real_download(str(tmp_path / 'out'), info)
    assert result is True
    # Ensure header written and fragment appended
    assert any(call[0] == 'write_header' for call in fd.calls)
    assert any(call[0] == 'append' for call in fd.calls)
    # dest_stream should contain header + dummy data
    content = fd.dest_stream.getvalue()
    assert content.startswith(b'header')
    assert b'moof' in content

def test_test_mode_only_first_fragment(tmp_path):
    fd = DummyIsmFD(ydl=None, params={'test': True})
    info = {
        'fragments': [
            {'url': 'http://example.com/frag1'},
            {'url': 'http://example.com/frag2'}
        ],
        '_download_params': {'track_id': None}
    }
    result = fd.real_download(str(tmp_path / 'out'), info)
    assert result is True
    # Only first fragment should be downloaded
    download_calls = [c for c in fd.calls if c[0] == 'download']
    assert len(download_calls) == 1
    assert download_calls[0][1] == 'http://example.com/frag1'

def test_retry_and_skip(tmp_path):
    class RetryDummyIsmFD(DummyIsmFD):
        def __init__(self, ydl, params):
            super().__init__(ydl, params)
            self.attempts = 0

        def _download_fragment(self, ctx, url, info_dict):
            self.attempts += 1
            if self.attempts < 3:
                raise compat_urllib_error.HTTPError(url, 404, 'Not Found', {}, None)
            return True, b'\x00\x00\x00\x08moof' + b'\x00'*4 + b'\x00\x00\x00\x08traf' + b'\x00'*4 + b'\x00\x00\x00\x08tfhd' + b'\x00'*4

    fd = RetryDummyIsmFD(ydl=None, params={'fragment_retries': 2, 'skip_unavailable_fragments': True})
    info = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None}
    }
    result = fd.real_download(str(tmp_path / 'out'), info)
    assert result is True
    # Should have retried twice before success
    retry_calls = [c for c in fd.calls if c[0] == 'retry']
    assert len(retry_calls) == 2
    # No skip should occur because success after retries
    skip_calls = [c for c in fd.calls if c[0] == 'skip']
    assert not skip_calls
