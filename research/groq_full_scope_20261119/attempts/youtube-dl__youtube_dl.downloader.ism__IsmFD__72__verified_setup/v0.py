import builtins
import types
import io
import pytest
from youtube_dl.downloader.ism import IsmFD, extract_box_data, write_piff_header
from youtube_dl.compat import compat_urllib_error

# Helper subclass that records calls and supplies deterministic behavior
class TestIsmFD(IsmFD):
    def __init__(self, params):
        super().__init__(params)
        self.prepare_called = False
        self.append_calls = []
        self.finish_called = False
        self.retry_calls = []
        self.skip_calls = []
        self.error_calls = []
        self.dest_stream = io.BytesIO()

    # Override required methods
    def _prepare_and_start_frag_download(self, ctx):
        self.prepare_called = True
        ctx['dest_stream'] = self.dest_stream

    def _download_fragment(self, ctx, url, info_dict):
        # Simulate success on first attempt
        if not hasattr(self, 'download_attempt'):
            self.download_attempt = 0
        self.download_attempt += 1
        # Return a byte string containing 'tfhd' box for the first fragment
        if self.download_attempt == 1:
            return True, b'\x00\x00\x00\x00moof\x00\x00\x00\x00traf\x00\x00\x00\x00tfhd\x00\x00\x00\x01'
        # Simulate failure for subsequent attempts
        raise compat_urllib_error.HTTPError(url, 404, "Not Found", {}, None)

    def _append_fragment(self, ctx, frag_content):
        self.append_calls.append(frag_content)

    def _finish_frag_download(self, ctx):
        self.finish_called = True

    def report_retry_fragment(self, err, frag_index, count, fragment_retries):
        self.retry_calls.append((frag_index, count))

    def report_skip_fragment(self, frag_index):
        self.skip_calls.append(frag_index)

    def report_error(self, msg):
        self.error_calls.append(msg)


def test_normal_download_single_fragment(tmp_path):
    """Test normal download with a single fragment succeeds and writes header."""
    fd = TestIsmFD(params={})
    # Prepare dummy info_dict
    info_dict = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None},
    }
    # Monkeypatch helper functions to avoid external dependencies
    original_extract = extract_box_data
    original_write = write_piff_header
    try:
        def fake_extract(data, boxes):
            # Return bytes where bytes[4:8] = track id 1
            return b'\x00\x00\x00\x01'
        def fake_write(stream, params):
            stream.write(b'HEADER')
        globals()['extract_box_data'] = fake_extract
        globals()['write_piff_header'] = fake_write

        result = fd.real_download(tmp_path / 'output.mp4', info_dict)
        assert result is True
        assert fd.prepare_called
        assert fd.finish_called
        assert len(fd.append_calls) == 1
        # Header should have been written
        fd.dest_stream.seek(0)
        assert fd.dest_stream.read() == b'HEADER' + fd.append_calls[0]
        # Track id should be set
        assert info_dict['_download_params']['track_id'] == 1
    finally:
        globals()['extract_box_data'] = original_extract
        globals()['write_piff_header'] = original_write


def test_test_param_limits_to_first_fragment(tmp_path):
    """When 'test' param is True, only the first fragment is processed."""
    fd = TestIsmFD(params={'test': True})
    info_dict = {
        'fragments': [
            {'url': 'http://example.com/frag1'},
            {'url': 'http://example.com/frag2'},
        ],
        '_download_params': {'track_id': None},
    }
    original_extract = extract_box_data
    original_write = write_piff_header
    try:
        def fake_extract(data, boxes):
            return b'\x00\x00\x00\x02'
        def fake_write(stream, params):
            stream.write(b'HEADER')
        globals()['extract_box_data'] = fake_extract
        globals()['write_piff_header'] = fake_write

        result = fd.real_download(tmp_path / 'output.mp4', info_dict)
        assert result is True
        # Only one fragment should be appended
        assert len(fd.append_calls) == 1
        # Track id should be set to 2
        assert info_dict['_download_params']['track_id'] == 2
    finally:
        globals()['extract_box_data'] = original_extract
        globals()['write_piff_header'] = original_write


def test_fragment_retry_and_skip(tmp_path):
    """Test that fragment retries are attempted and fragment is skipped after exhaustion."""
    fd = TestIsmFD(params={'fragment_retries': 1, 'skip_unavailable_fragments': True})
    info_dict = {
        'fragments': [{'url': 'http://example.com/frag1'}],
        '_download_params': {'track_id': None},
    }
    original_extract = extract_box_data
    original_write = write_piff_header
    try:
        def fake_extract(data, boxes):
            return b'\x00\x00\x00\x03'
        def fake_write(stream, params):
            stream.write(b'HEADER')
        globals()['extract_box_data'] = fake_extract
        globals()['write_piff_header'] = fake_write

        result = fd.real_download(tmp_path / 'output.mp4', info_dict)
        # Since download fails after retries, fragment should be skipped
        assert result is True
        assert fd.skip_calls == [1]
        assert fd.retry_calls == [(1, 1)]
        # No fragment appended
        assert len(fd.append_calls) == 0
    finally:
        globals()['extract_box_data'] = original_extract
        globals()['write_piff_header'] = original_write
